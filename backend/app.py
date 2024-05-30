from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from few_shots_groqllm import few_shots_groqnew

from langchain.prompts import SemanticSimilarityExampleSelector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from langchain.prompts.prompt import PromptTemplate
from sqlalchemy.exc import SQLAlchemyError


load_dotenv()

def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
    db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)


def get_sql_chain(db):
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question.

    <SCHEMA>{schema}</SCHEMA>


    Write only the SQL query and nothing else. 
    You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most 2 results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use CURDATE() function to get the current date, if the question involves "today".
    Rule 1: I repeat it again:  Wrap each column name in backticks (`) to denote them as delimited identifiers. Even while joining two tables using common column name, do wrap the columns in backticks. the reason why i am telling this is because
    the column names have an underscore in between, which is throwing error in parsing SQL code. 
    Example: FROM employees JOIN mentors ON employees.`mentor\_id` = mentors.`mentor\_id`. 
    Rule 2: Extremely important rule: For `COUNT(*)`, do not wrap it in backticks or add a backslash before the asterisk. Use `COUNT(*)` as is without any additional characters. 
    Rule 3: If the user queries anything related to a name, consider a LIKE clause with '%name%'. (it ensures to give results more concisely).

    For example:
    User Question: How many of them are from full stack batch located in delhi?
    SQL Query: SELECT COUNT(*) FROM employees WHERE `department_id` = 2 AND `location` = 'Noida';
    User Question: Tell me student names who have mentor named Ronald
    SQL Query: SELECT `first_name`, `last_name` FROM employees join mentors using (`mentor_id`) WHERE `mentor_name` like '%Ronald%';

    Keep in mind: if the user query is not related to any sql table/database, then do return null. 
    Your turn:

    User Question: {question}
    SQL Query:
    """


    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)

    def get_schema(_):
        return db.get_table_info()
    
    def post_process_sql(query: str) -> str:
        # Ensure COUNT(*) is correctly formatted
        query = query.replace("\\*", "*")
        query = query.replace("`COUNT(*)`", "COUNT(*)")
        query = query.replace("COUNT(`*`)", "COUNT(*)")
        query = query.replace("COUNT(\*)", "COUNT(*)")
        query = query.replace("COUNT(\\*)", "COUNT(*)")
        return query

    return (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | llm
    | StrOutputParser()
    | (lambda x: post_process_sql(x))
    )


    

def get_response_new(user_query: str, db: SQLDatabase):
    sql_chain = get_sql_chain(db)
    llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)

    new_template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, question, sql query, and sql response, write a natural language response.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.

    
    
    <SCHEMA>{schema}</SCHEMA>

    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}

    Related examples:
    {examples}

    Answer:
    """

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    to_vectorize = [" ".join(example.values()) for example in few_shots_groqnew]
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots_groqnew)
    example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=2,
    )
    
# Define the prompt template for examples
    example_prompt = PromptTemplate(
    input_variables=["User question", "SQL Query", "SQL Response"],
    template="User question: {User question}\nSQL Query: {SQL Query}\nSQL Response: {SQL Response}"
)


    new_prompt = ChatPromptTemplate.from_template(new_template)

# removed the fewshottemplate, instead directly added the embedding in the runnable for semantic search.
# in my opinion the response which it is giving now it great, earlier i was hardcoding the response in few_shots. which is actually not needed, as the database updates frequently.
# hence, the one which is working now, is right.
# i just have to add few more few shots to see the change in response.
# thanks to claude.

    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            response=lambda vars: db.run(vars["query"]),
            examples=lambda vars: "\n".join([example_prompt.format(**example) for example in example_selector.select_examples({"Question": vars["question"]})]),
        )
        | new_prompt
        | llm
        | StrOutputParser()
    )

    #st.write(example_selector.select_examples({"Question": "Tell me total number of female students studying artificial intelligence/ai"}))
    return chain.invoke({
        "question": user_query,
        "top_k":"1"
    })


########################### ROUTES ###############################

from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/api/connect', methods=['POST'])
def connect_to_db():
    # print(f"Request Headers: {request.headers}")  # Debugging line
    if request.is_json:
        db_info = request.get_json()
        print(f"Received db_info: {db_info}")  # Debugging line
        try:
            db = init_database(
                db_info['user'],
                db_info['password'],
                db_info['host'],
                db_info['port'],
                db_info['database']
            )
            return jsonify({'status': 'success'})
        except SQLAlchemyError as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
    else:
        return jsonify({'status': 'error', 'message': 'Content-Type must be application/json'}), 415

@app.route('/api/chatbot', methods=['POST'])
def handle_chat_request():
    user_query = request.json.get('message')
    db_info = request.json.get('dbInfo')

    # Initialize the database connection
    db = init_database(
        db_info['user'],
        db_info['password'],
        db_info['host'],
        db_info['port'],
        db_info['database']
    )

    # Process the user query using your chatbot logic
    response_text = get_response_new(user_query, db)
    print("response text:",response_text)
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)