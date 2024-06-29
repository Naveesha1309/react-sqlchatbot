from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
# from few_shots_groqllm import few_shots_groqnew
from few_shots_postgres import few_shots_postgresnew

from langchain.prompts import SemanticSimilarityExampleSelector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from langchain.prompts.prompt import PromptTemplate
from sqlalchemy.exc import SQLAlchemyError



load_dotenv()

# langsmith
import os
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"

################### CUSTOM OUTPUT PARSER FOR SQL AND NLP RESPONSE ##############

from typing import NamedTuple
from langchain.schema import BaseOutputParser

class SQLResponse(NamedTuple):
    sql_query: str
    nl_response: str

class SQLResponseOutputParser(BaseOutputParser):
    def parse(self, text: str) -> SQLResponse:
        return SQLResponse(
            sql_query=text.split("SQL Query:")[1].split("Natural Language Response:")[0].strip(),
            nl_response=text.split("Natural Language Response:")[1].strip()
        )

##################### DB CONNECTION ##########

#SQL
# def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
#     db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
#     return SQLDatabase.from_uri(db_uri)

#PGADMIN
def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
    db_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)

def get_sql_chain(db):

# SQL TEMPLATE
    # template = """
    # You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    # Based on the table schema below, write a SQL query that would answer the user's question.

    # <SCHEMA>{schema}</SCHEMA>


    # Write only the SQL query and nothing else. 
    # You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
    # Unless the user specifies in the question a specific number of examples to obtain, query for at most 2 results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
    # Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
    # Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    # Pay attention to use CURDATE() function to get the current date, if the question involves "today".
    # Rule 1: I repeat it again:  Wrap each column name in backticks (`) to denote them as delimited identifiers. Even while joining two tables using common column name, do wrap the columns in backticks. the reason why i am telling this is because
    # the column names have an underscore in between, which is throwing error in parsing SQL code. 
    # Example: FROM employees JOIN mentors ON employees.`mentor\_id` = mentors.`mentor\_id`. 
    # Rule 2: Extremely important rule: For `COUNT(*)`, do not wrap it in backticks or add a backslash before the asterisk. Use `COUNT(*)` as is without any additional characters. 
    # Rule 3: If the user queries anything related to a name, consider a LIKE clause with '%name%'. (it ensures to give results more concisely).

    # For example:
    # User Question: How many of them are from full stack batch located in delhi?
    # SQL Query: SELECT COUNT(*) FROM employees WHERE `department_id` = 2 AND `location` = 'Noida';
    # User Question: Tell me student names who have mentor named Ronald
    # SQL Query: SELECT `first_name`, `last_name` FROM employees join mentors using (`mentor_id`) WHERE `mentor_name` like '%Ronald%';

    # Keep in mind: if the user query is not related to any sql table/database, then do return null. 
    # Your turn:

    # User Question: {question}
    # SQL Query:
    # """

