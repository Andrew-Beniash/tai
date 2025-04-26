/**
 * ChatWidget component
 * Provides an interface for interacting with the AI assistant
 * Includes chat history, message input, and action handling
 */

import { useState, useEffect, useRef } from 'react';
import { sendChatMessage, ChatResponse, getPresetQuestions } from '../api/chat';
import { executeAction, ActionRequest } from '../api/actions';

interface ChatWidgetProps {
  taskId: string;
}

interface ChatMessage {
  sender: 'user' | 'ai';
  content: string;
  timestamp: Date;
  suggestedActionId?: string;
}

export default function ChatWidget({ taskId }: ChatWidgetProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [presetQuestions, setPresetQuestions] = useState<string[]>([]);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Fetch preset questions when component mounts
  useEffect(() => {
    const fetchPresetQuestions = async () => {
      try {
        const questions = await getPresetQuestions(taskId);
        setPresetQuestions(questions);
      } catch (err) {
        console.error('Error fetching preset questions:', err);
      }
    };
    
    fetchPresetQuestions();
  }, [taskId]);
  
  // Add initial greeting message when component mounts
  useEffect(() => {
    setMessages([
      {
        sender: 'ai',
        content: 'Hello! I\'m your AI tax assistant. How can I help you with this task today?',
        timestamp: new Date(),
      }
    ]);
  }, []);
  
  // Scroll to bottom of chat when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;
    
    const userMessage: ChatMessage = {
      sender: 'user',
      content: inputMessage,
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setError(null);
    setIsLoading(true);
    
    try {
      const response = await sendChatMessage(taskId, userMessage.content);
      
      const aiMessage: ChatMessage = {
        sender: 'ai',
        content: response.response,
        timestamp: new Date(),
        suggestedActionId: response.suggestedActionId,
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      setError('Failed to get a response from the AI assistant. Please try again.');
      console.error('Error sending message:', err);
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };
  
  const handlePresetQuestion = async (question: string) => {
    setInputMessage(question);
    // Wait for state update to complete before sending
    setTimeout(() => {
      handleSendMessage();
    }, 0);
  };
  
  const handleExecuteAction = async (actionId: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const actionRequest: ActionRequest = {
        action_id: actionId,
      };
      
      const result = await executeAction(taskId, actionRequest);
      
      if (result.success) {
        // Add a system message about the successful action
        const systemMessage: ChatMessage = {
          sender: 'ai',
          content: `✅ Action completed successfully: ${result.message}`,
          timestamp: new Date(),
        };
        
        setMessages(prev => [...prev, systemMessage]);
      } else {
        setError(`Action failed: ${result.message}`);
      }
    } catch (err) {
      setError('Failed to execute action. Please try again.');
      console.error('Error executing action:', err);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Function to render chat message based on type
  const renderMessage = (message: ChatMessage, index: number) => {
    if (message.sender === 'user') {
      return (
        <div key={index} className="flex justify-end mb-4">
          <div className="bg-blue-600 text-white rounded-lg py-2 px-4 max-w-md">
            <p>{message.content}</p>
            <p className="text-xs text-blue-200 mt-1 text-right">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </p>
          </div>
        </div>
      );
    } else {
      return (
        <div key={index} className="flex justify-start mb-4">
          <div className="bg-gray-200 rounded-lg py-2 px-4 max-w-md">
            <p className="whitespace-pre-wrap">{message.content}</p>
            
            {/* Suggested Action Button (if present) */}
            {message.suggestedActionId && (
              <button
                onClick={() => handleExecuteAction(message.suggestedActionId!)}
                className="mt-2 inline-flex items-center px-3 py-1 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                disabled={isLoading}
              >
                {isLoading ? 'Processing...' : 'Execute Suggested Action'}
              </button>
            )}
            
            <p className="text-xs text-gray-500 mt-1">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </p>
          </div>
        </div>
      );
    }
  };

  return (
    <div className="flex flex-col bg-white rounded-lg shadow">
      {/* Chat Messages */}
      <div className="flex-1 p-4 overflow-y-auto h-80 border border-gray-200 rounded-t-lg">
        {messages.map((message, index) => renderMessage(message, index))}
        
        {/* Loading indicator */}
        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-gray-200 rounded-lg py-2 px-4">
              <div className="flex space-x-2">
                <div className="bg-gray-500 rounded-full h-2 w-2 animate-bounce"></div>
                <div className="bg-gray-500 rounded-full h-2 w-2 animate-bounce delay-100"></div>
                <div className="bg-gray-500 rounded-full h-2 w-2 animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}
        
        {/* Error message */}
        {error && (
          <div className="flex justify-center mb-4">
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded-lg">
              {error}
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {/* Preset Questions */}
      {presetQuestions.length > 0 && (
        <div className="px-4 py-3 border-l border-r border-gray-200">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Quick Questions:</h4>
          <div className="flex flex-wrap gap-2">
            {presetQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => handlePresetQuestion(question)}
                className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700"
                disabled={isLoading}
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}
      
      {/* Message Input */}
      <div className="border border-gray-200 rounded-b-lg p-4">
        <div className="flex">
          <textarea
            className="flex-1 focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md resize-none"
            placeholder="Type your message..."
            rows={2}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
          />
          <button
            type="button"
            className="ml-3 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            onClick={handleSendMessage}
            disabled={isLoading || !inputMessage.trim()}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
