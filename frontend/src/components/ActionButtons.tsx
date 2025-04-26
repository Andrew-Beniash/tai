/**
 * ActionButtons component
 * Displays and handles AI-suggested actions for a task
 */

import { useState, useEffect } from 'react';
import { AvailableAction, executeAction, getAvailableActions } from '../api/actions';

interface ActionButtonsProps {
  taskId: string;
  suggestedActionId?: string;
  onActionComplete: (success: boolean, message: string, result?: Record<string, any>) => void;
}

export default function ActionButtons({ taskId, suggestedActionId, onActionComplete }: ActionButtonsProps) {
  const [availableActions, setAvailableActions] = useState<AvailableAction[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Fetch available actions when component mounts or suggestedActionId changes
  useEffect(() => {
    const fetchAvailableActions = async () => {
      try {
        const actions = await getAvailableActions(taskId);
        setAvailableActions(actions);
      } catch (err) {
        console.error('Error fetching available actions:', err);
      }
    };
    
    fetchAvailableActions();
  }, [taskId, suggestedActionId]);
  
  // Execute the suggested action
  const handleExecuteAction = async (actionId: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await executeAction(taskId, { action_id: actionId });
      
      if (result.success) {
        onActionComplete(true, result.message, result.result);
      } else {
        setError(`Action failed: ${result.message}`);
        onActionComplete(false, result.message);
      }
    } catch (err) {
      const errorMessage = 'Failed to execute action. Please try again.';
      setError(errorMessage);
      onActionComplete(false, errorMessage);
      console.error('Error executing action:', err);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Find the current suggested action from available actions
  const suggestedAction = availableActions.find(action => action.action_id === suggestedActionId);
  
  // If there's no suggested action, or we couldn't find it, don't render anything
  if (!suggestedActionId || !suggestedAction) {
    return null;
  }
  
  return (
    <div className="mt-4">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded-lg mb-4">
          {error}
        </div>
      )}
      
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Suggested Action:</h4>
        <div className="mb-3">
          <p className="text-sm text-gray-600">{suggestedAction.description}</p>
          
          {/* Optional parameter inputs would go here if we had them */}
        </div>
        
        <div className="flex justify-end">
          <button
            onClick={() => handleExecuteAction(suggestedAction.action_id)}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors duration-150"
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
                Execute: {suggestedAction.action_name}
              </span>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