# POSTGRES TEMPLATE
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question.

    <SCHEMA>{schema}</SCHEMA>

    Write only the SQL query and nothing else. 
    You are a PostgreSQL expert. Given an input question, first create a syntactically correct PostgreSQL query to run, then look at the results of the query and return the answer to the input question.
    You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. 
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use CURRENT_DATE function to get the current date, if the question involves "today". 
    Rule 2: Extremely important rule: For `COUNT(*)`, do not wrap it in backticks or add a backslash before the asterisk. Use `COUNT(*)` as is without any additional characters. 
    Rule 3: If the user queries anything related to a name, consider a LIKE clause with '%name%'. (it ensures to give results more concisely).
    Rule 4: Whenever assignment of work is asked by the user, always use the 'project_peopleallocation' table.
    Rule 5: A customer may have more than one projects, thus use the term 'IN' for selecting something, rather than using '=' (equals sign). This applies to all the cases where there is many to one relationship.
    Say, one employee might have different projects to work on etc. When this is the case, ALWAYS fetch out the distinct records.
    for example: select ... where some_id IN (select ) ... and so on

    Rule 6: Take note of column names carefully. for example, do not confuse with id and project_id. Look at the table schema and map correct column name with that table.
    for example: project_detail table has 'id' column, not 'project_id'
    Rule 7: If the user asks question related to some 'domain' projects, alter that domain name to find some similar match to find the role of the person in that project.
    for example: What are the data science projects we are working on? converts to : what are projects where Data Scientists are working on?

    All the nouns should be wrapped inside the like %'(noun)'% format in the sql code.
    for example: project names, customer names etc. 

    For example:
    User Question: How many of the employees have experience greater than 10 and are from delhi city?
    SQL Query: SELECT COUNT(*) FROM employees WHERE experience_yrs > 10 AND city = 'Delhi';

    Make sure of one thing. Do not add any backslash for special characters in the query.
    Example: SELECT COUNT(*) FROM employees WHERE full_name LIKE '%employee167%';

    If the user asks for the tables in the database, list the table names from the 'public' schema:
    User Question: Show me the tables in the database.
    SQL Query: SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

    Your turn:

    User Question: {question}
    SQL Query:

    Related examples:
    {examples}
 
    """
    # 1. Lines removed from the prompt. No need to apply limit:
    # Unless the user specifies in the question a specific number of examples to obtain, query for at most 2 results using the LIMIT clause as per PostgreSQL.
    # 2. Few shots should be provided to the SQL chain instead of get_response chain, hence added to the prompt:
    # Related examples:
    # {examples}

    prompt = ChatPromptTemplate.from_template(template)


    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    # llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)


    def get_schema(_):
        return db.get_table_info()
    
    def post_process_sql(query: str) -> str:
        # Ensure COUNT(*) is correctly formatted
        query = query.replace("\\*", "*")
        query = query.replace("`COUNT(*)`", "COUNT(*)")
        query = query.replace("COUNT(`*`)", "COUNT(*)")
        query = query.replace("COUNT(\*)", "COUNT(*)")
        query = query.replace("COUNT(\\*)", "COUNT(*)")
        # Remove 'SQL Query:' prefix 
        query = query.replace("SQL Query:", "").strip()
        return query

    example_prompt = PromptTemplate(
    input_variables=["User question", "SQL Query", "SQL Response"],
    template="{User question}\n{SQL Query}\n{SQL Response}"
    )

    return (
    RunnablePassthrough.assign(schema=get_schema).assign(
         examples=lambda vars: "\n".join([example_prompt.format(**example) for example in example_selector.select_examples({"Question": vars["question"]})])
    )
    | prompt
    | llm
    | StrOutputParser()
    | (lambda x: post_process_sql(x))
    )


embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
to_vectorize = [" ".join(example.values()) for example in few_shots_postgresnew]
vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots_postgresnew)
example_selector = SemanticSimilarityExampleSelector(   
vectorstore=vectorstore,
k=3,
)

def get_response_new(user_query: str, db: SQLDatabase):
    sql_chain = get_sql_chain(db)
    
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    # llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)


    new_template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, question, sql query, and sql response, write a natural language response.
    

    Keep in mind: Reply only the desired results ONLY. 
    Also, if the sql result is null, then please mention that too in natural langauge.
    
    
    <SCHEMA>{schema}</SCHEMA>

    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}

    Please provide your response in the following format:
    SQL Query: <the SQL query>
    Natural Language Response: <your natural language response>

    Natural language response:
    """
    # 1. Removed few shots (and {top_k}) from this chain because sql chain was generating correct code but the response was influenced by the few shots.
    # Related examples:
    # {examples}
    # Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.

    new_prompt = ChatPromptTemplate.from_template(new_template)

    # removed the fewshottemplate, instead directly added the embedding in the runnable for semantic search.
    # in my opinion the response which it is giving now it great, earlier i was hardcoding the response in few_shots. which is actually not needed, as the database updates frequently.
    # hence, the one which is working now, is right.
    # i just have to add few more few shots to see the change in response.
    # thanks to claude.

    #removed examples from the chain and applied customer string output parser to get two responses, sql query and nlp response. refer the prompt for clarity.
    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            response=lambda vars: db.run(vars["query"])
        )
        | new_prompt
        | llm
        | SQLResponseOutputParser()
    )

    #st.write(example_selector.select_examples({"Question": "Tell me total number of female students studying artificial intelligence/ai"}))
    result= chain.invoke({
        "question": user_query
    })

    return result.nl_response, result.sql_query

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

    response_text,sql_code = get_response_new(user_query, db)
    return jsonify({'response': response_text,'sql':sql_code})

if __name__ == '__main__':
    app.run(debug=True)