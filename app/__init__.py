from flask import Flask
from config import Config
from app.extensions import db, jwt, migrate, cors
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Make get_jwt_identity available in templates safely
    @app.context_processor
    def inject_jwt_identity():
        def get_identity_safe():
            try:
                verify_jwt_in_request(optional=True)
                return get_jwt_identity()
            except Exception:
                return None
        return dict(get_jwt_identity=get_identity_safe)

    # Register Blueprints
    from app.routes import auth, main, rooms, issues, groups, bookings
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(main.bp)
    app.register_blueprint(rooms.bp, url_prefix='/rooms')
    app.register_blueprint(issues.bp, url_prefix='/issues')
    app.register_blueprint(groups.bp, url_prefix='/groups')
    app.register_blueprint(bookings.bp, url_prefix='/bookings')
    
    # Configure JWT to look at cookies
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = False  # Set to True in production
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False # Simplification for prototype

    return app
