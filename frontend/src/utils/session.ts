/**
 * Session utilities for managing user authentication
 */

import { User } from '../api/auth';

// Local storage keys
const TOKEN_KEY = 'ai_tax_auth_token';
const USER_KEY = 'ai_tax_current_user';

/**
 * Save authentication token to local storage
 * 
 * @param token - JWT token from login response
 */
export const saveAuthToken = (token: string): void => {
  localStorage.setItem(TOKEN_KEY, token);
};

/**
 * Get authentication token from local storage
 * 
 * @returns Stored token or empty string if not found
 */
export const getAuthToken = (): string => {
  return localStorage.getItem(TOKEN_KEY) || '';
};

/**
 * Clear authentication token from local storage
 */
export const clearAuthToken = (): void => {
  localStorage.removeItem(TOKEN_KEY);
};

/**
 * Save current user info to local storage
 * 
 * @param user - User object from login response
 */
export const saveCurrentUser = (user: any): void => {
  localStorage.setItem(USER_KEY, JSON.stringify(user));
};

/**
 * Get current user info from local storage
 * 
 * @returns Stored user object or null if not found
 */
export const getCurrentUser = (): any => {
  const userJson = localStorage.getItem(USER_KEY);
  return userJson ? JSON.parse(userJson) : null;
};

/**
 * Clear current user info from local storage
 */
export const clearCurrentUser = (): void => {
  localStorage.removeItem(USER_KEY);
};

/**
 * Check if user is logged in
 * 
 * @returns Boolean indicating whether user is logged in
 */
export const isLoggedIn = (): boolean => {
  return !!getAuthToken() && !!getCurrentUser();
};

/**
 * Logout user by clearing all session data
 */
export const logout = (): void => {
  clearAuthToken();
  clearCurrentUser();
};

/**
 * Switch user by directly setting a new user in localStorage
 * This is a simplified approach for the prototype that skips the login API call
 * 
 * @param username - 'jeff' or 'hanna'
 * @returns User object for the newly logged in user
 */
export const switchUser = (username: 'jeff' | 'hanna'): User => {
  // Create a user object based on the selected username
  const user: User = {
    id: username,
    name: username === 'jeff' ? 'Jeff' : 'Hanna',
    role: username === 'jeff' ? 'Preparer' : 'Reviewer',
  };
  
  // Store user in localStorage
  saveCurrentUser(user);
  
  // Set a dummy token to indicate authenticated state
  saveAuthToken('prototype_token');
  
  return user;
};
