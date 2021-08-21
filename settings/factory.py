from flask import Flask
from flask_cors import CORS
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from jwt import DecodeError, ExpiredSignatureError

from settings.config import DevelopmentConfig
from settings.exceptions import NotFoundException, BadRequestException, InternalServerException, handle_exception, \
    handle_no_token, handle_invalid_header, handle_expires_token
from settings.layers.database import db
from settings.layers.jwt import jwt
from settings.layers.serialization import ma
from profiles.urls import profiles_blueprint


def create_app():
    app = Flask(__name__)
    config = DevelopmentConfig()
    CORS(app)
    app.config.from_object(config)
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        db.create_all()
    jwt.init_app(app)
    app.register_blueprint(profiles_blueprint)
    # app.register_blueprint(libraries_blueprint)
    app.register_error_handler(NoAuthorizationError, handle_no_token)
    app.register_error_handler(InvalidHeaderError, handle_invalid_header)
    app.register_error_handler(ExpiredSignatureError, handle_expires_token)
    app.register_error_handler(DecodeError, handle_invalid_header)
    app.register_error_handler(BadRequestException, handle_exception)
    app.register_error_handler(NotFoundException, handle_exception)
    app.register_error_handler(InternalServerException, handle_exception)

    return app
