from flask import Flask
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from jwt import DecodeError, ExpiredSignatureError
from flask_migrate import Migrate

from profiles.job import alert_report
from settings.config import DevelopmentConfig, ProductionConfig
from settings.exceptions import NotFoundException, BadRequestException, EmailException, InternalServerException,\
    handle_exception, handle_no_token, handle_invalid_header, handle_expires_token
from settings.layers.database import db
from settings.layers.scheduler import scheduler
from settings.layers.serialization import ma
from settings.layers.seeder import seeder
from settings.layers.jwt import jwt
from settings.layers.mail import mail
from auth.urls import auth_blueprint
from profiles.urls import profiles_blueprint
from medical_risks.urls import medical_risks_blueprint
from medical_monitoring.urls import medical_monitoring_blueprint


def create_app():
    app = Flask(__name__)
    config = ProductionConfig()
    app.config.from_object(config)
    db.init_app(app)
    Migrate(app, db)
    ma.init_app(app)
    # with app.app_context():
    #     db.create_all()
    seeder.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    app.app_context().push()
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id='alert_reports', func=alert_report, trigger="interval", hours=1)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(profiles_blueprint)
    app.register_blueprint(medical_risks_blueprint)
    app.register_blueprint(medical_monitoring_blueprint)
    app.register_error_handler(NoAuthorizationError, handle_no_token)
    app.register_error_handler(InvalidHeaderError, handle_invalid_header)
    app.register_error_handler(ExpiredSignatureError, handle_expires_token)
    app.register_error_handler(DecodeError, handle_invalid_header)
    app.register_error_handler(BadRequestException, handle_exception)
    app.register_error_handler(NotFoundException, handle_exception)
    app.register_error_handler(EmailException, handle_exception)
    app.register_error_handler(InternalServerException, handle_exception)

    return app
