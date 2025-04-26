import React, { useState, useEffect } from 'react';
import { AvailableAction, executeAction, getAvailableActions } from '../api/actions';

interface ActionButtonsProps {
  taskId: string;
  onActionComplete: (result: any) => void;
  suggestedActionId?: string; // Optional, for when AI suggests a specific action
}

/**
 * Component that displays buttons for available actions on a task
 * Allows user to execute actions recommended by the AI
 */
const ActionButtons: React.FC<ActionButtonsProps> = ({ 
  taskId, 
  onActionComplete,
  suggestedActionId 
}) => {
  const [availableActions, setAvailableActions] = useState<AvailableAction[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [executing, setExecuting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Load available actions when component mounts or taskId changes
  useEffect(() => {
    if (taskId) {
      fetchAvailableActions();
    }
  }, [taskId]);

  const fetchAvailableActions = async () => {
    setLoading(true);
    setError(null);
    try {
      const actions = await getAvailableActions(taskId);
      setAvailableActions(actions);
    } catch (err) {
      setError('Failed to load available actions');
      console.error('Error loading actions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExecuteAction = async (actionId: string) => {
    setExecuting(true);
    setError(null);
    try {
      // For demo, using empty params - in a real app, you'd collect required params
      const actionResult = await executeAction(taskId, {
        action_id: actionId
      });
      
      if (actionResult.success) {
        onActionComplete(actionResult.result);
      } else {
        setError(actionResult.message);
      }
    } catch (err) {
      setError('Failed to execute action');
      console.error('Error executing action:', err);
    } finally {
      setExecuting(false);
    }
  };

  // Highlight suggested action, if provided
  const getButtonClassName = (actionId: string) => {
    const baseClass = "px-4 py-2 rounded text-white font-medium transition-colors";
    if (suggestedActionId === actionId) {
      return `${baseClass} bg-green-600 hover:bg-green-700 border-2 border-green-400`;
    }
    return `${baseClass} bg-blue-600 hover:bg-blue-700`;
  };

  if (loading) {
    return <div className="text-center">Loading actions...</div>;
  }

  if (error) {
    return (
      <div className="text-red-500 p-2 rounded bg-red-50 border border-red-200">
        Error: {error}
        <button 
          className="ml-2 text-blue-500 underline" 
          onClick={fetchAvailableActions}
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="my-4">
      <h3 className="text-lg font-semibold mb-2">
        {suggestedActionId ? 'Suggested Action:' : 'Available Actions:'}
      </h3>
      
      <div className="flex flex-wrap gap-2">
        {availableActions.map(action => (
          <button
            key={action.action_id}
            className={getButtonClassName(action.action_id)}
            onClick={() => handleExecuteAction(action.action_id)}
            disabled={executing}
            title={action.description}
          >
            {action.action_name}
            {executing && action.action_id === suggestedActionId && (
              <span className="ml-2">...</span>
            )}
          </button>
        ))}
      </div>
      
      {executing && (
        <div className="mt-2 text-gray-600">Executing action, please wait...</div>
      )}
    </div>
  );
};

export default ActionButtons;
