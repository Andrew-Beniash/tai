import axios from 'axios';
import { getAuthToken } from '../utils/session';

// Define constants
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Define types
export interface Task {
  task_id: string;
  assigned_to: string;
  client: string;
  tax_form: string;
  status: string;
  priority: string;
  due_date: string;
  description: string;
  project_id: string;
  documents: any[];
}

/**
 * Get a list of tasks for the current user
 * 
 * @param projectId - Optional project ID to filter tasks
 * @returns Promise with array of tasks
 */
export const getTasks = async (projectId?: string): Promise<Task[]> => {
  try {
    const token = getAuthToken();
    let url = `${API_URL}/api/tasks`;
    
    // Add project filter if provided
    if (projectId) {
      url += `?project_id=${projectId}`;
    }
    
    const response = await axios.get<{ tasks: Task[] }>(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    return response.data.tasks;
  } catch (error) {
    console.error('Error fetching tasks:', error);
    return [];
  }
};

/**
 * Get details for a specific task
 * 
 * @param taskId - ID of the task to fetch
 * @returns Promise with task details
 */
export const getTask = async (taskId: string): Promise<Task> => {
  try {
    const token = getAuthToken();
    const response = await axios.get<Task>(
      `${API_URL}/api/task/${taskId}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    
    return response.data;
  } catch (error) {
    console.error(`Error fetching task ${taskId}:`, error);
    throw new Error('Failed to fetch task details');
  }
};
