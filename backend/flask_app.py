from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv

# Load environment first
load_dotenv()

# Import after loading env
from database import SessionLocal, engine
from models import Review, Base
from sentiment_analyzer import sentiment_analyzer
from keypoints_extractor import keypoints_extractor

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Create database tables
print("Creating database tables if not exist...")
Base.metadata.create_all(bind=engine)
print("✅ Database ready!")

@app.route('/api/analyze-review', methods=['POST', 'OPTIONS'])
def analyze_review_endpoint():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        review_text = data.get('review_text', '').strip()
        
        if not review_text:
            return jsonify({"error": "Review text is required"}), 400
        
        if len(review_text) < 10:
            return jsonify({"error": "Review text too short"}), 400
        
        print(f"Analyzing review: {review_text[:50]}...")
        
        # Analyze sentiment
        sentiment = sentiment_analyzer["analyze"](review_text)
        print(f"Sentiment: {sentiment}")
        
        # Extract key points
        key_points = keypoints_extractor.extract(review_text)
        print(f"Key points extracted: {len(key_points)}")
        
        # Save to database
        db = SessionLocal()
        try:
            review = Review(
                review_text=review_text,
                sentiment=sentiment,
                key_points=json.dumps(key_points) if key_points else None
            )
            
            db.add(review)
            db.commit()
            db.refresh(review)
            
            response_data = {
                "id": review.id,
                "review_text": review.review_text,
                "sentiment": review.sentiment,
                "key_points": json.loads(review.key_points) if review.key_points else [],
                "created_at": review.created_at.isoformat() if review.created_at else None,
                "message": "Review analyzed successfully"
            }
            
            return jsonify(response_data), 201
            
        except Exception as e:
            db.rollback()
            return jsonify({"error": f"Database error: {str(e)}"}), 500
        finally:
            db.close()
            
    except Exception as e:
        print(f"Error in analyze_review: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/reviews', methods=['GET', 'OPTIONS'])
def get_reviews_endpoint():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        db = SessionLocal()
        try:
            reviews = db.query(Review).order_by(Review.created_at.desc()).all()
            
            reviews_list = []
            for review in reviews:
                review_dict = {
                    "id": review.id,
                    "review_text": review.review_text,
                    "sentiment": review.sentiment,
                    "key_points": json.loads(review.key_points) if review.key_points else [],
                    "created_at": review.created_at.isoformat() if review.created_at else None
                }
                reviews_list.append(review_dict)
            
            return jsonify({
                "reviews": reviews_list,
                "count": len(reviews_list)
            })
            
        except Exception as e:
            return jsonify({"error": f"Database error: {str(e)}"}), 500
        finally:
            db.close()
            
    except Exception as e:
        print(f"Error in get_reviews: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Product Review Analyzer",
        "database": "connected",
        "sentiment_analyzer": "loaded" if sentiment_analyzer else "error",
        "gemini_api": "loaded" if keypoints_extractor.model else "not configured"
    })

@app.route('/')
def home():
    return jsonify({
        "message": "Product Review Analyzer API",
        "endpoints": {
            "POST /api/analyze-review": "Analyze a new product review",
            "GET /api/reviews": "Get all analyzed reviews",
            "GET /api/health": "Health check"
        },
        "docs": "See frontend at http://localhost:3000"
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"\n{'='*50}")
    print("🚀 PRODUCT REVIEW ANALYZER BACKEND")
    print(f"{'='*50}")
    print(f"📊 Database: {os.getenv('DATABASE_URL', 'sqlite:///./reviews.db')}")
    print(f"🔗 API URL: http://localhost:{port}")
    print(f"📝 Test: curl http://localhost:{port}/api/health")
    print(f"{'='*50}\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)