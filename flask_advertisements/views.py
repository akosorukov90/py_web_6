from flask import request, jsonify
from flask.views import MethodView

from app import app
from validator import validate, validate_auth
from models import Advertisement, User
from schema import USER_CREATE, ADVERTISEMENT_CREATE


class AdvertisementView(MethodView):
    def get(self, advertisement_id):
        advertisement = Advertisement.by_id(advertisement_id)
        return jsonify(advertisement.to_dict())

    @validate('json', ADVERTISEMENT_CREATE)
    def post(self):
        advertisement = Advertisement(**request.json)
        validate_auth(request, advertisement)
        advertisement.add()
        return jsonify(advertisement.to_dict())

    @validate('json', ADVERTISEMENT_CREATE)
    def put(self, advertisement_id):
        advertisement = Advertisement.by_id(advertisement_id)
        validate_auth(request, advertisement)
        advertisement.title = request.json['title']
        advertisement.description = request.json['description']
        advertisement.add()
        return jsonify(advertisement.to_dict())

    def delete(self, advertisement_id):
        advertisement = Advertisement.by_id(advertisement_id)
        validate_auth(request, advertisement)
        advertisement.delete()
        return "Объявление удалено"


class UserView(MethodView):
    def get(self, user_id):
        user = User.by_id(user_id)
        return jsonify(user.to_dict())

    @validate('json', USER_CREATE)
    def post(self):
        user = User(**request.json)
        user.set_password(request.json['password'])
        user.add()
        return jsonify(user.to_dict())


app.add_url_rule(
    '/advertisements/<int:advertisement_id>',
    view_func=AdvertisementView.as_view('advertisement_get'),
    methods=['GET', ]
)
app.add_url_rule(
    '/advertisements/',
    view_func=AdvertisementView.as_view('advertisement_create'),
    methods=['POST', ]
)
app.add_url_rule(
    '/advertisements/<int:advertisement_id>',
    view_func=AdvertisementView.as_view('advertisement_put'),
    methods=['PUT', ]
)
app.add_url_rule(
    '/advertisements/<int:advertisement_id>',
    view_func=AdvertisementView.as_view('advertisement_delete'),
    methods=['DELETE', ]
)
app.add_url_rule(
    '/users/<int:user_id>',
    view_func=UserView.as_view('user_get'),
    methods=['GET', ]
)
app.add_url_rule(
    '/users/',
    view_func=UserView.as_view('user_create'),
    methods=['POST', ]
)
