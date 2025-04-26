/**
 * DocumentList component
 * Displays a list of documents with view and download options
 * Used for showing project and task documents from Google Drive
 */

import { useState, useEffect } from 'react';
import { Document, getDocumentContent, getDocumentDownloadUrl } from '../api/documents';

interface DocumentListProps {
  documents: Document[];
  onRefresh?: () => void;
  showRefreshButton?: boolean;
  isLoading?: boolean;
}

// Document types to appropriate icons mapping
const FILE_ICON_MAP: Record<string, JSX.Element> = {
  pdf: (
    <svg className="flex-shrink-0 h-5 w-5 text-red-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
    </svg>
  ),
  docx: (
    <svg className="flex-shrink-0 h-5 w-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
    </svg>
  ),
  xlsx: (
    <svg className="flex-shrink-0 h-5 w-5 text-green-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M5 4a1 1 0 00-1 1v10a1 1 0 001 1h10a1 1 0 001-1V5a1 1 0 00-1-1H5zm6 9a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
    </svg>
  ),
  txt: (
    <svg className="flex-shrink-0 h-5 w-5 text-gray-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm3 1h6v4H7V5zm8 8v2H7v-2h8zM7 8h8v2H7V8z" clipRule="evenodd" />
    </svg>
  ),
  ppt: (
    <svg className="flex-shrink-0 h-5 w-5 text-orange-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
    </svg>
  ),
  // Default file icon
  default: (
    <svg className="flex-shrink-0 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
    </svg>
  )
};

