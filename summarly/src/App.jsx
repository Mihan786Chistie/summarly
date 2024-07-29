import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import DOMPurify from 'dompurify';
import './App.css';
import poster from './assets/poster.png';

function App() {
  return (
    <>
      <h1 style={{fontFamily: "Playwrite PE", textAlign: "center"}}>Summarly</h1>
     
      <h2 style={{textAlign: "center"}}>Your AI Sidekick for Quick YouTube Summaries</h2>
      <br />
      <br />
      <img src={poster} alt="" height="300px" />
      <br /><br />
      
    </>
  );
}

const Summarizer = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [summary, setSummary] = useState('');
  const [error, setError] = useState(null);

  const handleSummarizeClick = () => {
    setIsLoading(true);
    setSummary(''); // Clear previous summary
    setError(null); // Clear previous error
    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
      const url = tabs[0].url;
      fetch(`http://127.0.0.1:5000/summary?url=${encodeURIComponent(url)}`)
        .then(response => response.json())
        .then(data => {
          if (data.error) {
            setError(data.error);
          } else {
            const sanitizedText = DOMPurify.sanitize(data.summary);
            setSummary(sanitizedText);
          }
          setIsLoading(false);
        })
        .catch(error => {
          console.error('Error fetching the summary:', error);
          setError('An unexpected error occurred while fetching the summary.');
          setIsLoading(false);
        });
    });
  };

  return (
    <div>
      <button onClick={handleSummarizeClick} disabled={isLoading}>
        {isLoading ? <span className="loader"></span> : <span style={{color: 'black'}}>Summarise</span>}
      </button>
      {error && <div className="error">{error}</div>}
      <div id="output" className="markdown-content">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{summary}</ReactMarkdown>
      </div>
    </div>
  );
};

export default App;
