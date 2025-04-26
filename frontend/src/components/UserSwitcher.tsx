/**
 * UserSwitcher component
 * Provides a dropdown menu to switch between Jeff and Hanna user roles
 * Can be placed in the application header or sidebar
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { User } from '../api/auth';

export default function UserSwitcher() {
  const [isOpen, setIsOpen] = useState(false);
  const { user, login } = useAuth();
  const navigate = useNavigate();

  // Handle user selection
  const handleUserSelect = async (username: 'jeff' | 'hanna') => {
    try {
      // Only switch if selecting a different user
      if (user?.id !== username) {
        await login(username, 'password');
        // Redirect to projects page after switching
        navigate('/projects');
      }
      // Close the dropdown
      setIsOpen(false);
    } catch (error) {
      console.error('Failed to switch user:', error);
    }
  };

  // Helper function to get user avatar based on user id
  const getUserAvatar = (user: User | null) => {
    if (!user) return null;
    
    const initial = user.name.charAt(0).toUpperCase();
    const bgColor = user.id === 'jeff' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800';
    
    return (
      <div className={`${bgColor} font-bold rounded-full h-8 w-8 flex items-center justify-center text-sm`}>
        {initial}
      </div>
    );
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 text-sm font-medium text-gray-700 hover:text-gray-900 focus:outline-none"
      >
        {getUserAvatar(user)}
        <span className="hidden md:inline">{user?.name}</span>
        <svg className="h-5 w-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
          <path
            fillRule="evenodd"
            d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
            clipRule="evenodd"
          />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50">
          <div className="py-1" role="menu" aria-orientation="vertical">
            <div className="px-4 py-2 text-sm text-gray-500 border-b border-gray-100">
              Switch User
            </div>
            
            <button
              onClick={() => handleUserSelect('jeff')}
              className={`${
                user?.id === 'jeff' ? 'bg-gray-100' : ''
              } flex items-center w-full px-4 py-2 text-sm text-left text-gray-700 hover:bg-gray-50`}
              role="menuitem"
            >
              <div className="bg-blue-100 text-blue-800 font-bold rounded-full h-6 w-6 flex items-center justify-center text-sm mr-2">
                J
              </div>
              <div>
                <p className="font-medium">Jeff</p>
                <p className="text-xs text-gray-500">Preparer</p>
              </div>
            </button>
            
            <button
              onClick={() => handleUserSelect('hanna')}
              className={`${
                user?.id === 'hanna' ? 'bg-gray-100' : ''
              } flex items-center w-full px-4 py-2 text-sm text-left text-gray-700 hover:bg-gray-50`}
              role="menuitem"
            >
              <div className="bg-purple-100 text-purple-800 font-bold rounded-full h-6 w-6 flex items-center justify-center text-sm mr-2">
                H
              </div>
              <div>
                <p className="font-medium">Hanna</p>
                <p className="text-xs text-gray-500">Reviewer</p>
              </div>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
