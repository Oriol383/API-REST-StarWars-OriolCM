"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Fav, Weapon
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def welcome_sw():
    return jsonify({"mensaje": "Bienvendio humano a una galaxia muy muy lejana..."})


@app.route('/sitemap', methods=['GET'])
def obtener_StarWars():
    return jsonify(sitemap)


@app.route('/sitemap', methods=['POST'])
def crear_post():
    nueva = request.get_json()
    nueva["id"] = len(sitemap) + 1
    sitemap.append(nueva)
    return jsonify(nueva), 201


@app.route('/sitemap/<int:id>', methods=['DELETE'])
def elimina_post(id):
    global sitemap
    sitemap = [t for t in sitemap if t["id"] != id]
    return jsonify({"mensaje": f"Post {id} eliminado"})


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@app.route('/planet', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200


@app.route('/character', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters]), 200


@app.route('/fav', methods=['GET'])
def get_favs():
    favs = Fav.query.all()
    return jsonify([fav.serialize() for fav in favs]), 200


@app.route('/weapon', methods=['GET'])
def get_weapons():
    weapons = Weapon.query.all()
    return jsonify([weapon.serialize() for weapon in weapons]), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == '__main__':
    app.run(debug=True)
