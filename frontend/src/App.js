import React, { useState } from 'react'; // Removed useEffect
import './App.css';
import Header from './components/Header';
import Uploader from './components/Uploader';
import ResultsDisplay from './components/ResultsDisplay';

function App() {
    // The state is now initialized to null and will always be null on page load.
    const [parsedData, setParsedData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    // The useEffect hook that checked localStorage has been completely removed.

    const handleFileUpload = async (file) => {
        setIsLoading(true);
        setError('');
        setParsedData(null); // Clear previous results immediately

        const formData = new FormData();
        formData.append('statement', file);

        try {
            const response = await fetch('http://127.0.0.1:5000/parse', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'An unknown error occurred.');
            }

            setParsedData(data);
            
            // The line that saved to localStorage has been removed.
            // localStorage.setItem('parsedStatementData', JSON.stringify(data)); // <-- REMOVED

        } catch (err) {
            setError(err.message);
            // The line that removed from localStorage on error is also no longer needed.
            // localStorage.removeItem('parsedStatementData'); // <-- REMOVED
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container">
            <Header />
            <Uploader onFileUpload={handleFileUpload} />
            
            {isLoading && (
                <div className="spinner-container">
                    <div className="spinner"></div>
                    <p>Parsing your document...</p>
                </div>
            )}
            
            {error && <p className="error-message">Error: {error}</p>}
            
            {/* This will only render if parsedData is not null */}
            {parsedData && <ResultsDisplay data={parsedData} />}
        </div>
    );
}

export default App;