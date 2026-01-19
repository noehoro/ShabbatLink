"""Flask application factory."""
import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Handle DATABASE_URL - Render uses postgres:// but SQLAlchemy needs postgresql://
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///shabbatlink.db')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'shabbatlink2024')
    app.config['FRONTEND_URL'] = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
    
    # Apply any custom config
    if config:
        app.config.update(config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Configure CORS - allow both local development and production frontend
    allowed_origins = [
        app.config['FRONTEND_URL'],
        "http://localhost:3000",
        "https://shabbatlink.com",
        "https://www.shabbatlink.com",
        "https://shabbatlink-frontend.onrender.com"
    ]
    CORS(app, resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Register blueprints
    from app.routes.guests import guests_bp
    from app.routes.hosts import hosts_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.matches import matches_bp
    from app.routes.attendance import attendance_bp
    
    app.register_blueprint(guests_bp, url_prefix='/api/guests')
    app.register_blueprint(hosts_bp, url_prefix='/api/hosts')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(matches_bp, url_prefix='/api/matches')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
