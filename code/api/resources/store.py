from flask_restful import Resource, reqparse
from models.store import StoreModel
from schemas.store import StoreSchema
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity, fresh_jwt_required

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)

class Store(Resource):
    @jwt_required
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store)
        return {'message': 'Store not found'}, 404

    @fresh_jwt_required
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'Store exists'}, 400
        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {'message': 'Server problem'}, 500

        return store_schema.dump(store), 201

    @fresh_jwt_required
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted'}

class StoreList(Resource):
    @jwt_optional
    def get(self):
    #    user_id = get_jwt_identity()
    #    stores = [store.json() for store in StoreModel.find_all()]
    #    if user_id:
    #        return {'stores': stores}
        return {'stores': store_list_schema.dump(StoreModel.find_all())}
