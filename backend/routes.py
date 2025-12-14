from pyramid.view import view_config
from pyramid.response import Response
import json
from models import Review
from database import get_db
from sentiment_analyzer import sentiment_analyzer
from keypoints_extractor import keypoints_extractor
from sqlalchemy.orm import Session

@view_config(route_name='analyze_review', renderer='json', request_method='POST')
def analyze_review(request):
    try:
        db: Session = next(get_db())
        
        # Get review text from request
        data = request.json_body
        review_text = data.get('review_text', '').strip()
        
        if not review_text:
            request.response.status = 400
            return {"error": "Review text is required"}
        
        # Analyze sentiment
        sentiment = sentiment_analyzer.analyze(review_text)
        
        # Extract key points
        key_points = keypoints_extractor.extract(review_text)
        
        # Save to database
        review = Review(
            review_text=review_text,
            sentiment=sentiment,
            key_points=json.dumps(key_points) if key_points else None
        )
        
        db.add(review)
        db.commit()
        db.refresh(review)
        
        return {
            "id": review.id,
            "review_text": review.review_text,
            "sentiment": review.sentiment,
            "key_points": json.loads(review.key_points) if review.key_points else [],
            "created_at": review.created_at.isoformat() if review.created_at else None
        }
        
    except Exception as e:
        request.response.status = 500
        return {"error": str(e)}

@view_config(route_name='get_reviews', renderer='json')
def get_reviews(request):
    try:
        db: Session = next(get_db())
        
        # Get all reviews
        reviews = db.query(Review).order_by(Review.created_at.desc()).all()
        
        return {
            "reviews": [review.to_dict() for review in reviews]
        }
        
    except Exception as e:
        request.response.status = 500
        return {"error": str(e)}