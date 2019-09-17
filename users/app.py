import os
from datetime import datetime

import consul
from flask import Flask, request, jsonify

from db import db
from models import User

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS', 'config.DevelopmentConfig'))

db.init_app(app)
if not app.config['DEBUG']:
    consul.register()


@app.route("/add", methods=['POST'])
def add_user():
    name = request.json.get('name')
    username = request.json.get('username')
    try:
        user = User(
            name=name,
            username=username,
            created_at=datetime.now()
        )
        db.session.add(user)
        db.session.commit()
        return "User added. book id={}".format(user.id)
    except Exception as e:
        return (str(e))


@app.route("/")
def get_all():
    try:
        users = User.query.all()
        return jsonify([e.serialize() for e in users])
    except Exception as e:
        return (str(e))


@app.route("/<id_>")
def get_by_id(id_):
    try:
        user = User.query.filter_by(id=id_).first()
        return jsonify(user.serialize())
    except Exception as e:
        return (str(e))


if __name__ == '__main__':
    app.run()
