from transformers import pipeline
import os

# Inisialisasi sentiment analyzer
try:
    # Gunakan model yang lebih ringan
    classifier = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        framework="pt"
    )
    print("✅ Sentiment analyzer loaded successfully")
except Exception as e:
    print(f"❌ Error loading sentiment analyzer: {e}")
    classifier = None

def analyze_sentiment(text):
    """
    Analyze sentiment of text
    Returns: 'positive', 'negative', or 'neutral'
    """
    if classifier is None:
        return "neutral"
    
    try:
        # Batasi panjang teks untuk performa
        text = str(text)[:512]
        result = classifier(text)
        label = result[0]['label'].lower()
        
        # Map ke kategori kita
        if 'positive' in label:
            return 'positive'
        elif 'negative' in label:
            return 'negative'
        else:
            return 'neutral'
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return 'neutral'

# Buat instance untuk import
sentiment_analyzer = {
    "analyze": analyze_sentiment
}