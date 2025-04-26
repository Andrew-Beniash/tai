/**
 * Authentication API client module
 * Handles user login/logout and session management
 */

import axios from 'axios';
import { saveCurrentUser, getCurrentUser as getStoredUser, clearCurrentUser, saveAuthToken, clearAuthToken } from '../utils/session';

// Get API URL from environment or use default
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * User interface representing a logged-in user
 */
export interface User {
  id: string;
  name: string;
  role: string;
}

/**
 * Login response interface
 */
interface LoginResponse {
  access_token: string;
  token_type: string;
}

/**
 * Login with username and password
 * 
 * @param username User's username (jeff or hanna)
 * @param password User's password
 * @returns Promise resolving to the logged in user
 */
export async function login(username: string, password: string): Promise<User> {
  try {
    // For the prototype, we're using hardcoded users
    // In a real app, this would validate against backend API
    
    // Check if username is one of our hardcoded users
    if (username !== 'jeff' && username !== 'hanna') {
      throw new Error('Invalid credentials. Use "jeff" or "hanna" for username.');
    }
    
    // Check if password is correct (in real app, this would be handled securely)
    if (password !== 'password') {
      throw new Error('Invalid password. Use "password" for the prototype.');
    }
    
    // Simulate API call to get token
    // In a production app, we would actually make this request
    /*
    const response = await axios.post<LoginResponse>(`${API_URL}/api/login`, {
      username,
      password,
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      }
    });
    
    const { access_token } = response.data;
    saveAuthToken(access_token);
    */
    
    // For the prototype, store a dummy token
    saveAuthToken('prototype_auth_token');
    
    // Create a mock user based on username
    const user: User = {
      id: username,
      name: username === 'jeff' ? 'Jeff' : 'Hanna',
      role: username === 'jeff' ? 'Preparer' : 'Reviewer',
    };
    
    // Store user in localStorage for session management
    saveCurrentUser(user);
    
    return user;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
}

/**
 * Get the current logged-in user from localStorage
 * 
 * @returns The current user or null if not logged in
 */
export function getCurrentUser(): User | null {
  return getStoredUser();
}

/**
 * Logout the current user by clearing localStorage
 */
export function logout(): void {
  clearCurrentUser();
  clearAuthToken();
}

/**
 * Check if the user is logged in
 * 
 * @returns True if the user is logged in, false otherwise
 */
export function isLoggedIn(): boolean {
  return !!getCurrentUser();
}
