import os
from datetime import datetime

import consul
from flask import Flask, request, jsonify

from db import db
from models import Following

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS', 'config.DevelopmentConfig'))

db.init_app(app)
if not app.config['DEBUG']:
    consul.register()


@app.route("/following/<id_>")
def get_following_of_user(id_):
    try:
        following = Following.query.filter_by(follower_id=id_).all()
        return jsonify([{'following_id': f.following_id} for f in following])
    except Exception as e:
        return (str(e))


@app.route("/followers/<id_>")
def get_followers_of_user(id_):
    try:
        following = Following.query.filter_by(following_id=id_).all()
        return jsonify([{'follower_id': f.follower_id} for f in following])
    except Exception as e:
        return (str(e))


@app.route("/follow", methods=['POST'])
def follow_user():
    follower_id = request.json.get('follower_id')
    following_id = request.json.get('following_id')
    try:
        following = Following(
            follower_id=follower_id,
            following_id=following_id,
            followed_at=datetime.now()
        )
        db.session.add(following)
        db.session.commit()
        return jsonify(success=True), 201
    except Exception as e:
        return (str(e))


@app.route("/<follower_id_>/unfollow/<following_id_>", methods=['DELETE'])
def unfollow_user(follower_id_, following_id_):
    try:
        following = Following.query.filter_by(following_id=following_id_, follower_id=follower_id_).first()
        db.session.delete(following)
        db.session.commit()
        return jsonify(success=True), 200
    except Exception as e:
        return (str(e))


if __name__ == '__main__':
    app.run()
