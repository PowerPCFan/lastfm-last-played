# stdlib
import os

# 3rd party
from flask import Flask, Blueprint
from flask_cors import CORS

# local
import modules.latest_songs as latest_songs
import modules.healthcheck as healthcheck

def create_healthcheck_blueprint():
    blueprint = Blueprint('Health Check Blueprint', __name__)
    blueprint.route('/')(healthcheck.route)
    return blueprint

def create_songs_blueprint():
    blueprint = Blueprint('Songs Blueprint', __name__)
    blueprint.route('/<user>', methods=['GET'])(latest_songs.route)
    return blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(create_healthcheck_blueprint())
app.register_blueprint(create_songs_blueprint())
