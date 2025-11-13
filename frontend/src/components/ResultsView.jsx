// frontend/src/components/ResultsView.jsx
import React, { useState } from 'react';
import './ResultsView.css';

function ResultsView({ result, onReset }) {
  const [activeTab, setActiveTab] = useState('overview');

  if (!result) return null;

  const downloadReport = () => {
    const dataStr = JSON.stringify(result, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `tracelens-report-${Date.now()}.json`;
    link.click();
  };

  const getAIVerdictClass = (verdict) => {
    switch (verdict) {
      case 'ai': return 'verdict-ai';
      case 'human': return 'verdict-human';
      default: return 'verdict-uncertain';
    }
  };

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>📊 Analysis Results</h2>
        <div className="results-actions">
          <button onClick={downloadReport} className="btn btn-download">
            💾 Download Report
          </button>
          <button onClick={onReset} className="btn btn-reset">
            🔄 New Analysis
          </button>
        </div>
      </div>

      <div className="results-tabs">
        <button 
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={`tab ${activeTab === 'metadata' ? 'active' : ''}`}
          onClick={() => setActiveTab('metadata')}
        >
          Metadata
        </button>
        <button 
          className={`tab ${activeTab === 'ocr' ? 'active' : ''}`}
          onClick={() => setActiveTab('ocr')}
        >
          OCR Text
        </button>
        <button 
          className={`tab ${activeTab === 'ai' ? 'active' : ''}`}
          onClick={() => setActiveTab('ai')}
        >
          AI Detection
        </button>
        <button 
          className={`tab ${activeTab === 'search' ? 'active' : ''}`}
          onClick={() => setActiveTab('search')}
        >
          Reverse Search
        </button>
      </div>

      <div className="results-content">
        {activeTab === 'overview' && (
          <div className="tab-content">
            <h3>📁 File Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <strong>Filename:</strong> {result.filename}
              </div>
              <div className="info-item">
                <strong>Format:</strong> {result.metadata.basic?.format}
              </div>
              <div className="info-item">
                <strong>Dimensions:</strong> {result.metadata.basic?.size?.width} × {result.metadata.basic?.size?.height}
              </div>
              <div className="info-item">
                <strong>File Size:</strong> {(result.metadata.basic?.file_size_bytes / 1024).toFixed(2)} KB
              </div>
            </div>

            <h3 className="section-title">🤖 AI Detection Quick View</h3>
            <div className={`ai-verdict-card ${getAIVerdictClass(result.ai_detection.verdict)}`}>
              <div className="verdict-score">{(result.ai_detection.score * 100).toFixed(1)}%</div>
              <div className="verdict-label">{result.ai_detection.verdict.toUpperCase()}</div>
              <p className="verdict-explanation">{result.ai_detection.explanation}</p>
            </div>

            <h3 className="section-title">🔍 Perceptual Hash</h3>
            <code className="hash-display">{result.perceptual_hash}</code>
          </div>
        )}

        {activeTab === 'metadata' && (
          <div className="tab-content">
            <h3>📋 EXIF Data</h3>
            {Object.keys(result.metadata.exif).length > 0 ? (
              <div className="metadata-table">
                {Object.entries(result.metadata.exif).map(([key, value]) => (
                  <div key={key} className="metadata-row">
                    <span className="metadata-key">{key}:</span>
                    <span className="metadata-value">{String(value)}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-data">No EXIF data found</p>
            )}

            {Object.keys(result.metadata.gps).length > 0 && (
              <>
                <h3 className="section-title">📍 GPS Data</h3>
                <div className="metadata-table">
                  {Object.entries(result.metadata.gps).map(([key, value]) => (
                    <div key={key} className="metadata-row">
                      <span className="metadata-key">{key}:</span>
                      <span className="metadata-value">{String(value)}</span>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        )}

        {activeTab === 'ocr' && (
          <div className="tab-content">
            <h3>📝 Extracted Text</h3>
            {result.ocr.confidence && (
              <div className="confidence-badge">
                Confidence: {(result.ocr.confidence * 100).toFixed(1)}%
              </div>
            )}
            {result.ocr.text ? (
              <div className="ocr-text">
                {result.ocr.text}
              </div>
            ) : (
              <p className="no-data">No text detected in image</p>
            )}
          </div>
        )}

        {activeTab === 'ai' && (
          <div className="tab-content">
            <h3>🤖 AI Generation Detection</h3>
            <div className={`ai-verdict-card-large ${getAIVerdictClass(result.ai_detection.verdict)}`}>
              <div className="verdict-header">
                <div className="verdict-score-large">{(result.ai_detection.score * 100).toFixed(1)}%</div>
                <div className="verdict-label-large">{result.ai_detection.verdict.toUpperCase()}</div>
              </div>
              <p className="verdict-explanation-large">{result.ai_detection.explanation}</p>
            </div>

            <h3 className="section-title">🔬 Detection Signals</h3>
            <div className="signals-grid">
              {Object.entries(result.ai_detection.signals).map(([key, value]) => (
                <div key={key} className="signal-card">
                  <h4>{key.replace(/_/g, ' ').toUpperCase()}</h4>
                  <div className="signal-score">
                    Score: {(value.score * 100).toFixed(1)}%
                  </div>
                  <p className="signal-description">{value.description}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'search' && (
          <div className="tab-content">
            <h3>🔄 Reverse Image Search Results</h3>
            {result.reverse_search && result.reverse_search.length > 0 ? (
              <div className="search-results">
                {result.reverse_search.map((match, index) => (
                  <div key={index} className="search-result-card">
                    <div className="search-result-header">
                      <strong>{match.source}</strong>
                      <span className="similarity-badge">
                        {(match.similarity * 100).toFixed(1)}% match
                      </span>
                    </div>
                    {match.url && (
                      <a href={match.url} target="_blank" rel="noopener noreferrer" className="search-link">
                        View Source →
                      </a>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-data">No reverse search matches found</p>
            )}

            {result.duplicates && result.duplicates.length > 0 && (
              <>
                <h3 className="section-title">🔗 Similar Images (pHash)</h3>
                <div className="duplicates-list">
                  {result.duplicates.map((dup, index) => (
                    <div key={index} className="duplicate-card">
                      <code>{dup.hash}</code>
                      <span className="similarity-badge">
                        {dup.similarity_percentage.toFixed(1)}% similar
                      </span>
                      <span className="distance-info">
                        Distance: {dup.distance}
                      </span>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default ResultsView;