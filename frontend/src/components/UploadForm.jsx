// frontend/src/components/UploadForm.jsx
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './UploadForm.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function UploadForm({ onAnalysisComplete, onAnalysisStart, loading }) {
  const [error, setError] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setError(null);
    onAnalysisStart();
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/api/v1/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setUploadProgress(percentCompleted);
        },
      });

      onAnalysisComplete(response.data);
    } catch (err) {
      console.error('Analysis error:', err);
      setError(
        err.response?.data?.detail || 
        'Analysis failed. Please try again with a different image.'
      );
      onAnalysisComplete(null);
    }
  }, [onAnalysisComplete, onAnalysisStart]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: false
  });

  return (
    <div className="upload-container">
      <div 
        {...getRootProps()} 
        className={`dropzone ${isDragActive ? 'active' : ''} ${loading ? 'loading' : ''}`}
      >
        <input {...getInputProps()} />
        
        {loading ? (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Analyzing image...</p>
            {uploadProgress > 0 && uploadProgress < 100 && (
              <div className="progress-bar">
                <div 
                  className="progress-fill" 
                  style={{ width: `${uploadProgress}%` }}
                ></div>
              </div>
            )}
          </div>
        ) : (
          <>
            <div className="upload-icon">📤</div>
            {isDragActive ? (
              <p className="upload-text">Drop the image here...</p>
            ) : (
              <>
                <p className="upload-text">
                  Drag & drop an image here, or click to select
                </p>
                <p className="upload-hint">
                  Supported: JPG, PNG, GIF, BMP, TIFF (Max 10MB)
                </p>
              </>
            )}
          </>
        )}
      </div>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}
    </div>
  );
}

export default UploadForm;