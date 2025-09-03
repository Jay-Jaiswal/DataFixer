import { useState } from 'react';
import Report from './components/Report';
import './App.css';

const Spinner = () => <div className="spinner"></div>;

function App() {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [analysisData, setAnalysisData] = useState(null);
  const [status, setStatus] = useState('');
  const [isLoading, setIsLoading] = useState(false);

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

      if (!response.ok) throw new Error('API call failed. Check server logs.');

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
    if (response) {
      try {
        const data = await response.json();
        setAnalysisData(data);
        setStatus('✅ Analysis complete!');
      } catch (err) {
        // Server returned non-JSON (possibly an error message)
        const text = await response.text();
        setStatus('❌ Server returned an unexpected response. See console for details.');
        console.error('Non-JSON analyze response:', err, text);
      }
    }
  };

  const handleCleanAndDownload = async () => {
    const response = await handleApiCall('clean-file');
    if (response) {
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
    }
  };

  return (
    <>
      <div className="container">
        <h1>DataFixer 🚀</h1>
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
        </div>
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
