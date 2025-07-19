"""
Configuration file for Hinglish Translation Tool
Modify these settings to customize the application behavior
"""

import os

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    
    # File storage settings
    UPLOAD_FOLDER = 'uploads'
    PROCESSED_FOLDER = 'processed'
    
    # Processing limits
    MAX_PDF_PAGES = 1000  # Maximum pages to process from PDF files
    MAX_TEXT_CHUNK_SIZE = 2000  # Characters per processing chunk
    MAX_PROCESSING_TIME = 1800  # 30 minutes timeout
    
    # File type settings
    ALLOWED_EXTENSIONS = {'.pdf', '.html', '.htm', '.zip', '.doc', '.docx', '.txt'}
    
    # Translation settings
    MAX_SUMMARY_SENTENCES = 5  # Number of sentences in summary
    
    # UI settings
    APP_NAME = "Hinglish Translation Tool"
    APP_DESCRIPTION = "Convert your documents into simple, easy-to-understand Hinglish language"
    
    # Cleanup settings
    AUTO_CLEANUP_HOURS = 24  # Delete processed files after 24 hours
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.PROCESSED_FOLDER, exist_ok=True)

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Use environment variables for production settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-this-in-production'
    
    # Stricter limits for production
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB for production
    MAX_PDF_PAGES = 500  # Reduced for production
    MAX_PROCESSING_TIME = 900  # 15 minutes for production

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB for testing
    MAX_PDF_PAGES = 10  # Very limited for testing

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}