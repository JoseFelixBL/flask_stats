""" Consultar bases de datos de JoyasTV desde el navegador usando Flask """
import os
from flask import Flask

from dotenv import load_dotenv


def create_app():
    """Create and configure the app"""
    app = Flask(__name__, instance_relative_config=True)

    load_dotenv()

    app.config.from_mapping(
        # FROM_EMAIL=os.environ.get('FROM_EMAIL'),
        # SENDGRID_KEY=os.environ.get('SENDGRID_API_KEY'),
        # SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE'),
    )

    from . import show
    app.register_blueprint(show.bp)

    # print(app.url_map)  # Para ver las reglas registradas en la app

    return app
