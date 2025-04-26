/**
 * Session utility functions
 * Helper functions for session management in the frontend
 */

import { User } from '../api/auth';

// Constants for localStorage keys
const USER_KEY = 'user';
const TOKEN_KEY = 'token';

/**
 * Save user to localStorage
 * 
 * @param user User object to save
 */
export const saveUser = (user: User): void => {
  localStorage.setItem(USER_KEY, JSON.stringify(user));
};

/**
 * Get user from localStorage
 * 
 * @returns User object or null if not found
 */
export const getUser = (): User | null => {
  const userJson = localStorage.getItem(USER_KEY);
  return userJson ? JSON.parse(userJson) : null;
};

/**
 * Save token to localStorage
 * 
 * @param token JWT token to save
 */
export const saveToken = (token: string): void => {
  localStorage.setItem(TOKEN_KEY, token);
};

/**
 * Get token from localStorage
 * 
 * @returns JWT token or null if not found
 */
export const getToken = (): string | null => {
  return localStorage.getItem(TOKEN_KEY);
};

/**
 * Clear all session data from localStorage
 */
export const clearSession = (): void => {
  localStorage.removeItem(USER_KEY);
  localStorage.removeItem(TOKEN_KEY);
};

/**
 * Check if user is authenticated
 * 
 * @returns True if user is authenticated, false otherwise
 */
export const isAuthenticated = (): boolean => {
  return !!getUser();
};

/**
 * Get authentication headers for API requests
 * 
 * @returns Headers object with Authorization header if token exists
 */
export const getAuthHeaders = (): Record<string, string> => {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
};
