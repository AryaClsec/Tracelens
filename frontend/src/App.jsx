// frontend/src/App.jsx
import React, { useState } from 'react';
import UploadForm from './components/UploadForm';
import ResultsView from './components/ResultsView';
import './App.css';

function App() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalysisComplete = (result) => {
    setAnalysisResult(result);
    setLoading(false);
  };

  const handleAnalysisStart = () => {
    setLoading(true);
    setAnalysisResult(null);
  };

  const handleReset = () => {
    setAnalysisResult(null);
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔍 TraceLens</h1>
        <p className="subtitle">OSINT Image Analysis Platform</p>
        <div className="ethics-notice">
          ⚖️ For lawful, ethical research only. Respect privacy and local laws.
        </div>
      </header>

      <main className="App-main">
        <UploadForm 
          onAnalysisComplete={handleAnalysisComplete}
          onAnalysisStart={handleAnalysisStart}
          loading={loading}
        />
        
        {analysisResult && (
          <ResultsView 
            result={analysisResult}
            onReset={handleReset}
          />
        )}
      </main>

      <footer className="App-footer">
        <p>TraceLens v1.0.0 | Open Source OSINT Tool</p>
        <p>
          <a href="https://github.com/yourusername/tracelens" target="_blank" rel="noopener noreferrer">
            GitHub
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;