from flask import Flask
from flask_migrate import Migrate

from padv_9.config import DevelopmentConfig
from padv_9.routers.questions import questions_bp
from padv_9.routers.answers import answers_bp
from padv_9.models import db


def create_app() -> Flask:
    app = Flask(__name__)  # http://127.0.0.1:5000
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app=app, db=db)
    app.register_blueprint(questions_bp, url_prefix="/questions")
    app.register_blueprint(answers_bp, url_prefix="/answers")

    return app