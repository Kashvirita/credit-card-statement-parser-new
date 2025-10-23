import React from 'react';

// Helper to format keys like "card_holder_name" into "Card Holder Name"
const formatKey = (key) => {
    return key.replace(/_/g, ' ').replace(/\b\w/g, (char) => char.toUpperCase());
};

const ResultCard = ({ label, value }) => (
    <div className="result-card">
        <div className="key">{label}</div>
        <div className="value">{value}</div>
    </div>
);

const ResultsDisplay = ({ data }) => (
    <section className="results-container">
        {Object.entries(data)
            .filter(([key, value]) => value !== null && value !== undefined) // Only show cards with data
            .map(([key, value]) => (
                <ResultCard key={key} label={formatKey(key)} value={value} />
            ))
        }
    </section>
);

export default ResultsDisplay;