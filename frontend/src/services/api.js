import axios from 'axios';

const API_BASE_URL = 'http://localhost:6543/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzeReview = async (reviewText) => {
  try {
    const response = await api.post('/analyze-review', {
      review_text: reviewText,
    });
    return response.data;
  } catch (error) {
    console.error('Error analyzing review:', error);
    throw error;
  }
};

export const getReviews = async () => {
  try {
    const response = await api.get('/reviews');
    return response.data;
  } catch (error) {
    console.error('Error fetching reviews:', error);
    throw error;
  }
};

export default api;