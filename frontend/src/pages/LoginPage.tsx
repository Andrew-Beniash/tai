/**
 * LoginPage component
 * Provides a user interface for logging in as Jeff or Hanna
 * Allows easy switching between users with clear role identification
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleUserSelect = async (user: 'jeff' | 'hanna') => {
    try {
      setError('');
      setLoading(true);
      await login(user, 'password');
      
      // Redirect to projects page after successful login
      navigate('/projects');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="max-w-md w-full space-y-8 p-10 bg-white rounded-xl shadow-lg">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-bold text-gray-900">
            AI-Augmented Tax Engagement
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Prototype User Selector
          </p>
        </div>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <span className="block sm:inline">{error}</span>
          </div>
        )}
        
        <div className="my-8">
          <p className="text-sm text-gray-500 mb-4 text-center">
            This prototype simulates two different user roles in the tax engagement process.
            Select a user to begin exploring the application.
          </p>
        </div>
        
        <div className="space-y-4">
          <button
            onClick={() => handleUserSelect('jeff')}
            disabled={loading}
            className="w-full flex items-center p-4 border border-gray-200 rounded-lg shadow-sm hover:bg-blue-50 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <div className="bg-blue-100 text-blue-800 font-bold rounded-full h-12 w-12 flex items-center justify-center text-xl">
              J
            </div>
            <div className="ml-4 text-left">
              <p className="text-lg font-medium text-gray-900">Jeff</p>
              <p className="text-sm text-gray-500">Tax Preparer</p>
              <p className="text-xs text-gray-400 mt-1">Responsible for preparing tax forms and gathering client information</p>
            </div>
          </button>
          
          <button
            onClick={() => handleUserSelect('hanna')}
            disabled={loading}
            className="w-full flex items-center p-4 border border-gray-200 rounded-lg shadow-sm hover:bg-purple-50 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
          >
            <div className="bg-purple-100 text-purple-800 font-bold rounded-full h-12 w-12 flex items-center justify-center text-xl">
              H
            </div>
            <div className="ml-4 text-left">
              <p className="text-lg font-medium text-gray-900">Hanna</p>
              <p className="text-sm text-gray-500">Tax Reviewer</p>
              <p className="text-xs text-gray-400 mt-1">Responsible for reviewing prepared tax forms and ensuring compliance</p>
            </div>
          </button>
        </div>
        
        {loading && (
          <div className="mt-4 text-center text-sm text-gray-500">
            Logging in...
          </div>
        )}
        
        <div className="mt-6 pt-4 border-t border-gray-200">
          <p className="text-xs text-gray-500 text-center">
            Note: This is a prototype application with simulated authentication.
            Your session will be stored in your browser's localStorage.
          </p>
        </div>
      </div>
    </div>
  );
}
