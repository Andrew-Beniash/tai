/**
 * Document API client
 * Handles fetching documents and their contents from the backend
 */

import axios from 'axios';
import { getAuthToken } from '../utils/session';

// Define constants
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Define types
export interface Document {
  doc_id: string;
  file_name: string;
  file_type: string;
  last_modified: string;
  project_id: string;
  drive_file_id: string;
  description?: string;
  size_bytes?: number;
  web_view_link?: string;
}

/**
 * Get documents for a project
 * 
 * @param projectId - Project ID
 * @param sync - Whether to sync with Google Drive first (default: false)
 * @returns Promise with array of documents
 */
export const getProjectDocuments = async (projectId: string, sync: boolean = false): Promise<Document[]> => {
  try {
    const token = getAuthToken();
    const response = await axios.get<Document[]>(
      `${API_URL}/api/projects/${projectId}/documents${sync ? '?sync=true' : ''}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    
    return response.data;
  } catch (error) {
    console.error(`Error fetching documents for project ${projectId}:`, error);
    return [];
  }
};

/**
 * Get documents associated with a task
 * 
 * @param taskId - Task ID
 * @returns Promise with array of documents
 */
export const getTaskDocuments = async (taskId: string): Promise<Document[]> => {
  try {
    const token = getAuthToken();
    const response = await axios.get<Document[]>(
      `${API_URL}/api/tasks/${taskId}/documents`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    
    return response.data;
  } catch (error) {
    console.error(`Error fetching documents for task ${taskId}:`, error);
    return [];
  }
};

/**
 * Get document content as base64 for display
 * 
 * @param docId - Document ID
 * @returns Promise with document content and metadata
 */
export const getDocumentContent = async (docId: string): Promise<{
  content: string;
  mime_type: string;
  file_name: string;
  file_type: string;
  size_bytes: number;
}> => {
  try {
    const token = getAuthToken();
    const response = await axios.get(
      `${API_URL}/api/documents/${docId}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    
    return response.data;
  } catch (error) {
    console.error(`Error fetching content for document ${docId}:`, error);
    throw new Error('Failed to fetch document content');
  }
};

/**
 * Get document text content
 * 
 * @param docId - Document ID
 * @returns Promise with document text content
 */
export const getDocumentTextContent = async (docId: string): Promise<{ content: string; file_name: string }> => {
  try {
    const token = getAuthToken();
    const response = await axios.get(
      `${API_URL}/api/documents/${docId}?text_only=true`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    
    return response.data;
  } catch (error) {
    console.error(`Error fetching text content for document ${docId}:`, error);
    throw new Error('Failed to fetch document text content');
  }
};

/**
 * Get document download URL
 * 
 * @param docId - Document ID
 * @returns Download URL for the document
 */
export const getDocumentDownloadUrl = (docId: string): string => {
  const token = getAuthToken();
  return `${API_URL}/api/documents/${docId}?download=true&token=${token}`;
};

/**
 * Sync project documents with Google Drive
 * 
 * @param projectId - Project ID
 * @returns Promise with array of synced documents
 */
export const syncProjectDocuments = async (projectId: string): Promise<Document[]> => {
  try {
    const token = getAuthToken();
    const response = await axios.post<Document[]>(
      `${API_URL}/api/projects/${projectId}/documents/sync`,
      {},
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    
    return response.data;
  } catch (error) {
    console.error(`Error syncing documents for project ${projectId}:`, error);
    throw new Error('Failed to sync project documents');
  }
};
