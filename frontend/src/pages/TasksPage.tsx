/**
 * TasksPage component
 * Displays a list of tasks for the selected project and current user
 */

import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Task, getTasks } from '../api/tasks';
import { Project, getProject } from '../api/projects';
import { useAuth } from '../context/AuthContext';
import TaskList from '../components/TaskList';

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [project, setProject] = useState<Project | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  
  // Extract project ID from query string
  const queryParams = new URLSearchParams(location.search);
  const projectId = queryParams.get('project');

  useEffect(() => {
    // Fetch tasks when the component mounts or projectId changes
    const fetchData = async () => {
      if (!projectId) {
        navigate('/projects');
        return;
      }

      try {
        setLoading(true);
        
        // First get project details
        const projectData = await getProject(projectId);
        setProject(projectData);
        
        // Then get tasks for this project
        const tasksData = await getTasks(projectId);
        
        // Filter tasks assigned to the current user
        const filteredTasks = tasksData.filter(task => 
          task.assigned_to === user?.id
        );
        
        setTasks(filteredTasks);
        setError(null);
      } catch (err) {
        setError('Failed to load tasks. Please try again.');
        console.error('Error fetching tasks:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [projectId, user, navigate]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const goBack = () => {
    navigate('/projects');
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
        <div className="md:flex md:items-center md:justify-between mb-6">
          <div className="flex-1 min-w-0">
            <button
              onClick={goBack}
              className="inline-flex items-center mb-4 text-sm font-medium text-blue-600 hover:text-blue-900"
            >
              <svg className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              Back to Projects
            </button>
            
            <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
              Tasks for {project?.name || 'Project'}
            </h2>
            {project && (
              <div className="mt-1 text-sm text-gray-500">
                <span className="font-medium">Clients:</span> {project.clients.join(', ')} | 
                <span className="font-medium ml-2">Services:</span> {project.services.join(', ')}
              </div>
            )}
          </div>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        <TaskList tasks={tasks} isLoading={loading} />
      </main>
    </div>
  );
}