export default function DocumentList({ 
  documents, 
  onRefresh,
  showRefreshButton = true,
  isLoading = false 
}: DocumentListProps) {
  const [viewingDocument, setViewingDocument] = useState<Document | null>(null);
  const [documentContent, setDocumentContent] = useState<string | null>(null);
  const [isLoadingContent, setIsLoadingContent] = useState(false);
  const [mimeType, setMimeType] = useState<string>('');
  
  // Reset document content when viewing document changes
  useEffect(() => {
    if (!viewingDocument) {
      setDocumentContent(null);
      setMimeType('');
      return;
    }
    
    const fetchContent = async () => {
      try {
        setIsLoadingContent(true);
        const docContent = await getDocumentContent(viewingDocument.doc_id);
        setDocumentContent(docContent.content);
        setMimeType(docContent.mime_type);
      } catch (error) {
        console.error('Error fetching document content:', error);
      } finally {
        setIsLoadingContent(false);
      }
    };
    
    fetchContent();
  }, [viewingDocument]);
  
  // Helper function to get file type icon
  const getFileIcon = (fileName: string) => {
    const extension = fileName.split('.').pop()?.toLowerCase() || 'default';
    return FILE_ICON_MAP[extension] || FILE_ICON_MAP.default;
  };
  
  // Helper to view a document
  const viewDocument = (doc: Document) => {
    if (doc.web_view_link) {
      // If Google Drive link available, open in new tab
      window.open(doc.web_view_link, '_blank');
    } else {
      // Otherwise, fetch and display document
      setViewingDocument(doc);
    }
  };
  
  // Helper to download document
  const downloadDocument = (doc: Document) => {
    // Create download link
    const downloadUrl = getDocumentDownloadUrl(doc.doc_id);
    
    // Create temp anchor and trigger download
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = doc.file_name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };
  
  // Helper to format file size
  const formatFileSize = (bytes?: number) => {
    if (!bytes) return 'Unknown size';
    
    if (bytes < 1024) return bytes + ' B';
    else if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    else if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    else return (bytes / (1024 * 1024 * 1024)).toFixed(1) + ' GB';
  };
  
  // Close document preview
  const closePreview = () => {
    setViewingDocument(null);
    setDocumentContent(null);
  };

  return (
    <div className="mt-1 text-sm text-gray-900">
      {/* Document preview modal */}
      {viewingDocument && (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl w-11/12 lg:w-3/4 xl:w-2/3 h-5/6 flex flex-col">
            <div className="flex justify-between items-center px-6 py-4 border-b">
              <h3 className="text-lg font-medium text-gray-900">
                {viewingDocument.file_name}
              </h3>
              <button
                onClick={closePreview}
                className="text-gray-400 hover:text-gray-500 focus:outline-none"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="flex-1 p-6 overflow-auto">
              {isLoadingContent ? (
                <div className="flex items-center justify-center h-full">
                  <svg className="animate-spin h-10 w-10 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </div>
              ) : documentContent ? (
                mimeType.startsWith('text/') ? (
                  <pre className="whitespace-pre-wrap font-mono text-sm">{atob(documentContent)}</pre>
                ) : mimeType.startsWith('image/') ? (
                  <img src={`data:${mimeType};base64,${documentContent}`} alt={viewingDocument.file_name} className="max-w-full max-h-full mx-auto" />
                ) : mimeType === 'application/pdf' ? (
                  <iframe
                    src={`data:application/pdf;base64,${documentContent}`}
                    className="w-full h-full"
                    title={viewingDocument.file_name}
                  />
                ) : (
                  <div className="flex flex-col items-center justify-center h-full">
                    <div className="text-4xl mb-4">{getFileIcon(viewingDocument.file_name)}</div>
                    <p className="text-gray-500 mb-4">Preview not available for this file type.</p>
                    <button
                      onClick={() => downloadDocument(viewingDocument)}
                      className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                    >
                      Download File
                    </button>
                  </div>
                )
              ) : (
                <div className="flex items-center justify-center h-full">
                  <p className="text-gray-500">Unable to load document content.</p>
                </div>
              )}
            </div>
            
            <div className="px-6 py-4 border-t flex justify-between">
              <div className="text-sm text-gray-500">
                {viewingDocument.description && <p>{viewingDocument.description}</p>}
                <p>
                  {viewingDocument.size_bytes && (
                    <span className="mr-3">{formatFileSize(viewingDocument.size_bytes)}</span>
                  )}
                  {viewingDocument.last_modified && (
                    <span>Modified: {new Date(viewingDocument.last_modified).toLocaleDateString()}</span>
                  )}
                </p>
              </div>
              <button
                onClick={() => downloadDocument(viewingDocument)}
                className="ml-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Download
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Documents list with refresh button */}
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-sm font-medium text-gray-500">
          Documents ({documents.length})
        </h3>
        {showRefreshButton && onRefresh && (
          <button
            onClick={onRefresh}
            disabled={isLoading}
            className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            {isLoading ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-blue-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Syncing...
              </>
            ) : (
              <>
                <svg className="-ml-1 mr-2 h-4 w-4 text-blue-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Sync with Drive
              </>
            )}
          </button>
        )}
      </div>
      
      {/* Document list */}
      <ul className="border border-gray-200 rounded-md divide-y divide-gray-200">
        {isLoading ? (
          <li className="pl-3 pr-4 py-3 flex items-center justify-center">
            <svg className="animate-spin h-5 w-5 text-blue-500 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span className="text-sm text-gray-500">Loading documents...</span>
          </li>
        ) : documents.length > 0 ? (
          documents.map((doc, index) => (
            <li key={index} className="px-3 py-3 flex items-center justify-between text-sm hover:bg-gray-50">
              <div className="w-0 flex-1 flex items-center">
                {getFileIcon(doc.file_name)}
                <div className="ml-2 flex-1 w-0">
                  <div className="font-medium truncate">{doc.file_name}</div>
                  {doc.description && (
                    <div className="text-gray-500 text-xs">{doc.description}</div>
                  )}
                  <div className="text-gray-500 text-xs mt-1 flex space-x-3">
                    {doc.size_bytes && (
                      <span>{formatFileSize(doc.size_bytes)}</span>
                    )}
                    {doc.last_modified && (
                      <span>Modified: {new Date(doc.last_modified).toLocaleDateString()}</span>
                    )}
                  </div>
                </div>
              </div>
              <div className="ml-4 flex-shrink-0 flex">
                <button
                  onClick={() => viewDocument(doc)}
                  className="font-medium text-blue-600 hover:text-blue-500 mr-3"
                >
                  View
                </button>
                <button 
                  onClick={() => downloadDocument(doc)}
                  className="font-medium text-blue-600 hover:text-blue-500"
                >
                  Download
                </button>
              </div>
            </li>
          ))
        ) : (
          <li className="pl-3 pr-4 py-3 text-sm text-gray-500">
            No documents available.
          </li>
        )}
      </ul>
    </div>
  );
}
