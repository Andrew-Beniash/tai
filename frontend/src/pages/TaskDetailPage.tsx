/**
 * TaskDetailPage component
 * Displays task details, associated documents, and embedded AI chat
 */

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Task, getTask } from '../api/tasks';
import { useAuth } from '../context/AuthContext';
import ChatWidget from '../components/ChatWidget';
import TaskDetail from '../components/TaskDetail';

export default function TaskDetailPage() {
  const { taskId } = useParams<{ taskId: string }>();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch task details when the component mounts
    const fetchTaskDetails = async () => {
      if (!taskId) {
        navigate('/projects');
        return;
      }

      try {
        setLoading(true);
        const taskData = await getTask(taskId);
        setTask(taskData);
        setError(null);
      } catch (err) {
        setError('Failed to load task details. Please try again.');
        console.error('Error fetching task details:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTaskDetails();
  }, [taskId, navigate]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const goBack = () => {
    navigate(-1); // Go back to previous page
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900">AI-Augmented Tax Engagement</h1>
          <div className="flex items-center">
            {user && (
              <div className="mr-4">
                <span className="text-gray-700">Logged in as </span>
                <span className="font-medium text-blue-600">{user.name} ({user.role})</span>
              </div>
            )}
            <button
              onClick={handleLogout}
              className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button
          onClick={goBack}
          className="inline-flex items-center mb-4 text-sm font-medium text-blue-600 hover:text-blue-900"
        >
          <svg className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back
        </button>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : task ? (
          <div className="space-y-6">
            {/* Task Detail Component */}
            <TaskDetail task={task} />
            
            {/* AI Chat Widget */}
            <div className="bg-white shadow overflow-hidden sm:rounded-lg">
              <div className="px-4 py-5 sm:px-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                  AI Assistant
                </h3>
                {taskId && <ChatWidget taskId={taskId} />}
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-white shadow overflow-hidden sm:rounded-lg p-6 text-center">
            <p>Task not found or you don't have permission to view it.</p>
            <button
              onClick={() => navigate('/projects')}
              className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              Return to Projects
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
