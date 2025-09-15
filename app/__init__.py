from flask import Flask, render_template
from flask_cors import CORS
from .config import Config
from .extensions import db, jwt

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from .routes.auth import auth
    from .routes.tasks import tasks

    with app.app_context():
        db.create_all()
        
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(tasks, url_prefix="/api")

    @app.route('/')
    def home():
        return render_template('home.html')

    return app