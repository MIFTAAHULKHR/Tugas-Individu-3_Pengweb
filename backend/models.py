from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    review_text = Column(Text, nullable=False)
    sentiment = Column(String(20), nullable=False)
    key_points = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "review_text": self.review_text,
            "sentiment": self.sentiment,
            "key_points": self.key_points,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }