/**
 * useActions hook
 * Custom hook for managing AI-recommended actions in the task context
 */

import { useState, useCallback } from 'react';
import { AvailableAction, executeAction, getAvailableActions } from '../api/actions';

interface ActionExecutionResult {
  success: boolean;
  message: string;
  result?: Record<string, any>;
}

interface UseActionsReturn {
  suggestedActionId: string | undefined;
  setSuggestedActionId: (actionId: string | undefined) => void;
  availableActions: AvailableAction[];
  isLoadingActions: boolean;
  executeActionById: (actionId: string) => Promise<ActionExecutionResult>;
  refreshActions: (taskId: string) => Promise<void>;
}

export default function useActions(taskId: string): UseActionsReturn {
  const [suggestedActionId, setSuggestedActionId] = useState<string | undefined>(undefined);
  const [availableActions, setAvailableActions] = useState<AvailableAction[]>([]);
  const [isLoadingActions, setIsLoadingActions] = useState(false);

  // Fetch available actions for a task
  const refreshActions = useCallback(async (taskId: string) => {
    try {
      setIsLoadingActions(true);
      const actions = await getAvailableActions(taskId);
      setAvailableActions(actions);
    } catch (error) {
      console.error('Error fetching available actions:', error);
    } finally {
      setIsLoadingActions(false);
    }
  }, []);

  // Execute an action by ID
  const executeActionById = useCallback(async (actionId: string): Promise<ActionExecutionResult> => {
    try {
      setIsLoadingActions(true);
      const result = await executeAction(taskId, { action_id: actionId });
      return {
        success: result.success,
        message: result.message,
        result: result.result
      };
    } catch (error) {
      console.error('Error executing action:', error);
      return {
        success: false,
        message: 'Failed to execute action due to an error'
      };
    } finally {
      setIsLoadingActions(false);
      // After action execution, clear the suggested action ID
      setSuggestedActionId(undefined);
    }
  }, [taskId]);

  return {
    suggestedActionId,
    setSuggestedActionId,
    availableActions,
    isLoadingActions,
    executeActionById,
    refreshActions
  };
}
