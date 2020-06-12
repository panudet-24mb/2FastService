import random
from flask import Flask, jsonify, request
import json

app = Flask(__name__)


@app.route('/TestService/getTest', methods=['GET'])
def myRandom():
    r1 = random.uniform(0, 10)
    
    return jsonify('dasdasd') , 200
    

@app.route('/TestService/PostTest', methods=['POST'])
def myRandom2():
    
    data = request.get_json()

    return jsonify(data) ,200


if __name__ == '__main__':
    app.run( host= '0.0.0.0' , threaded=True, debug=True, port=5002) # running m2 on a different port than default 5000