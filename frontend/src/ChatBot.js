import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ChatInput from './components/ChatInput';
import ChatMessage from './components/ChatMessage';

const ChatBot = ({ dbInfo }) => {
  const [messages, setMessages] = useState([
    { text: 'Hello! I\'m a SQL assistant. Ask me anything about your database.', isUser: false },
  ]);
  
  const [isLoading, setIsLoading] = useState(false);

  const chatContainerRef = useRef(null);

  const handleSendMessage = async (message) => {
    setIsLoading(true);
    setMessages((prevMessages) => [...prevMessages, { text: message, isUser: true }]);

    try {
      const response = await axios.post('http://localhost:5000/api/chatbot', { message, dbInfo });
      const botResponse = response.data.response;
      setMessages((prevMessages) => [...prevMessages, { text: botResponse, isUser: false }]);
    } catch (error) {
      console.error('Error fetching bot response:', error); // Log detailed error information
      if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
        console.error('Response headers:', error.response.headers);
      }
      setMessages((prevMessages) => [...prevMessages, { text: 'Please provide a question related to the database.', isUser: false }]);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Use useEffect to auto-scroll whenever messages change
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);


  return (
    <div className="flex flex-col h-full p-4">
      <div className="flex-1 overflow-y-auto mb-4"  ref={chatContainerRef}>
        {messages.map((message, index) => (
          <ChatMessage
            key={index}
            message={message.text}
            isUser={message.isUser}
          />
        ))}
      </div>
      <div className="mt-4">
        {isLoading ? <p>Loading...</p> : <ChatInput onSendMessage={handleSendMessage} />}
      </div>
    </div>
  );
};


export default ChatBot;