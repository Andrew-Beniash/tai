/**
 * DocumentsPage component
 * Displays all documents for a specific project with ability to view and download
 */

import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Document, getProjectDocuments, syncProjectDocuments } from '../api/documents';
import { getProject } from '../api/projects';
import DocumentList from '../components/DocumentList';
import Navbar from '../components/Navbar';

export default function DocumentsPage() {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  
  const [documents, setDocuments] = useState<Document[]>([]);
  const [projectName, setProjectName] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  
  // Fetch project and documents on page load
  useEffect(() => {
    if (!projectId) {
      navigate('/projects');
      return;
    }
    
    fetchProjectData();
  }, [projectId]);
  
  // Fetch project details and documents
  const fetchProjectData = async () => {
    try {
      setIsLoading(true);
      
      // Fetch project details
      const project = await getProject(projectId!);
      setProjectName(project.name);
      
      // Fetch project documents
      const docs = await getProjectDocuments(projectId!);
      setDocuments(docs);
    } catch (error) {
      console.error('Error fetching project data:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Handle document sync with Google Drive
  const handleSyncDocuments = async () => {
    if (!projectId) return;
    
    try {
      setIsLoading(true);
      const syncedDocs = await syncProjectDocuments(projectId);
      setDocuments(syncedDocs);
    } catch (error) {
      console.error('Error syncing documents:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      
      <div className="py-10">
        <header>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center">
              <h1 className="text-3xl font-bold leading-tight text-gray-900">
                {projectName || 'Project'} Documents
              </h1>
              
              <div className="flex items-center space-x-4">
                <button
                  onClick={() => navigate(`/projects/${projectId}`)}
                  className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  <svg className="-ml-1 mr-2 h-5 w-5 text-gray-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  Back to Project
                </button>
                
                <button
                  onClick={handleSyncDocuments}
                  disabled={isLoading}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  {isLoading ? (
                    <>
                      <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Syncing...
                    </>
                  ) : (
                    <>
                      <svg className="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      Sync with Google Drive
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </header>
        
        <main>
          <div className="max-w-7xl mx-auto sm:px-6 lg:px-8 mt-8">
            <div className="bg-white shadow overflow-hidden sm:rounded-lg">
              <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
                <h3 className="text-lg leading-6 font-medium text-gray-900">
                  Project Documents
                </h3>
                <p className="mt-1 max-w-2xl text-sm text-gray-500">
                  View and download documents associated with this project
                </p>
              </div>
              
              <div className="px-4 py-5 sm:px-6">
                <DocumentList 
                  documents={documents}
                  onRefresh={handleSyncDocuments}
                  isLoading={isLoading}
                  showRefreshButton={false}
                />
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
