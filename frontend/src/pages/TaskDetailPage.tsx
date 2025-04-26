import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ChatWidget from '../components/ChatWidget';
import { getTask } from '../api/tasks';
import { sendChatMessage, getPresetQuestions } from '../api/chat';

interface TaskDetailPageProps {}

/**
 * Page component for displaying task details and the chat interface
 */
const TaskDetailPage: React.FC<TaskDetailPageProps> = () => {
  const { taskId } = useParams<{ taskId: string }>();
  const navigate = useNavigate();
  
  const [task, setTask] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [presetQuestions, setPresetQuestions] = useState<string[]>([]);
  
  useEffect(() => {
    if (taskId) {
      fetchTaskDetails();
      fetchPresetQuestions();
    }
  }, [taskId]);
  
  const fetchTaskDetails = async () => {
    setLoading(true);
    setError(null);
    try {
      const taskData = await getTask(taskId!);
      setTask(taskData);
    } catch (err) {
      setError('Failed to load task details');
      console.error('Error loading task:', err);
    } finally {
      setLoading(false);
    }
  };
  
  const fetchPresetQuestions = async () => {
    try {
      const questions = await getPresetQuestions(taskId!);
      setPresetQuestions(questions);
    } catch (err) {
      console.error('Error loading preset questions:', err);
      // Use default questions from the chat component
    }
  };
  
  const handleSendMessage = async (message: string) => {
    try {
      const response = await sendChatMessage(taskId!, message);
      
      // Transform the response format from backend to what the chat widget expects
      return {
        response: response.response,
        suggestedActionId: response.suggestedActionId
      };
    } catch (err) {
      console.error('Error sending chat message:', err);
      throw err;
    }
  };
  
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }
  
  if (error || !task) {
    return (
      <div className="container mx-auto p-4">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
          <strong className="font-bold">Error: </strong>
          <span className="block sm:inline">{error || 'Task not found'}</span>
          <button 
            className="mt-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            onClick={() => navigate('/tasks')}
          >
            Back to Tasks
          </button>
        </div>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto p-4">
      <div className="mb-4">
        <button 
          className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center"
          onClick={() => navigate('/tasks')}
        >
          <span>← Back to Tasks</span>
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Task details panel */}
        <div className="md:col-span-1 bg-white rounded-lg shadow p-4">
          <h1 className="text-2xl font-bold mb-4">{task.client} - {task.tax_form}</h1>
          
          <div className="mb-4">
            <h2 className="text-lg font-semibold mb-2">Task Details</h2>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="font-medium">Task ID:</div>
              <div>{task.task_id}</div>
              
              <div className="font-medium">Status:</div>
              <div className="capitalize">{task.status}</div>
              
              <div className="font-medium">Assigned To:</div>
              <div className="capitalize">{task.assigned_to}</div>
              
              <div className="font-medium">Tax Form:</div>
              <div>{task.tax_form}</div>
              
              <div className="font-medium">Due Date:</div>
              <div>{new Date(task.due_date).toLocaleDateString()}</div>
            </div>
          </div>
          
          <div>
            <h2 className="text-lg font-semibold mb-2">Documents</h2>
            {task.documents && task.documents.length > 0 ? (
              <ul className="list-disc pl-5">
                {task.documents.map((doc: any) => (
                  <li key={doc.doc_id} className="mb-1">
                    <a 
                      href={doc.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-blue-500 hover:underline"
                    >
                      {doc.filename}
                    </a>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 italic">No documents attached</p>
            )}
          </div>
        </div>
        
        {/* Chat widget panel */}
        <div className="md:col-span-2 h-[600px]">
          <ChatWidget 
            taskId={taskId!}
            onSendMessage={handleSendMessage}
            presetQuestions={presetQuestions}
          />
        </div>
      </div>
    </div>
  );
};

export default TaskDetailPage;
