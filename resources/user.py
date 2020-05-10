import sqlite3
from flask_restful import Resource, reqparse
from controller.models.usermodel import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="You should fill username")
    parser.add_argument('password', type=str, required=True, help="You should type Your password")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with with user name: {} already exists".format(data['username'])}, 400

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # # NULL because autoincrement _id field in database
        # query = "INSERT INTO users VALUES (NULL, ?, ?)"
        # cursor.execute(query, (data['username'], data['password'],))
        #
        # connection.commit()
        # connection.close()
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201
