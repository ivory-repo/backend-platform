from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from models.user import UserModel

class UserResource(Resource):


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',
                        required=True,
                        type=str,
                        help='Username required')
        parser.add_argument('password',
                        required=True,
                        type=str,
                        help='Password required')
        parser.add_argument('active',
                        required=True,
                        type=bool,
                        help='Status required.')

        body = parser.parse_args()
        if UserModel.find_by_username(body['username']):
            return {'message': 'User with that username already exists.'}, 400
        
        new_user = UserModel(**body)
        try:
            new_user.save_to_db()
            return new_user.json(), 201
        except:
            return {'message': 'Internal server error.'}, 500
    
    @jwt_required()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',
                        required=True,
                        type=str,
                        help='Username required')
        body = parser.parse_args()
        user = UserModel.find_by_username(body['username'])
        if user:
            try:
                user.delete_from_db()
            except:
                return {'message': 'Internal server error.'}, 500
        return {'message': 'User was deleted.'}, 200

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username',
                        required=True,
                        type=str,
                        help='Username required')
        parser.add_argument('active',
                        required=True,
                        type=bool,
                        help='Status required.')
        body = parser.parse_args()
        user = UserModel.find_by_username(body['username'])

        if user and current_identity.username == user.username:
            user.active = body['active']
        else:
            return {'message': 'User not found.'}, 404
        
        try:
            user.save_to_db()
            return {'message': 'User state updated.'}, 200    
        except:
            return {'message': 'Internal server error.'}, 500


class UserList(Resource):

    def get(self):
        return {'users': [user.json() for user in UserModel.query.filter_by(active=True).all()]}
