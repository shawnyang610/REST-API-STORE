import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')# can be changed to any kind of sql
app.config['SQLAlchemy_TRACK_MODIFICATIONS']=False
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']
app.secret_key = 'MyKey'
api = Api(app)


# #comment out the following block to run on ubuntu
# #uwsgi will run the app from run.py instead
# #uncomment the block only when trying to run on localhost by
# #running app.py directly
# @app.before_first_request
# def create_tables():
#     db.create_all()


jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin":True}
    return {"is_admin":False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify(
        {
            "description": "The token has expired.",
            "error":"token_expired"
        }
    ),401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify(
        {
            "description":"Signature verification failed.",
            "error":"invalid_token"
        }
    ),401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify(
        {
            "description":"The token is not fresh.",
            "error":"fresh_token_required"
        }
    ),401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify(
        {
            "description":"Token not fresh.",
            "error":"fresh token required"
        }
    ),401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify(
        {
            "description":"The token has been revoked.",
            "error":"token_revoked"
        }
    ),401


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, "/refresh")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
