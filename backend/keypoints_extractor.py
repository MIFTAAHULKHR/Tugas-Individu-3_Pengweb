import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class KeyPointsExtractor:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'PASTE_YOUR_NEW_API_KEY_HERE':
            print("⚠️ Warning: GEMINI_API_KEY not set or using default")
            self.model = None
            return
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            print("✅ Gemini API configured successfully")
        except Exception as e:
            print(f"❌ Error configuring Gemini: {e}")
            self.model = None
    
    def extract(self, text):
        if self.model is None:
            return ["No key points extracted (API not configured)"]
        
        try:
            prompt = f"""
            Extract 3-5 key points from this product review.
            Return as a JSON array of strings.
            
            Review: {text}
            
            Format: ["key point 1", "key point 2", "key point 3"]
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean response
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
            
            # Parse JSON
            try:
                key_points = json.loads(response_text)
                if isinstance(key_points, list):
                    return key_points[:5]  # Max 5 points
            except:
                # Fallback: split by lines or bullets
                lines = [line.strip() for line in response_text.split('\n') if line.strip()]
                return lines[:5]
            
        except Exception as e:
            print(f"Error extracting key points: {e}")
        
        return ["Key points extraction failed"]

# Buat instance
keypoints_extractor = KeyPointsExtractor()