import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from prometheus_flask_exporter import PrometheusMetrics

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
metrics = PrometheusMetrics.for_app_factory()

def create_app(config=None):
    app = Flask(__name__, static_folder='static')
    
    # Load configuration
    app.config.from_object('app.config.Config')
    if config:
        app.config.update(config)
    
    # Initialize extensions with app
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    metrics.init_app(app)
    
    # Custom metrics
    metrics.info('app_info', 'Application info', version='1.0.0')
    
    # Register blueprints
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    @app.route('/')
    def index():
        return app.send_static_file('index.html')
    
    # Handle 404 and serve index.html for all other routes (SPA support)
    @app.errorhandler(404)
    def not_found(e):
        return app.send_static_file('index.html')
    
    return app
