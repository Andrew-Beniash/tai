import axios from 'axios';
import { getAuthToken } from '../utils/session';

// Define constants
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Define types
export interface ActionRequest {
  action_id: string;
  params?: Record<string, any>;
}

export interface ActionResponse {
  success: boolean;
  message: string;
  result?: Record<string, any>;
}

export interface AvailableAction {
  action_id: string;
  action_name: string;
  description: string;
  function_path: string;
  required_params: string[];
}

/**
 * Execute an action for a specific task
 * 
 * @param taskId - ID of the task to execute action for
 * @param actionRequest - Action details including action_id and parameters
 * @returns Promise with the action execution result
 */
export const executeAction = async (taskId: string, actionRequest: ActionRequest): Promise<ActionResponse> => {
  try {
    const token = getAuthToken();
    const response = await axios.post<ActionResponse>(
      `${API_URL}/api/task/${taskId}/action`,
      actionRequest,
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      }
    );
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      console.error('Error executing action:', error.response.data);
      return {
        success: false,
        message: error.response.data.detail || 'Failed to execute action'
      };
    }
    console.error('Error executing action:', error);
    return {
      success: false,
      message: 'Failed to execute action due to network error'
    };
  }
};

/**
 * Get available actions for a specific task
 * 
 * @param taskId - ID of the task to get available actions for
 * @returns Promise with list of available actions
 */
export const getAvailableActions = async (taskId: string): Promise<AvailableAction[]> => {
  try {
    const token = getAuthToken();
    const response = await axios.get<{ actions: AvailableAction[] }>(
      `${API_URL}/api/task/${taskId}/available-actions`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    return response.data.actions;
  } catch (error) {
    console.error('Error getting available actions:', error);
    return [];
  }
};
