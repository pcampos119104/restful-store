from models.item import ItemModel
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
from schemas.item import ItemSchema

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200
        return {'message': 'not find'}, 404

    @fresh_jwt_required
    def post(self, name):
        item_json = request.get_json()
        item_json["name"] = name
        item = item_schema.load(item_json)

        if ItemModel.find_by_name(item.name):
            return {'message': 'Item exists'}, 400

        try:
            item.save_to_db()
        except:
            return {'message': 'Server problem'}, 500

        return item_schema.dump(item), 201

    @fresh_jwt_required
    def put(self, name):
        item_json = request.get_json()
        item_json["name"] = name
        data_item = item_schema.load(item_json)

        item = ItemModel.find_by_name(data_item.name)
        if item:
            item.price = data_item.price
        else:
            item = data_item

        try:
            item.save_to_db()
        except:
            return {'message': 'Server problem'}, 500

        return item_schema.dump(item)

    @fresh_jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item_schema.dump(ItemModel.find_all())]
        if user_id:
            return {'items': items}
        return {'items': [item['name'] for item in items],
                'message': 'More data if log in'}
