import React from 'react';



const ChatMessage = ({ message, isUser }) => {

  
  return (
    <div className={`flex items-start mb-4 ${isUser ? 'flex-row-reverse' : ''}`}>
      <div className="flex-shrink-0">
        <img
          src={isUser ? 'https://cdn-icons-png.freepik.com/256/3001/3001758.png?semt=ais_hybrid' : 'https://t3.ftcdn.net/jpg/02/15/61/92/240_F_215619203_9mmrDaPnSHOUBfz9XVkjBAknw5XFEK0D.jpg'}
          alt={isUser ? 'User' : 'AI'}
          className="w-10 h-10 rounded-full"
        />
      </div>
      <div className={`ml-3 p-2 rounded-lg ${isUser ? 'bg-login-color' : 'bg-gray-200'}`}>{message}</div>
      {console.log("message from chatmessage", message)}
    </div>
        
        
   
  );
};

export default ChatMessage;