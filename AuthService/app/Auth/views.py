from flask import Flask, request, jsonify, make_response ,Blueprint
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from app.Auth.models import User
from app import Secret_key
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'thisissecret'
# app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql://root:@localhost/2fast'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# ma = Marshmallow(app)
AuthService = Blueprint('AuthService', __name__)
# db.create_all()

@AuthService.route('/login', methods=['POST'] )
def login():
    data = request.get_json()

    if not data or not data['username'] or not data['password']:
        return jsonify({ "Code" : "401_1" , 'Error' : "Username or password is empty " }  ) , 401
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({"Code": "401_2", 'Error': "Username is incorrect "}), 401

    if check_password_hash(user.password, data['password']):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=1440)}, Secret_key)

        return jsonify({'token':token.decode('UTF-8')}), 200
    else:
        return jsonify({"Code": "401_3", 'Error': "Password is incorrect "}), 401


    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


    
