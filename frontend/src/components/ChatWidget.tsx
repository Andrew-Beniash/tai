/**
 * ChatWidget component
 * Provides an interface for interacting with the AI assistant
 * Includes chat history, message input, and action handling
 */

import { useState, useEffect, useRef } from 'react';
import { sendChatMessage, ChatResponse, getPresetQuestions } from '../api/chat';
import { executeAction, ActionRequest, getAvailableActions, AvailableAction } from '../api/actions';
import ReactMarkdown from 'react-markdown';

interface ChatWidgetProps {
  taskId: string;
  onSuggestAction?: (actionId: string) => void;
}

interface ChatMessage {
  sender: 'user' | 'ai' | 'system';
  content: string;
  timestamp: Date;
  suggestedActionId?: string;
  suggestedActionName?: string;
  actionResult?: {
    success: boolean;
    message: string;
    documentUrl?: string;
  };
}

export default function ChatWidget({ taskId, onSuggestAction }: ChatWidgetProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [presetQuestions, setPresetQuestions] = useState<string[]>([]);
  const [loadingQuestions, setLoadingQuestions] = useState(true);
  const [availableActions, setAvailableActions] = useState<AvailableAction[]>([]);
  const [loadingAction, setLoadingAction] = useState(false);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
  
  // Fetch preset questions and available actions when component mounts
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        setLoadingQuestions(true);
        const [questions, actions] = await Promise.all([
          getPresetQuestions(taskId),
          getAvailableActions(taskId)
        ]);
        setPresetQuestions(questions);
        setAvailableActions(actions);
      } catch (err) {
        console.error('Error fetching initial data:', err);
      } finally {
        setLoadingQuestions(false);
      }
    };
    
    fetchInitialData();
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

  // Auto resize textarea based on content
  useEffect(() => {
    if (textAreaRef.current) {
      textAreaRef.current.style.height = 'auto';
      textAreaRef.current.style.height = textAreaRef.current.scrollHeight + 'px';
    }
  }, [inputMessage]);
  
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
      
      // Extract action name if present
      let actionName = 'Execute Suggested Action';
      if (response.suggestedActionId) {
        // Try to find action name from available actions first
        const actionInfo = availableActions.find(a => a.action_id === response.suggestedActionId);
        if (actionInfo) {
          actionName = actionInfo.action_name;
        } else {
          // Fall back to regex extraction
          const actionMatch = response.response.match(/\*\*Action:\s+([^*]+)\*\*/);
          if (actionMatch && actionMatch[1]) {
            actionName = actionMatch[1].trim();
          }
        }
        
        // Notify parent component if callback is provided
        if (onSuggestAction) {
          onSuggestAction(response.suggestedActionId);
        }
      }
      
      const aiMessage: ChatMessage = {
        sender: 'ai',
        content: response.response,
        timestamp: new Date(),
        suggestedActionId: response.suggestedActionId,
        suggestedActionName: actionName,
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
    setLoadingAction(true);
    setError(null);
    
    try {
      const actionRequest: ActionRequest = {
        action_id: actionId,
      };
      
      const result = await executeAction(taskId, actionRequest);
      
      // Find action details for better description
      const actionInfo = availableActions.find(a => a.action_id === actionId);
      const actionDescription = actionInfo ? actionInfo.description : '';
      
      // Create a system message about the action result
      const systemMessage: ChatMessage = {
        sender: 'system',
        content: result.success 
          ? `✅ Action completed successfully: ${actionDescription || result.message}` 
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

      // Notify parent component if callback is provided (to clear the standalone action buttons)
      if (onSuggestAction) {
        onSuggestAction(undefined);
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
      setLoadingAction(false);
    }
  };
  
  // Function to format timestamp
  const formatTimestamp = (date: Date) => {
    return date.toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: true
    });
  };
  
  // Function to render chat message based on type
  const renderMessage = (message: ChatMessage, index: number) => {
    // User message styling
    if (message.sender === 'user') {
      return (
        <div key={index} className="flex justify-end mb-4 animate-fadeIn">
          <div className="bg-blue-600 text-white rounded-lg py-2 px-4 max-w-3xl shadow">
            <p className="whitespace-pre-wrap break-words">{message.content}</p>
            <p className="text-xs text-blue-200 mt-1 text-right">
              {formatTimestamp(message.timestamp)}
            </p>
          </div>
        </div>
      );
    }
    // System message styling (for action results)
    else if (message.sender === 'system') {
      return (
        <div key={index} className="flex justify-center mb-4 animate-fadeIn">
          <div className={`rounded-lg py-2 px-4 max-w-3xl shadow ${
            message.actionResult?.success 
              ? 'bg-green-100 border border-green-300 text-green-800' 
              : 'bg-red-100 border border-red-300 text-red-800'
          }`}>
            <p className="whitespace-pre-wrap break-words">{message.content}</p>
            
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
              {formatTimestamp(message.timestamp)}
            </p>
          </div>
        </div>
      );
    }
    // AI message styling
    else {
      return (
        <div key={index} className="flex justify-start mb-4 animate-fadeIn">
          <div className="bg-gray-100 rounded-lg py-3 px-4 max-w-3xl shadow">
            <div className="prose prose-sm max-w-none">
              <ReactMarkdown>
                {message.content}
              </ReactMarkdown>
            </div>
            
            {/* Enhanced Suggested Action Button (if present) */}
            {message.suggestedActionId && (
              <div className="mt-3 border-t border-gray-200 pt-3">
                <div className="flex flex-col space-y-2">
                  <h4 className="text-sm font-medium text-gray-700">Suggested Action:</h4>
                  
                  {/* Action details */}
                  {availableActions.length > 0 && message.suggestedActionId && (
                    <div className="text-sm text-gray-600 mb-2">
                      {availableActions.find(action => action.action_id === message.suggestedActionId)?.description || 
                        "This action can be executed to address the current task."}
                    </div>
                  )}
                  
                  <button
                    onClick={() => handleExecuteAction(message.suggestedActionId!)}
                    className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 shadow-sm transition-colors duration-150"
                    disabled={loadingAction}
                  >
                    {loadingAction ? (
                      <span className="flex items-center">
                        <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Processing Action...
                      </span>
                    ) : (
                      <span className="flex items-center">
                        <svg className="mr-1.5 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        {message.suggestedActionName || "Execute Suggested Action"}
                      </span>
                    )}
                  </button>
                </div>
              </div>
            )}
            
            <p className="text-xs text-gray-500 mt-2 text-right">
              {formatTimestamp(message.timestamp)}
            </p>
          </div>
        </div>
      );
    }
  };

  // Group preset questions by category for better organization
  const questionCategories = {
    'Information': [
      'List missing information for filing.',
      'Summarize prior year notes.',
      'Generate additional questions to client'
    ],
    'Review': [
      'Review prepared forms',
      'Check calculation for the forms',
      'What are the risks based on prior year financials?'
    ],
    'Analysis': [
      'Explain calculation and tax considerations',
      'What tax changes should we consider?',
      'Summarize important filing deadlines'
    ]
  };

  // Filter preset questions that match our categories
  const categorizedQuestions = () => {
    const result: Record<string, string[]> = {};
    
    for (const [category, questions] of Object.entries(questionCategories)) {
      result[category] = questions.filter(q => 
        presetQuestions.some(pq => pq.includes(q) || q.includes(pq))
      );
      
      // If we don't have any matches in our predefined list, add some from the fetched list
      if (result[category].length === 0 && presetQuestions.length > 0) {
        // Distribute available questions across categories
        const index = Object.keys(questionCategories).indexOf(category);
        const questionsPerCategory = Math.ceil(presetQuestions.length / Object.keys(questionCategories).length);
        const start = index * questionsPerCategory;
        const end = Math.min(start + questionsPerCategory, presetQuestions.length);
        
        result[category] = presetQuestions.slice(start, end);
      }
    }
    
    return result;
  };

  return (
    <div className="flex flex-col bg-white rounded-lg shadow">
      {/* Chat Messages */}
      <div 
        ref={chatContainerRef}
        className="flex-1 p-4 overflow-y-auto h-[500px] border border-gray-200 rounded-t-lg bg-gray-50"
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
      
      {/* Enhanced Preset Questions UI */}
      {!loadingQuestions && (
        <div className="px-4 py-3 border-l border-r border-gray-200 bg-gray-50">
          <h4 className="text-sm font-medium text-gray-700 mb-3">Quick Questions:</h4>
          
          {/* Categorized Questions */}
          <div className="space-y-3">
            {Object.entries(categorizedQuestions()).map(([category, questions]) => (
              questions.length > 0 && (
                <div key={category} className="space-y-2">
                  <h5 className="text-xs font-medium text-gray-500">{category}</h5>
                  <div className="flex flex-wrap gap-2">
                    {questions.map((question, index) => (
                      <button
                        key={index}
                        onClick={() => handlePresetQuestion(question)}
                        className="px-3 py-1.5 bg-white hover:bg-gray-100 border border-gray-300 rounded-full text-sm text-gray-700 transition duration-150 ease-in-out shadow-sm hover:shadow flex items-center"
                        disabled={isLoading}
                      >
                        {getQuestionIcon(category)}
                        <span>{question}</span>
                      </button>
                    ))}
                  </div>
                </div>
              )
            ))}
          </div>
        </div>
      )}
      
      {/* Message Input */}
      <div className="border border-gray-200 rounded-b-lg p-4 bg-white">
        <div className="flex">
          <textarea
            ref={textAreaRef}
            className="flex-1 focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md resize-none min-h-[50px]"
            placeholder="Type your message..."
            rows={1}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading || loadingAction}
          />
          <button
            type="button"
            className={`ml-3 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white ${
              isLoading || loadingAction || !inputMessage.trim() 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'
            }`}
            onClick={handleSendMessage}
            disabled={isLoading || loadingAction || !inputMessage.trim()}
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
              <span className="flex items-center">
                <svg className="mr-1.5 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
                Send
              </span>
            )}
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Press Shift+Enter for a new line, Enter to send
        </p>
      </div>
    </div>
  );
}

// Helper function to get an appropriate icon based on question category
function getQuestionIcon(category: string) {
  switch (category) {
    case 'Information':
      return (
        <svg className="w-4 h-4 mr-1.5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      );
    case 'Review':
      return (
        <svg className="w-4 h-4 mr-1.5 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      );
    case 'Analysis':
      return (
        <svg className="w-4 h-4 mr-1.5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      );
    default:
      return (
        <svg className="w-4 h-4 mr-1.5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      );
  }
}