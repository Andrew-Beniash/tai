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
  sender: 'user' | 'ai' | 'system';
  content: string;
  timestamp: Date;
  suggestedActionId?: string;
  actionResult?: {
    success: boolean;
    message: string;
    documentUrl?: string;
  };
}

export default function ChatWidget({ taskId }: ChatWidgetProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [presetQuestions, setPresetQuestions] = useState<string[]>([]);
  const [loadingQuestions, setLoadingQuestions] = useState(true);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  
  // Fetch preset questions when component mounts
  useEffect(() => {
    const fetchPresetQuestions = async () => {
      try {
        setLoadingQuestions(true);
        const questions = await getPresetQuestions(taskId);
        setPresetQuestions(questions);
      } catch (err) {
        console.error('Error fetching preset questions:', err);
      } finally {
        setLoadingQuestions(false);
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
      
      // Create a system message about the action result
      const systemMessage: ChatMessage = {
        sender: 'system',
        content: result.success 
          ? `✅ Action completed successfully: ${result.message}` 
          : `❌ Action failed: ${result.message}`,
        timestamp: new Date(),
        actionResult: {
          success: result.success,
          message: result.message,
          documentUrl: result.result?.documentUrl || result.result?.fileUrl
        }
      };
      
      setMessages(prev => [...prev, systemMessage]);
      
      if (!result.success) {
        setError(`Action failed: ${result.message}`);
      }
    } catch (err) {
      setError('Failed to execute action. Please try again.');
      console.error('Error executing action:', err);
      
      // Add error message to chat
      const errorMessage: ChatMessage = {
        sender: 'system',
        content: '❌ There was an error executing the action. Please try again.',
        timestamp: new Date(),
        actionResult: {
          success: false,
          message: 'Network or server error'
        }
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Function to render chat message based on type
  const renderMessage = (message: ChatMessage, index: number) => {
    // User message styling
    if (message.sender === 'user') {
      return (
        <div key={index} className="flex justify-end mb-4">
          <div className="bg-blue-600 text-white rounded-lg py-2 px-4 max-w-md">
            <p className="whitespace-pre-wrap">{message.content}</p>
            <p className="text-xs text-blue-200 mt-1 text-right">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </p>
          </div>
        </div>
      );
    }
    // System message styling (for action results)
    else if (message.sender === 'system') {
      return (
        <div key={index} className="flex justify-center mb-4">
          <div className={`rounded-lg py-2 px-4 max-w-md ${
            message.actionResult?.success 
              ? 'bg-green-100 border border-green-300 text-green-800' 
              : 'bg-red-100 border border-red-300 text-red-800'
          }`}>
            <p className="whitespace-pre-wrap">{message.content}</p>
            
            {/* Document link if available */}
            {message.actionResult?.documentUrl && (
              <a 
                href={message.actionResult.documentUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-2 inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-800"
              >
                <svg className="h-4 w-4 mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
                View Generated Document
              </a>
            )}
            
            <p className="text-xs text-gray-500 mt-1 text-right">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </p>
          </div>
        </div>
      );
    }
    // AI message styling
    else {
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
                {isLoading ? (
                  <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
                  </span>
                ) : (
                  <span className="flex items-center">
                    <svg className="mr-1.5 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    Execute Suggested Action
                  </span>
                )}
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
      <div 
        ref={chatContainerRef}
        className="flex-1 p-4 overflow-y-auto h-96 border border-gray-200 rounded-t-lg"
      >
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
        <div className="px-4 py-3 border-l border-r border-gray-200 bg-gray-50">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Quick Questions:</h4>
          <div className="flex flex-wrap gap-2">
            {presetQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => handlePresetQuestion(question)}
                className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700 transition duration-150 ease-in-out"
                disabled={isLoading}
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}
      
      {/* Message Input */}
      <div className="border border-gray-200 rounded-b-lg p-4 bg-white">
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
            className={`ml-3 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white ${
              isLoading || !inputMessage.trim() 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'
            }`}
            onClick={handleSendMessage}
            disabled={isLoading || !inputMessage.trim()}
          >
            {isLoading ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Sending...
              </span>
            ) : (
              'Send'
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
