from flask_app import  db, jwt__
from flask import jsonify, request
from flask_app.models import User
from flask_app.utils import check_and_update, check_username, load_roles
from flask_jwt_extended import jwt_required, get_jwt_identity, create_refresh_token, create_access_token, get_jwt

def get_app():
    """
    Returns the Flask application object. 
    This function imports the Flask application object from the `flask_app` module and returns it.
    This must be done so there is no circular import problem.
    """
    from flask_app import app
    return app

app = get_app()

@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    claims = get_jwt()
    if claims["role"]=='user':
        return jsonify(error="you don't have permission to access this route")
    else:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200

@app.route('/users', methods=['POST'])
def add_new_user():
    new_user = request.get_json()
    validation = check_username(new_user['username'])
    if validation != None:
        return validation, 400
    new_user = User(username=new_user['username'], password=new_user['password'])
    new_user.set_password(new_user.password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 200

@app.route('/login', methods=["POST"])
def login():
    user = request.get_json()
    try:
        user_db = User.query.filter_by(username=user["username"]).first()
        if user_db.check_password(user["password" ]) == True:
            additional_claims = load_roles()
            if user["username"] != "doe.vidaesangue@gmail.com":
                access_token = create_access_token(identity=user_db.username, additional_claims=additional_claims["user"])
                refresh_token = create_refresh_token(identity=user_db.username, additional_claims=additional_claims["user"])
            else:
                access_token = create_access_token(identity=user_db.username, additional_claims=additional_claims["admin"])
                refresh_token = create_refresh_token(identity=user_db.username, additional_claims=additional_claims["admin"])
            return jsonify(access_token=access_token, refresh_token=refresh_token)
        else:
            return jsonify({"Erro": "Wrong password"}), 403
    except Exception as e:
        return jsonify({"Erro": "User not found"}), 404

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

@app.route('/users/<string:username>', methods=['GET'])
@jwt_required()
def get_user_by_username(username):
    claims = get_jwt()
    if claims["role"]=='user' and claims['sub'] != username:
        return jsonify(error="you don't have permission to access this route")
    else:
        user = User.query.filter_by(username=username).first()
        if user is None:
            return jsonify({"Error": "User not found"}), 404
        return jsonify(user.to_dict()), 200

@app.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user_by_id(id):
    claims = get_jwt()
    user = User.query.get(id)
    if claims["role"]=='user' and claims['sub'] != user.username:
        return jsonify(error="you don't have permission to access this route")
    if user is None:
        return jsonify({"Error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@app.route('/users/<string:username>', methods=['PUT'])
@jwt_required()
def update_user_by_username(username):
    claims = get_jwt()
    if claims["role"]=='user' and claims['sub'] != username:
        return jsonify(error="you don't have permission to access this route")
    else:
        user = User.query.filter_by(username=username).first()
        if user is None:
            return jsonify({"Error": "User not found"}), 404
        changed_password = request.get_json()
        user = check_and_update(user, **changed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 200


@app.route('/users/<string:username>', methods=['DELETE'])
@jwt_required()
def delete_user_by_username(username):
    claims = get_jwt()
    if claims["role"]=='user' and claims['sub'] != username:
        return jsonify(error="you don't have permission to access this route")
    else:
        user = User.query.filter_by(username=username).first()
        if user is None:
            return jsonify({"Error": "User not found"}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": "deleted user"}), 200