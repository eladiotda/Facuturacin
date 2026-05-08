from flask import Flask
from werkzeug.exceptions import BadRequest

from app.api.responses import error_response
from app.controllers import ConflictError, NotFoundError, ValidationError

from app.extensions import db, migrate
from app.routes import clientes_bp, facturas_bp, productos_bp
from config.settings import config_by_name


def create_app(config_name: str = "development") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    register_extensions(app)
    register_models()
    register_blueprints(app)
    register_error_handlers(app)

    return app


def register_extensions(app: Flask) -> None:
    """Inicializa ORM y migraciones para la aplicacion."""

    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app: Flask) -> None:
    """Registra blueprints de la API."""

    app.register_blueprint(clientes_bp)
    app.register_blueprint(facturas_bp)
    app.register_blueprint(productos_bp)


def register_models() -> None:
    """Importa modelos para registrarlos en el metadata del ORM."""

    from app import models  # noqa: F401


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(BadRequest)
    def bad_request(error):
        return error_response("Solicitud invalida", 400)

    @app.errorhandler(ValidationError)
    def validation_error(error):
        return error_response(str(error), 400)

    @app.errorhandler(ConflictError)
    def conflict_error(error):
        return error_response(str(error), 409)

    @app.errorhandler(NotFoundError)
    def not_found_domain_error(error):
        return error_response(str(error), 404)

    @app.errorhandler(404)
    def not_found(error):
        return error_response("Recurso no encontrado", 404)

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return error_response("Error interno del servidor", 500)
