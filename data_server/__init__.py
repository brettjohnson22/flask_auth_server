import os
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS, cross_origin

db = MongoEngine()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['MONGODB_SETTINGS'] = {
        'host': 'mongodb+srv://admin:admin@cluster0.folri.mongodb.net/data_server?retryWrites=true&w=majority',
    }

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
