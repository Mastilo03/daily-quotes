from flask import Flask
from flask_pymongo import PyMongo

# Initialize extensions
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = 'mongodb://mongo:27017/quotes_db'

    # Initialize extensions with app
    mongo.init_app(app)

    # Register routes
    from app.routes import main
    app.register_blueprint(main)

    return app
