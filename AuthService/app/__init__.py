from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql://admin:Passw0rd_2020@54.254.141.16/2Fast'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Secret_key = 'thisissecret'
db = SQLAlchemy(app)
ma = Marshmallow(app)


from app.Auth.views import AuthService
app.register_blueprint(AuthService)