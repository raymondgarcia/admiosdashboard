#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, Resource, reqparse, fields, marshal
from document import Service
from enum import Enum

app = Flask(__name__)
api = Api(app)

service = Service()

class Status(Enum):
    NOT_FOUND = '{"status" : "Object not found"}'

class TeamListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('client',  help='Client cannot be converted', location = 'json')
        self.reqparse.add_argument('tech',  help='Tech cannot be converted', location = 'json')
        self.reqparse.add_argument('contract', help='Contract cannot be converted', location = 'json')
        self.reqparse.add_argument('developers', help='Developers cannot be converted', location = 'json')
        super(TeamListAPI, self).__init__()

    def post(self):
        team = request.get_json()
        result = service.save(team=team)
        return result.to_json(), 201
        pass

    def get(self):
        try:
            return service.list(), 201
        except:
            return Status.NOT_FOUND.value, 404


class TeamAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(TeamAPI, self).__init__()

    def get(self, id):
        try:
            return service.get(id).to_json(), 201
        except:
            return Status.NOT_FOUND.value, 404

    def put(self, id):
        team = request.get_json()
        result = service.update(team=team, id=id)
        return result.to_json(), 201
        pass

    def delete(self, id):
        try:
            service.delete(id)
        except:
            return Status.NOT_FOUND.value, 404


api.add_resource(TeamListAPI, '/api/v1.0/teams', endpoint = 'teams')
api.add_resource(TeamAPI, '/api/v1.0/teams/<string:id>', endpoint = 'team')

if __name__ == '__main__':
    app.run(debug=True, port=5001)