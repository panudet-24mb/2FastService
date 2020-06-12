from flask import Flask, request, jsonify, make_response, Blueprint
import uuid
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import CombinedMultiDict
import jwt
import json
from functools import wraps
from app.Client.models import User
from app import Secret_key, EndPoint
import urllib 
import os
import requests

ClientService = Blueprint("ClientService", __name__, url_prefix=EndPoint + "/v1")


def ListMicroService():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "", "microservice.json")
    data = json.load(open(json_url))
    return data


Service = ListMicroService()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, Secret_key)
            current_user = User.query.filter_by(public_id=data["public_id"]).first()
        except Exception as e:

            return jsonify({"message": "Invalid Token"}), 401

        return f(current_user, *args, **kwargs)

    return decorated




@ClientService.route("/", methods=["GET"])
def DefaultGateway():
    return jsonify({"Code": "0001", "Message": "Welcome to 2Fast Gateway"})


@ClientService.route("/reverse_random/<string:string>", methods=["GET"])
def reverse(string):
    content = urllib.request.urlopen("http://localhost:5002").read().decode("utf-8")
    string = string[::-1]
    print(content)
    return jsonify({"message": string, "random": json.loads(content)["message"]})


@ClientService.route("/GetUserData", methods=["GET"])
@token_required
def ClientCheckvalidJWT(current_user):
    public_id = current_user.public_id
    username = current_user.username
    return jsonify({"public_id": public_id, "username": username})



@ClientService.route("/<string:ServiceName>/<string:route>",methods=["GET", "POST", "PUT", "DELETE"])
def MainGateWay(ServiceName, route  ):
    method = request.method
    if ValidServiceName(ServiceName) != True:
        return jsonify({"Code": "0002", " Message": "No ServiceName"}),403
    if GetChildDetail(ServiceName, route) == False:
        return jsonify({"Code": "0003", " Message": "No RouteName or It not Alive"}) ,403
    ChildDetail = GetChildDetail(ServiceName, route)
    if method != isMethod(ChildDetail):
        return jsonify({"Code": "0004", " Message": "MethodNotAllowed"}), 405
    Path = isPath(ChildDetail)
    if method == "POST":
        data_json = request.args.to_dict()
        res = requests.post(Path + "/" + ServiceName + "/" + route, json=data_json,)
        return jsonify(res.json()) ,res.status_code
    if method == "GET":
        data_json = request.args.to_dict()
        res = requests.get(Path + "/" + ServiceName + "/" + route, json=data_json,)
        return jsonify(res.json()) ,res.status_code
    if method == "PUT":
        data_json = request.args.to_dict()
        res = requests.put(Path + "/" + ServiceName + "/" + route, json=data_json,)
        return jsonify(res.json()) ,res.status_code
    if method == "DELETE":
        data_json = request.args.to_dict()
        res = requests.delete(Path + "/" + ServiceName + "/" + route, json=data_json,)
        return jsonify(res.json()) ,res.status_code
    return jsonify({"Code": "0005" , " Message": "Not Condition Matchwith"}), 405
 

def ValidServiceName(ServiceName):
    try:
        GetMicroService = Service["MicroService"][0][ServiceName]
        return True
    except Exception as e:
        return False


def GetChildDetail(ServiceName, ChildName):
    if ValidServiceName(ServiceName) != True:
        return False
    else:
        try : 
            GetMicroService = Service["MicroService"][0][ServiceName][0][ChildName]
        except:
            return False
        CheckChildIsAlive = isAlive(GetMicroService)
        if CheckChildIsAlive == 1:
            return GetMicroService
        else:
            return False


def isAlive(ChildData):
    ChildNodeData = ChildData[0]["alive"]
    return ChildNodeData
def isMethod(ChildData):
    ChildNodeData = ChildData[0]["method"]
    return ChildNodeData

def isPath(ChildData):
    ChildNodeData = ChildData[0]["Path"]
    return ChildNodeData



# print(GetChildDetail('UserService' , 'UserGet'))

