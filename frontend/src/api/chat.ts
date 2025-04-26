import axios from 'axios';
import { getAuthToken } from '../utils/session';

// Define constants
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Define types
export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  response: string;
  suggestedActionId?: string;
  documentIds?: string[];
}

/**
 * Send a message to the AI chat for a specific task
 * 
 * @param taskId - ID of the task to send chat message for
 * @param message - User's message to send to the AI
 * @returns Promise with the AI's response
 */
export const sendChatMessage = async (taskId: string, message: string): Promise<ChatResponse> => {
  try {
    const token = getAuthToken();
    const response = await axios.post<ChatResponse>(
      `${API_URL}/api/task/${taskId}/chat`,
      { message } as ChatRequest,
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
      console.error('Error sending chat message:', error.response.data);
      throw new Error(error.response.data.detail || 'Failed to send message');
    }
    console.error('Error sending chat message:', error);
    throw new Error('Failed to send message due to network error');
  }
};

/**
 * Get preset questions for a specific task type
 * 
 * @param taskId - ID of the task to get preset questions for
 * @returns Array of preset question strings
 */
export const getPresetQuestions = async (taskId: string): Promise<string[]> => {
  try {
    const token = getAuthToken();
    const response = await axios.get<{ questions: string[] }>(
      `${API_URL}/api/task/${taskId}/preset-questions`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    return response.data.questions;
  } catch (error) {
    console.error('Error getting preset questions:', error);
    // Return default preset questions in case of error
    return [
      "What are the risks based on prior year financials?",
      "List missing information for filing.",
      "Review prepared forms",
      "Check calculation for the forms",
      "Explain calculation and tax considerations",
      "Generate additional questions to client"
    ];
  }
};
