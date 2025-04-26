/**
 * Projects API client module
 * Handles fetching project data from the backend
 */

import axios from 'axios';
import { getAuthToken } from '../utils/session';

// Define constants
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Define types
export interface Project {
  project_id: string;
  name: string;
  clients: string[];
  services: string[];
  documents: string[];
  tasks: string[];
}

/**
 * Get a list of all projects
 * 
 * @returns Promise with array of projects
 */
export const getProjects = async (): Promise<Project[]> => {
  try {
    const token = getAuthToken();
    const response = await axios.get<{ projects: Project[] }>(
      `${API_URL}/api/projects`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    
    return response.data.projects;
  } catch (error) {
    console.error('Error fetching projects:', error);
    return [];
  }
};

/**
 * Get details for a specific project
 * 
 * @param projectId - ID of the project to fetch
 * @returns Promise with project details
 */
export const getProject = async (projectId: string): Promise<Project> => {
  try {
    const token = getAuthToken();
    const response = await axios.get<Project>(
      `${API_URL}/api/project/${projectId}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    
    return response.data;
  } catch (error) {
    console.error(`Error fetching project ${projectId}:`, error);
    throw new Error('Failed to fetch project details');
  }
};
