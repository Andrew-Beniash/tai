/**
 * AuthContext component
 * Provides authentication state and methods to login/logout
 */

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, login as apiLogin, logout as apiLogout, getCurrentUser } from '../api/auth';

// Define the shape of our auth context
interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

// Create the context with default values
const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  login: async () => {},
  logout: () => {},
});

// Custom hook to use the auth context
export function useAuth() {
  return useContext(AuthContext);
}

// Provider component to wrap our application
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Load user from localStorage on initial mount
  useEffect(() => {
    const loadUser = () => {
      const currentUser = getCurrentUser();
      setUser(currentUser);
      setLoading(false);
    };

    loadUser();
  }, []);

  // Login function
  const login = async (username: string, password: string) => {
    try {
      setLoading(true);
      const loggedInUser = await apiLogin(username, password);
      setUser(loggedInUser);
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = () => {
    apiLogout();
    setUser(null);
  };

  // Value object that will be provided to consumers
  const value = {
    user,
    loading,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
