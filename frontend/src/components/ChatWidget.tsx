import React, { useState, useEffect, useRef } from 'react';
import ActionButtons from './ActionButtons';

interface Message {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
  suggestedActionId?: string;
}

interface ChatWidgetProps {
  taskId: string;
  onSendMessage: (message: string) => Promise<{
    response: string;
    suggestedActionId?: string;
  }>;
  presetQuestions?: string[];
}

/**
 * Chat widget component that allows users to interact with AI assistant
 * Supports text input, preset questions, and executing suggested actions
 */
const ChatWidget: React.FC<ChatWidgetProps> = ({ 
  taskId, 
  onSendMessage,
  presetQuestions = []
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentActionId, setCurrentActionId] = useState<string | undefined>();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Scroll to bottom of chat whenever messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return;
    
    // Add user message to chat
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    
    try {
      // Send message to backend
      const { response, suggestedActionId } = await onSendMessage(content);
      
      // Add AI response to chat
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: response,
        timestamp: new Date(),
        suggestedActionId
      };
      
      setMessages(prev => [...prev, aiMessage]);
      
      // If AI suggests an action, set it as the current action
      if (suggestedActionId) {
        setCurrentActionId(suggestedActionId);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: 'Sorry, there was an error processing your request. Please try again.',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(inputValue);
    }
  };
  
  const handleActionComplete = (result: any) => {
    // Add message about completed action
    const actionMessage: Message = {
      id: Date.now().toString(),
      type: 'ai',
      content: `Action completed successfully! ${result?.documentUrl ? `Generated document: ${result.documentUrl}` : ''}`,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, actionMessage]);
    setCurrentActionId(undefined);
  };
  
  return (
    <div className="flex flex-col h-full border rounded-lg shadow-sm bg-white">
      {/* Chat header */}
      <div className="p-3 border-b bg-gray-50">
        <h2 className="text-lg font-semibold">AI Assistant - Task #{taskId}</h2>
      </div>
      
      {/* Messages container */}
      <div className="flex-1 p-4 overflow-y-auto">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 my-4">
            Ask a question about this task or use one of the preset questions below.
          </div>
        ) : (
          messages.map(message => (
            <div 
              key={message.id} 
              className={`mb-4 ${message.type === 'user' ? 'text-right' : 'text-left'}`}
            >
              <div 
                className={`inline-block p-3 rounded-lg ${
                  message.type === 'user' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                {message.content}
              </div>
              <div className="text-xs text-gray-500 mt-1">
                {message.timestamp.toLocaleTimeString()}
              </div>
              
              {/* Show action buttons if this message has a suggested action */}
              {message.type === 'ai' && message.suggestedActionId && (
                <div className="mt-2">
                  <ActionButtons 
                    taskId={taskId}
                    suggestedActionId={message.suggestedActionId}
                    onActionComplete={handleActionComplete}
                  />
                </div>
              )}
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Preset questions */}
      {presetQuestions.length > 0 && (
        <div className="p-3 border-t bg-gray-50">
          <div className="flex flex-wrap gap-2">
            {presetQuestions.map((question, index) => (
              <button
                key={index}
                className="px-2 py-1 bg-gray-200 hover:bg-gray-300 rounded text-sm"
                onClick={() => handleSendMessage(question)}
                disabled={isLoading}
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}
      
      {/* Input area */}
      <div className="p-3 border-t">
        <div className="flex">
          <textarea
            className="flex-1 p-2 border rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Type your message..."
            value={inputValue}
            onChange={e => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
            rows={2}
          />
          <button
            className="px-4 py-2 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            onClick={() => handleSendMessage(inputValue)}
            disabled={isLoading || !inputValue.trim()}
          >
            {isLoading ? '...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatWidget;
