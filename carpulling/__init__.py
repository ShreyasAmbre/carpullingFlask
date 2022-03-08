from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_marshmallow import Marshmallow



app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carpulling.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

from carpulling import routes


@app.route('/')
def index():
    return 'Web App with Python Flask!'