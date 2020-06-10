from flask import Flask, request, jsonify, make_response , Blueprint
import uuid
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import json
from functools import wraps
from app.Client.models import User
from app import Secret_key


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


@ClientService.route('/Client', methods=['GET'])
@token_required
def ClientCheckvalidJWT(current_user):
  public_id = current_user.public_id
  username = current_user.username
  return jsonify({"public_id":public_id , "username":username})
    
