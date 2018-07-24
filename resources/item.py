from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item (Resource):
    parser= reqparse.RequestParser()
    parser.add_argument("price", type=float, required=True,
                        help="This field cannot be left blank")
    parser.add_argument("store_id", type=int, required=True,
                        help="This field cannot be left blank")


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message":"item not found"},404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {"message":"an item with name '{}' already exists".format(name)},400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message":"an error occurred inserting the item."},500
        return item.json(),201




    def delete (self, name):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query ="DELETE FROM items WHERE name=?"
        # cursor.execute (query, (name,))
        # connection.commit()
        # connection.close()
        # return {"message":"item'{}' deleted".format(name)}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message":"item is deleted"}


    def put (self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price=data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json()



class ItemList (Resource):
    def get (self):
        # item_list= ItemModel.query.all()
        # res = []
        # for item in item_list:
        #     res.append(item.json())
        # return {"items":res}
        # or
        # res = list(map(lambda x: x.json(), ItemModel.query.all()))
        # or
        res = [item.json() for item in ItemModel.find_all()]
        return {'items':res}
