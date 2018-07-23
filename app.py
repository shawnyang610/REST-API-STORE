from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from security import authentication, identify
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'# can be changed to any kind of sql
app.config['SQLAlchemy_TRACK_MODIFICATIONS']=False
app.secret_key = 'MyKey'
jwt = JWT(app, authentication, identify)
api = Api(app)



api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
