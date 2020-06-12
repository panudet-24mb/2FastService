import random
from flask import Flask, jsonify, request ,make_response
import requests, json

app = Flask(__name__)


@app.route('/TestService/GetTest', methods=['GET'])
def myRandom():
    return jsonify(Response = "da") , 200
    

@app.route('/TestService/PostTest', methods=['POST'])
def myRandom2():
    
    data = request.get_json()
    return jsonify(
		Response=data
	),200

 

if __name__ == '__main__':
    app.run( host= '0.0.0.0' , threaded=True, debug=True, port=5002) # running m2 on a different port than default 5000