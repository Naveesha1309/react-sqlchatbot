//////////////////////////////////////// SHOW SQL BUTTON //////////////////////////////////////
import React,{useState} from 'react';

const ChatMessage = ({ message, isUser, sql, showSQLButton  }) => {
  const [showSQL, setShowSQL] = useState(false);

  const toggleSQL = () => {
    setShowSQL(!showSQL);
  };

  return (
    <div className={`flex items-start mb-4 ${isUser ? 'flex-row-reverse' : ''}`}>
      <div className="flex-shrink-0">
        <img
          src={isUser ? 'https://cdn-icons-png.freepik.com/256/3001/3001758.png?semt=ais_hybrid' : 'https://t3.ftcdn.net/jpg/02/15/61/92/240_F_215619203_9mmrDaPnSHOUBfz9XVkjBAknw5XFEK0D.jpg'}
          alt={isUser ? 'User' : 'AI'}
          className="w-10 h-10 rounded-full"
        />
      </div>
      <div className={`ml-3 p-2 rounded-lg ${isUser ? 'bg-login-color' : 'bg-gray-200'}`}>
        {message}
        {!isUser && showSQLButton &&(
          <div>
            <button 
              onClick={toggleSQL} 
              className="mt-2 p-1 bg-blue-500 text-white rounded"
            >
              {showSQL ? 'Hide SQL' : 'Show SQL'}
            </button>
            {showSQL && (
              <div className="mt-2 p-2 bg-gray-100 rounded">
                <pre>{sql}</pre>
              </div>
            )}
          </div>
        )}
      </div>
      {console.log("message from chatmessage", message)}
    </div>
  );
};


export default ChatMessage;