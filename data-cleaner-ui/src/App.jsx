import { useState } from 'react';
import Report from './components/Report';
import './App.css';

const Spinner = () => <div className="spinner"></div>;

const ProgressBar = ({ progress, message }) => (
  <div className="progress-container">
    <div className="progress-message">{message}</div>
    <div className="progress-bar">
      <div className="progress-fill" style={{ width: `${progress}%` }}></div>
    </div>
    <div className="progress-percentage">{progress}%</div>
  </div>
);

function App() {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [analysisData, setAnalysisData] = useState(null);
  const [status, setStatus] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isGeneratingProfile, setIsGeneratingProfile] = useState(false);
  const [profileProgress, setProfileProgress] = useState(0);
  const [profileMessage, setProfileMessage] = useState('');

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
      setAnalysisData(null);
      setStatus('');
    }
  };

  const handleApiCall = async (endpoint) => {
    if (!file) {
      setStatus('Please select a file first!');
      return null;
    }

    setIsLoading(true);
    setStatus('Working on it...');
    setAnalysisData(null);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/${endpoint}/`, {
        method: 'POST',
        body: formData,
      });
      // Always return the response; callers handle status-specific logic
      return response;
    } catch (error) {
      setStatus('❌ Failed to connect to the server. Is it running?');
      console.error('Error:', error);
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnalyze = async () => {
    const response = await handleApiCall('upload-and-analyze');
    if (!response) return;
    if (!response.ok) {
      const text = await response.text();
      setStatus(`❌ Analyze failed: ${text || response.status}`);
      return;
    }
    try {
      const data = await response.json();
      setAnalysisData(data);
      setStatus('✅ Analysis complete!');
    } catch (err) {
      const text = await response.text();
      setStatus('❌ Server returned an unexpected response. See console for details.');
      console.error('Non-JSON analyze response:', err, text);
    }
  };

  const handleCleanAndDownload = async () => {
    const response = await handleApiCall('clean-file');
    if (!response) return;
    if (!response.ok) {
      const text = await response.text();
      setStatus(`❌ Clean failed: ${text || response.status}`);
      return;
    }
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cleaned_${file.name}`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
    setStatus('✅ Download complete!');
  };

  const handleProfileReport = async () => {
    if (!file) {
      setStatus('Please select a file first!');
      return;
    }

    setIsGeneratingProfile(true);
    setProfileProgress(0);
    setProfileMessage('Preparing data for profiling...');
    setStatus('');

    // Simulate progress updates during the profiling process
    const progressInterval = setInterval(() => {
      setProfileProgress(prev => {
        if (prev < 90) {
          const increment = Math.random() * 15 + 5; // Random increment between 5-20
          const newProgress = Math.min(prev + increment, 90);

          // Update message based on progress
          if (newProgress < 20) {
            setProfileMessage('Uploading and parsing file...');
          } else if (newProgress < 40) {
            setProfileMessage('Analyzing data structure...');
          } else if (newProgress < 60) {
            setProfileMessage('Computing statistical summaries...');
          } else if (newProgress < 80) {
            setProfileMessage('Generating visualizations...');
          } else {
            setProfileMessage('Finalizing report...');
          }

          return newProgress;
        }
        return prev;
      });
    }, 800); // Update every 800ms

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/profile-report/`, {
        method: 'POST',
        body: formData,
      });

      clearInterval(progressInterval);
      setProfileProgress(100);
      setProfileMessage('Processing complete!');

      if (!response.ok) {
        // Try to read JSON error with message
        let msg = '';
        try {
          const err = await response.json();
          msg = err?.message || '';
        } catch {
          msg = await response.text();
        }
        setStatus(`ℹ️ ${msg || 'Profiling not available on this environment.'}`);
        return;
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `profile_${file.name.replace(/\.[^.]+$/, '')}.html`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      setStatus('✅ Profiling report downloaded!');
    } catch (error) {
      clearInterval(progressInterval);
      setStatus('❌ Failed to connect to the server. Is it running?');
      console.error('Error:', error);
    } finally {
      // Keep progress bar visible for a moment before hiding
      setTimeout(() => {
        setIsGeneratingProfile(false);
        setProfileProgress(0);
        setProfileMessage('');
      }, 2000);
    }
  };



  return (
    <>
      <div className="container">
        <div className="header">
          <img src="/logo.gif" alt="DataFixer Logo" className="logo" />
          <h1>DataFixer</h1>
        </div>
        <p>Upload a CSV file to get a professional report on potential issues and cleaning recommendations.</p>

        <label htmlFor="file-upload" className="file-upload-label">
          {fileName ? (
            <div className="filename">Selected: <strong>{fileName}</strong></div>
          ) : (
            <div>
              <span className="placeholder">Drag & drop or click to upload</span>
              <p style={{ fontSize: '0.8rem', color: '#9ca3af', margin: '0.5rem 0 0 0' }}>CSV and JSON files supported</p>
            </div>
          )
          }
        </label>
        <input id="file-upload" type="file" onChange={handleFileChange} accept=".csv,.json,application/json" />

        <div className="button-group">
          <button onClick={handleAnalyze} className="analyzeBtn" disabled={isLoading || !file}>
            {isLoading && <Spinner />} Analyze Data
          </button>
          <button onClick={handleCleanAndDownload} className="cleanBtn" disabled={isLoading || !file}>
            {isLoading && <Spinner />} Clean & Download
          </button>
          <button onClick={handleProfileReport} className="analyzeBtn" disabled={isLoading || !file || isGeneratingProfile}>
            {isGeneratingProfile ? <Spinner /> : (isLoading && <Spinner />)} Generate Profile
          </button>
        </div>

        {isGeneratingProfile && (
          <ProgressBar
            progress={profileProgress}
            message={profileMessage}
          />
        )}

        <p id="status">{status}</p>
      </div>

      <div className="results-area">
        {analysisData ? (
          <Report data={analysisData} />
        ) : (
          <div className="placeholder-results">Upload a file and click Analyze to see the report here.</div>
        )}
      </div>
    </>
  );
}

export default App;
