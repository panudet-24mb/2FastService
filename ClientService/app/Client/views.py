from flask import Flask, request, jsonify, make_response , Blueprint
import uuid
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import json
from functools import wraps
from app.Client.models import User
from app import Secret_key, EndPoint
import urllib


ClientService = Blueprint('ClientService', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, Secret_key)
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except Exception as e:
    
            return jsonify({'message' : 'Invalid Token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@ClientService.route('/', methods=['GET'])
def DefaultGateway():
  return jsonify({"Code": "0001", "Message": "Welcome to 2Fast Gateway"})

@ClientService.route(EndPoint+'/reverse_random/<string:string>', methods=['GET'])
def reverse(string):
    content = urllib.request.urlopen('http://localhost:5002').read().decode('utf-8')
    string = string[::-1]
    return jsonify({'message': string, 'random' : json.loads(content)['message']})

@ClientService.route(EndPoint, methods=['GET'])
@token_required
def ClientCheckvalidJWT(current_user):
  public_id = current_user.public_id
  username = current_user.username
  return jsonify({"public_id": public_id, "username": username})

  
  

    
