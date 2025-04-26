/**
 * ActionButtons component
 * Displays and handles AI-suggested actions for a task
 */

import { useState, useEffect } from 'react';
import { AvailableAction, executeAction } from '../api/actions';

interface ActionButtonsProps {
  taskId: string;
  suggestedActionId?: string;
  onActionComplete: (success: boolean, message: string) => void;
}

export default function ActionButtons({ taskId, suggestedActionId, onActionComplete }: ActionButtonsProps) {
  const [availableActions, setAvailableActions] = useState<AvailableAction[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Execute the suggested action
  const handleExecuteAction = async (actionId: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await executeAction(taskId, { action_id: actionId });
      
      if (result.success) {
        onActionComplete(true, result.message);
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
        </div>
        <button
          onClick={() => handleExecuteAction(suggestedAction.action_id)}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
          disabled={isLoading}
        >
          {isLoading ? 'Processing...' : `Execute: ${suggestedAction.action_name}`}
        </button>
      </div>
    </div>
  );
}
