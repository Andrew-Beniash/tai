/**
 * Navbar component
 * Provides navigation and user switcher functionality
 */

import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import UserSwitcher from './UserSwitcher';

export default function Navbar() {
  const { user, logout } = useAuth();
  const location = useLocation();
  
  // Don't render navbar on the login page
  if (location.pathname === '/login') {
    return null;
  }
  
  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <span className="text-xl font-semibold text-blue-600">AI Tax Assistant</span>
            </div>
            
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              <Link
                to="/projects"
                className={`${
                  location.pathname === '/projects'
                    ? 'border-blue-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
              >
                Projects
              </Link>
              
              <Link
                to="/tasks"
                className={`${
                  location.pathname === '/tasks' || location.pathname.startsWith('/tasks/')
                    ? 'border-blue-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
              >
                Tasks
              </Link>
            </div>
          </div>
          
          <div className="hidden sm:ml-6 sm:flex sm:items-center">
            {user && (
              <div className="flex items-center space-x-4">
                <div className="text-xs text-gray-500">
                  Logged in as: <span className="font-medium">{user.name}</span> ({user.role})
                </div>
                
                <UserSwitcher />
                
                <button
                  onClick={logout}
                  className="ml-2 px-3 py-1 text-sm text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-md"
                >
                  Logout
                </button>
              </div>
            )}
          </div>
          
          {/* Mobile menu button */}
          <div className="flex items-center sm:hidden">
            <div className="flex items-center space-x-3">
              {user && <UserSwitcher />}
            </div>
          </div>
        </div>
      </div>
      
      {/* Mobile menu, show/hide based on menu state */}
      <div className="sm:hidden">
        <div className="pt-2 pb-3 space-y-1">
          <Link
            to="/projects"
            className={`${
              location.pathname === '/projects'
                ? 'bg-blue-50 border-blue-500 text-blue-700'
                : 'border-transparent text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800'
            } block pl-3 pr-4 py-2 border-l-4 text-base font-medium`}
          >
            Projects
          </Link>
          
          <Link
            to="/tasks"
            className={`${
              location.pathname === '/tasks' || location.pathname.startsWith('/tasks/')
                ? 'bg-blue-50 border-blue-500 text-blue-700'
                : 'border-transparent text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800'
            } block pl-3 pr-4 py-2 border-l-4 text-base font-medium`}
          >
            Tasks
          </Link>
          
          <button
            onClick={logout}
            className="block w-full text-left pl-3 pr-4 py-2 border-l-4 border-transparent text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800 text-base font-medium"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}
