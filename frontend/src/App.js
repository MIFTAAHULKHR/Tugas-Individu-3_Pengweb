import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [review, setReview] = useState('');
  const [result, setResult] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch all reviews on component mount
  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async () => {
    try {
      const response = await fetch('/api/reviews');
      const data = await response.json();
      setReviews(data.reviews || []);
    } catch (err) {
      console.error('Error fetching reviews:', err);
    }
  };

  const analyzeReview = async () => {
    if (!review.trim()) {
      setError('Please enter a review text');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await fetch('/api/analyze-review', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ review_text: review }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to analyze review');
      }

      setResult(data);
      setReview('');
      
      // Refresh reviews list
      fetchReviews();
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive': return '#4CAF50';
      case 'negative': return '#F44336';
      case 'neutral': return '#FF9800';
      default: return '#9E9E9E';
    }
  };

  const getSentimentIcon = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive': return '😊';
      case 'negative': return '😞';
      case 'neutral': return '😐';
      default: return '❓';
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>📊 Product Review Analyzer</h1>
        <p>Analyze sentiment and extract key points from product reviews</p>
      </header>

      <main className="App-main">
        <div className="container">
          {/* Left Panel - Input Form */}
          <div className="left-panel">
            <div className="review-form">
              <h2>🔍 Analyze New Review</h2>
              
              <div className="form-group">
                <label htmlFor="reviewText">Product Review:</label>
                <textarea
                  id="reviewText"
                  value={review}
                  onChange={(e) => setReview(e.target.value)}
                  placeholder="Enter your product review here... Example: 'This product is amazing! Great quality and fast delivery.'"
                  rows="6"
                  disabled={loading}
                />
              </div>

              {error && <div className="error-message">⚠️ {error}</div>}

              <button 
                onClick={analyzeReview}
                disabled={loading || !review.trim()}
                className="submit-btn"
              >
                {loading ? '⏳ Analyzing...' : '🚀 Analyze Review'}
              </button>

              {result && (
                <div className="result-card">
                  <h3>✅ Analysis Result:</h3>
                  <div className="sentiment-display">
                    <span className="sentiment-icon">
                      {getSentimentIcon(result.sentiment)}
                    </span>
                    <span 
                      className="sentiment-text"
                      style={{ color: getSentimentColor(result.sentiment) }}
                    >
                      {result.sentiment.toUpperCase()}
                    </span>
                  </div>
                  
                  {result.key_points && result.key_points.length > 0 && (
                    <div className="key-points">
                      <h4>📌 Key Points:</h4>
                      <ul>
                        {result.key_points.map((point, index) => (
                          <li key={index}>{point}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Right Panel - Reviews List */}
          <div className="right-panel">
            <div className="review-list">
              <div className="review-list-header">
                <h2>📋 Analysis History</h2>
                <button 
                  onClick={fetchReviews} 
                  className="refresh-btn"
                  disabled={loading}
                >
                  🔄 Refresh
                </button>
              </div>

              {reviews.length === 0 ? (
                <div className="empty-state">
                  <p>No reviews analyzed yet. Submit your first review!</p>
                </div>
              ) : (
                <div className="reviews-container">
                  {reviews.map((rev) => (
                    <div key={rev.id} className="review-card">
                      <div className="review-header">
                        <div className="sentiment-badge">
                          <span className="sentiment-icon">
                            {getSentimentIcon(rev.sentiment)}
                          </span>
                          <span 
                            className="sentiment-text"
                            style={{ color: getSentimentColor(rev.sentiment) }}
                          >
                            {rev.sentiment}
                          </span>
                        </div>
                        <span className="review-date">
                          {new Date(rev.created_at).toLocaleDateString()}
                        </span>
                      </div>
                      
                      <div className="review-text">
                        <p>{rev.review_text}</p>
                      </div>

                      {rev.key_points && rev.key_points.length > 0 && (
                        <div className="key-points">
                          <h4>Key Points:</h4>
                          <ul>
                            {rev.key_points.map((point, index) => (
                              <li key={index}>• {point}</li>
                            ))}
                          </ul>
                        </div>
                      )}

                      <div 
                        className="sentiment-bar"
                        style={{ backgroundColor: getSentimentColor(rev.sentiment) }}
                      />
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      <footer className="App-footer">
        <p>© 2025 Product Review Analyzer | React + Flask + PostgreSQL + Gemini AI</p>
      </footer>
    </div>
  );
}

export default App;