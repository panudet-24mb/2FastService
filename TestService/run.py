import random
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def myRandom():
    r1 = random.uniform(0, 10)

    return jsonify({'message': r1 })

if __name__ == '__main__':
    app.run( host= '0.0.0.0' , threaded=True, debug=True, port=5002) # running m2 on a different port than default 5000