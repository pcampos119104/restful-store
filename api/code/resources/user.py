from flask_restful import Resource
from flask import request, current_app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
from schemas.user import UserSchema

user_schema = UserSchema()

class UserRegister(Resource):
    def post(self):
        current_app.logger.info('post user')
        user = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            return {'message': 'User exists'}, 400

        try:
            user.save_to_db()
        except Exception as e:
            current_app.logger.debug(e)
            return {'message': 'Server error'}, 500 

        return {'message': 'User created'}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not find'}, 404
        return user_schema.dump(user)

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not find'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        current_app.logger.info('User login')
        user_data = user_schema.load(request.get_json())
        current_app.logger.debug(f'user: {user_schema.dump(user_data)}')
        user = UserModel.validate_user_password(user_data.username, user_data.password)
        current_app.logger.debug(f'Retrieve user from db: {user_schema.dump(user)}')
        
        if user:
            current_app.logger.info('user password accepted')
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        current_app.logger.info('user password invalid')
        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'return': 'Logged out'}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}
