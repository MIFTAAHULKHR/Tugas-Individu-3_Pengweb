import React from 'react';

const SentimentDisplay = ({ sentiment }) => {
  const getSentimentIcon = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive':
        return '😊';
      case 'negative':
        return '😞';
      case 'neutral':
        return '😐';
      default:
        return '❓';
    }
  };

  const getSentimentText = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive':
        return 'Positive';
      case 'negative':
        return 'Negative';
      case 'neutral':
        return 'Neutral';
      default:
        return 'Unknown';
    }
  };

  return (
    <div className="sentiment-display">
      <span className="sentiment-icon">{getSentimentIcon(sentiment)}</span>
      <span className="sentiment-text">{getSentimentText(sentiment)}</span>
    </div>
  );
};

export default SentimentDisplay;