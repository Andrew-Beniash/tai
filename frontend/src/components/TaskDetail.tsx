/**
 * TaskDetail component
 * Displays detailed information about a task including metadata and associated documents
 * Allows viewing/downloading of project documents from Google Drive
 */

import { useState, useEffect } from 'react';
import { Task } from '../api/tasks';
import { Document, getTaskDocuments, syncProjectDocuments } from '../api/documents';
import DocumentList from './DocumentList';

interface TaskDetailProps {
  task: Task;
}

export default function TaskDetail({ task }: TaskDetailProps) {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  
  // Fetch documents when the task changes
  useEffect(() => {
    fetchDocuments();
  }, [task.task_id]);
  
  // Function to fetch documents associated with the task
  const fetchDocuments = async () => {
    try {
      setIsLoading(true);
      const docs = await getTaskDocuments(task.task_id);
      setDocuments(docs);
    } catch (error) {
      console.error('Error fetching task documents:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Function to sync documents with Google Drive
  const handleSyncDocuments = async () => {
    try {
      setIsLoading(true);
      // Sync project documents first
      await syncProjectDocuments(task.project_id);
      // Then refresh the task documents
      await fetchDocuments();
    } catch (error) {
      console.error('Error syncing documents:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'in progress':
        return 'bg-yellow-100 text-yellow-800';
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'not started':
        return 'bg-gray-100 text-gray-800';
      case 'blocked':
        return 'bg-red-100 text-red-800';
      case 'review':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
      <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              {task.description || `Task ${task.task_id}`}
            </h3>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              Task details and associated documents
            </p>
          </div>
          <div>
            <span className={`px-3 py-1 inline-flex text-sm leading-5 font-semibold rounded-full ${getStatusColor(task.status)}`}>
              {task.status}
            </span>
          </div>
        </div>
      </div>
      
      <div className="border-b border-gray-200">
        <dl>
          <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt className="text-sm font-medium text-gray-500">
              Task ID
            </dt>
            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              {task.task_id}
            </dd>
          </div>
          <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt className="text-sm font-medium text-gray-500">
              Client
            </dt>
            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              {task.client}
            </dd>
          </div>
          <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt className="text-sm font-medium text-gray-500">
              Tax Form
            </dt>
            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              {task.tax_form}
            </dd>
          </div>
          <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt className="text-sm font-medium text-gray-500">
              Assigned To
            </dt>
            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              {task.assigned_to === 'jeff' ? 'Jeff (Preparer)' : 'Hanna (Reviewer)'}
            </dd>
          </div>
          <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt className="text-sm font-medium text-gray-500">
              Status
            </dt>
            <dd className="mt-1 sm:mt-0 sm:col-span-2">
              <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(task.status)}`}>
                {task.status}
              </span>
            </dd>
          </div>
          <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt className="text-sm font-medium text-gray-500">
              Priority
            </dt>
            <dd className="mt-1 sm:mt-0 sm:col-span-2">
              <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getPriorityColor(task.priority || 'medium')}`}>
                {task.priority || 'Medium'}
              </span>
            </dd>
          </div>
          <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt className="text-sm font-medium text-gray-500">
              Due Date
            </dt>
            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              {formatDate(task.due_date)}
            </dd>
          </div>
          <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt className="text-sm font-medium text-gray-500">
              Description
            </dt>
            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              {task.description || 'No description provided.'}
            </dd>
          </div>
          
          {/* Associated Documents Section */}
          <div className="bg-gray-50 px-4 py-5 sm:px-6">
            <dt className="text-sm font-medium text-gray-500 mb-2">
              Associated Documents
            </dt>
            <dd>
              <DocumentList 
                documents={documents} 
                onRefresh={handleSyncDocuments}
                isLoading={isLoading}
              />
            </dd>
          </div>
        </dl>
      </div>
    </div>
  );
}
