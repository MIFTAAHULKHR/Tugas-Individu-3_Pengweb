from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Import routes
from routes import analyze_review, get_reviews

def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)

def main():
    with Configurator() as config:
        # Add CORS headers via event subscriber
        config.add_subscriber(add_cors_headers_response_callback, 'pyramid.events.NewRequest')
        
        # Add routes
        config.add_route('analyze_review', '/api/analyze-review')
        config.add_route('get_reviews', '/api/reviews')
        
        # Add views directly
        config.add_view(
            analyze_review,
            route_name='analyze_review',
            request_method='POST',
            renderer='json'
        )
        
        config.add_view(
            get_reviews,
            route_name='get_reviews',
            request_method='GET',
            renderer='json'
        )
        
        # Handle OPTIONS method for CORS preflight
        config.add_view(
            lambda request: Response(),
            route_name='analyze_review',
            request_method='OPTIONS'
        )
        
        config.add_view(
            lambda request: Response(),
            route_name='get_reviews',
            request_method='OPTIONS'
        )
        
        app = config.make_wsgi_app()
    
    return app

if __name__ == '__main__':
    # Create tables first
    from database import Base, engine
    from models import Review
    Base.metadata.create_all(bind=engine)
    print("Database tables checked/created!")
    
    # Start server
    app = main()
    port = int(os.getenv('PORT', 6543))
    server = make_server('0.0.0.0', port, app)
    print(f'Server running on http://localhost:{port}')
    print('Press Ctrl+C to stop the server')
    server.serve_forever()