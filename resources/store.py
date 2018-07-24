from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.jason()
        return {"message":"store not found"},404

    def post (self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message":"the store {} already exists".format(name)},400

        store = StoreModel(name)
        try:
            store.save_to_db()
            return {"message":"store created"}
        except:
            return {"message":"an error occured while creating the store"},500

    def delete (self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()
        return {'message':'Store deleted'}


class StoreList(Resource):
    def get(self):
        storelist = [store.json() for store in StoreModel.find_all()]
        return {"stores":storelist}
