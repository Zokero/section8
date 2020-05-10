import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot left blank")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs store_id")
    @jwt_required()
    def get(self, name):
        # May be self. or Item.
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exist.".format(name)}, 400
        data = Item.parser.parse_args()
        # item = {'name': name, 'price': data['price']}
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except sqlite3.Error:
            return {"message": "An error occurred inserting the item."}, 500
        return item.json(), 201

    def delete(self, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()
        # return {'message': 'Item deleted'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

    def put(self, name):
        # data = Item.parser.parse_args()
        # item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price'])
        #
        # if item:
        #     updated_item.insert()
        # else:
        #     updated_item.update()
        # return updated_item.json()
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            # item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * from items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
        # connection.close()
        #
        # return {'items': items}
        items = ItemModel.query.all()

        # return {'items': [item.json() for item in item_list]}
        return {'items': list(map(lambda x: x.json(), items))}
