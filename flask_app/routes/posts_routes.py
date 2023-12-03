from flask_app import app, db
from flask_app.models import Posts
from flask import jsonify, request
from datetime import datetime
from flask_app import  db, jwt__
from flask import jsonify, request
from flask_app.models import User, Donation_order
from flask_app.utils.utils import check_and_update, check_username, load_roles, jwt_handling, create_token_and_send_email, can_donate
from flask_app.constants import errors, messages
from flask_jwt_extended import jwt_required, get_jwt_identity, create_refresh_token, create_access_token, get_jwt
from . import BaseResponse
from flask_app.constants import errors, messages
import base64
from flask_jwt_extended import jwt_required


@app.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    try:
        data = request.get_json()
        new_post = Posts(title=data['title'], content=data['content'], user_id=data['user_id'])
        db.session.add(new_post)
        db.session.commit()
        response = BaseResponse(data=new_post.to_dict(), errors=None, message=messages["GENERAL_SUCCESS"])
        return response.response(), 200
    except Exception as e:
        print(e)
        response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
        return response.response(), 500

# Example route for getting all posts
# Example route for getting all posts
@app.route('/posts', methods=['GET'])
def get_all_posts():
    try:
        posts = Posts.query.all()
        response = BaseResponse(data=[post.to_dict() for post in posts], errors=None, message=messages["GENERAL_SUCCESS"])
        return response.response(), 200
    except Exception as e:
        print(e)
        response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
        return response.response(), 500

# Example route for getting a specific post by ID
@app.route('/posts/<int:id>', methods=['GET'])
@jwt_required()
def get_post_by_id(id):
    try:
        post = Posts.query.get(id)
        if post is None:
            response = BaseResponse(data=None, errors=errors["NOT_FOUND"], message=messages["GENERAL_SUCCESS"])
            return response.response(), 404
        response = BaseResponse(data=post.to_dict(), errors=None, message=messages["GENERAL_SUCCESS"])
        return response.response(), 200
    except Exception as e:
        print(e)
        response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
        return response.response(), 500


@app.route('/posts/<int:id>', methods=['PUT'])
@jwt_required()
def update_post_by_id(id):
    try:
        post = Posts.query.get(id)
        if post is None:
            response = BaseResponse(data=None, errors=errors["NOT_FOUND"], message=messages["GENERAL_SUCCESS"])
            return response.response(), 404
        updated_data = request.get_json()
        post.title = updated_data.get('title', post.title)
        post.content = updated_data.get('content', post.content)
        db.session.commit()
        response = BaseResponse(data=post.to_dict(), errors=None, message=messages["GENERAL_SUCCESS"])
        return response.response(), 200
    except Exception as e:
        print(e)
        response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
        return response.response(), 500

# Example route for deleting a specific post by ID
@app.route('/posts/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post_by_id(id):
    try:
        post = Posts.query.get(id)
        if post is None:
            response = BaseResponse(data=None, errors=errors["NOT_FOUND"], message=messages["GENERAL_SUCCESS"])
            return response.response(), 404
        db.session.delete(post)
        db.session.commit()
        response = BaseResponse(data=None, errors=None, message=messages["GENERAL_SUCCESS"])
        return response.response(), 200
    except Exception as e:
        print(e)
        response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
        return response.response(), 500

