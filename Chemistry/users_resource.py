from flask import Flask, jsonify
from flask_restful import abort, Api, Resource

from data import db_session
from data.prsr import parser
from data.users import User

app = Flask(__name__)
api = Api(app)


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    users = session.query(User).get(news_id)
    if not users:
        abort(404, message=f"User {news_id} not found")


class UsersResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        users = session.query(User).get(news_id)
        return jsonify({'users': users.to_dict(
            only=('id', 'name', 'about', 'email', 'hashed_password', 'created_date',
                  'surname', 'age', 'position', 'speciality', 'address', 'modified_date'))})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        users = session.query(User).get(news_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'news': [item.to_dict(
            only=('title', 'content', 'user.name')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User(
            id=args['id'],
            name=args['name'],
            about=args['about'],
            email=args['email'],
            hashed_password=args['hashed_password'],
            surname=args['surname'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address']
        )
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})
