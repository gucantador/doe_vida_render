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
    try:
        claims = get_jwt()
        if claims["role"]=='user':
            response = BaseResponse(Data=None, errors=errors["NOT_ACCESS_ERROR"], message=messages["NOT_ACCESS_ERROR_MESSAGE"])
            return response.response(), 200
        else:
            users = User.query.all()
            response = BaseResponse(data=[user.to_dict() for user in users], errors=None, message=messages["LIST_USERS"])
            return response.response(), 200
    except Exception as e:
        print(e)
        response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
        return response.response(), 500

@app.route('/users', methods=['POST'])
def add_new_user():
    try:
        new_user = request.get_json()
        validation = check_username(new_user['username'])
        if validation != None:
            response = BaseResponse(data=None, errors=errors["EMAIL_ERROR"], message=validation)
            return jsonify(response.response), 400
        new_user = User(username=new_user['username'], password=new_user['password'])
        new_user.set_password(new_user.password)
        db.session.add(new_user)
        db.session.commit()
        response = BaseResponse(data=new_user.to_dict(), errors=None, message=messages["USER_CREATED"])
        return response.response(), 200
    except Exception as e:
        print(e)
        response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
        return response.response()
    
@app.route('/users/password_reset', methods=['POST'])
def password_reset():
    try:
        user_data = request.get_json()
        validation = check_username(user_data['username'])
        if validation != None:
            response = BaseResponse(data=None, errors=errors["EMAIL_ERROR"], message=validation)
            return jsonify(response.response), 400
        user = User.query.filter_by(username=user_data['username']).first()  # TODO testar o que acontece se nao existir o usuario
        token = create_token_and_send_email(email=user_data['username'])
        user.set_token(token)
        db.session.add(user)
        db.session.commit()
        response = BaseResponse(data='Email enviado com sucesso', errors=None, message=messages["GENERAL_SUCCESS"])
        return response.response(), 200
    except Exception as e:
        print(e)
        response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
        return response.response()

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
                tokens = dict(access_token=access_token, refresh_token=refresh_token)
            else:
                access_token = create_access_token(identity=user_db.username, additional_claims=additional_claims["admin"])
                refresh_token = create_refresh_token(identity=user_db.username, additional_claims=additional_claims["admin"])
                tokens = dict(access_token=access_token, refresh_token=refresh_token)
            response = BaseResponse(data=tokens, errors=None, message=messages["SUCCESS_TOKENS"])
            return response.response()
        else:
            response = BaseResponse(data=None, errors=errors["WRONG_PASSWORD"], message=messages["WRONG_PASSWORD"])
            return response.response, 403
    except Exception as e:
        print(e)
        response = BaseResponse(data=None, errors=errors["NOT_FOUND"], message=messages["NOT_FOUND"])
        return response.response(), 404
    
@app.route('/users/token_validation', methods=["POST"])
def token_validation():
    user = request.get_json()
    try:
        user_db = User.query.filter_by(username=user["username"]).first()
        if user_db.check_token(user["token" ]) == True:
            additional_claims = load_roles()
            if user["username"] != "doe.vidaesangue@gmail.com":
                access_token = create_access_token(identity=user_db.username, additional_claims=additional_claims["user"])
                refresh_token = create_refresh_token(identity=user_db.username, additional_claims=additional_claims["user"])
                tokens = dict(access_token=access_token, refresh_token=refresh_token)
            else:
                access_token = create_access_token(identity=user_db.username, additional_claims=additional_claims["admin"])
                refresh_token = create_refresh_token(identity=user_db.username, additional_claims=additional_claims["admin"])
                tokens = dict(access_token=access_token, refresh_token=refresh_token)
            response = BaseResponse(data=tokens, errors=None, message=messages["SUCCESS_TOKENS"])
            return response.response()
        else:
            response = BaseResponse(data=None, errors=errors["WRONG_PASSWORD"], message=messages["WRONG_PASSWORD"])
            return response.response, 403
    except Exception as e:
        print(e)
        response = BaseResponse(data=None, errors=errors["NOT_FOUND"], message=messages["NOT_FOUND"])
        return response.response(), 404

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        data = dict(access_token=access_token)
        response = BaseResponse(data=data, errors=None, message=messages["GENERAL_SUCCESS"])
        return response.response(), 500
    except:
        response = BaseResponse(data=None, error=errors["REFRESH_ERROR"], message=messages["REFRESH_ERROR"])
    
@app.route('/users/<string:username>', methods=['GET'])
@jwt_required()
def get_user_by_username(username):
    try:
        claims = get_jwt()
        if claims["role"]=='user' and claims['sub'] != username:
            response = BaseResponse(data=None, errors=errors["NOT_ACCESS_ERROR"], message=messages["NOT_ACCESS_ERROR_MESSAGE"])
            return response.response()
        else:
            user = User.query.filter_by(username=username).first()
            if user is None:
                response = BaseResponse(data=None, errors=errors["NOT_FOUND"], message=messages["NOT_FOUND"])
                return response.response(), 404
            response = BaseResponse(data=user.to_dict(), errors=None, message=messages["GENERAL_SUCCESS"])
            return response.response(), 200
    except Exception as e:
        print(e)
        response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
        return response.response(), 500

@app.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user_by_id(id):
    try:
        claims = get_jwt()
        user = User.query.get(id)
        
        if claims["role"] == 'user' and claims['sub'] != user.username:
            response = BaseResponse(data=None, errors=errors["NOT_ACCESS_ERROR"], message=messages["NOT_ACCESS_ERROR_MESSAGE"])
            return response.response(), 403  
        if user is None:
            response = BaseResponse(data=None, errors=errors["NOT_FOUND"], message=messages["NOT_FOUND"])
            return response.response(), 404  

        response = BaseResponse(data=user.to_dict(), errors=None, message=messages["GENERAL_SUCCESS"])
        return response.response(), 200 
    except Exception as e:
        print(e)
        response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
        return response.response(), 500

@app.route('/users/<string:username>', methods=['PUT'])
@jwt_required()
def update_user_by_username(username):
    claims = get_jwt()
    if claims["role"]=='user' and claims['sub'] != username:
        response = BaseResponse(data=None, errors=errors["NOT_ACCESS_ERROR"], message=messages["NOT_ACCESS_ERROR_MESSAGE"])
        return response.response(), 403 
    else:
        user = User.query.filter_by(username=username).first()
        if user is None:
            response = BaseResponse(data=None, errors=errors["NOT_FOUND"], message=messages["NOT_FOUND"])
            return response.response(), 404  
        try:
            changed_password = request.get_json()
            user = check_and_update(user, **changed_password)
            db.session.add(user)
            db.session.commit()
            response = BaseResponse(data=user.to_dict(), errors=None, message=messages["GENERAL_SUCCESS"])
            return response.response(), 200
        except Exception as e:
            print(e)
            response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
            return response.response(), 500


@app.route('/users/<string:username>', methods=['DELETE'])
@jwt_required()
def delete_user_by_username(username):
    try:
        claims = get_jwt()
        if claims["role"]=='user' and claims['sub'] != username:
            response = BaseResponse(Data=None, errors=errors["NOT_ACCESS_ERROR"], message=messages["NOT_ACCESS_ERROR_MESSAGE"])
            return jsonify(response.response())
        else:
            user = User.query.filter_by(username=username).first()
            if user is None:
                response = BaseResponse(data=None, errors=errors["NOT_FOUND"], message=messages["NOT_FOUND"])
                return response.response(), 404  
            db.session.delete(user)
            db.session.commit()
            response = BaseResponse(data=user.to_dict(), errors=None, message=messages["GENERAL_SUCCESS"])
            return response.reponse(), 200
    except Exception as e:
        print(e)
        response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
        return response.response(), 500

@app.route('/users/<string:username>/matches', methods=['GET'])
@jwt_required()
def get_matches(username):
    try:
        claims = get_jwt()
        if claims["role"]=='user' and claims['sub'] != username:
            response = BaseResponse(data=None, errors=errors["NOT_ACCESS_ERROR"], message=messages["NOT_ACCESS_ERROR_MESSAGE"])
            return response.response()
        else:
            user = User.query.filter_by(username=username).first()
            if user is None:
                response = BaseResponse(data=None, errors=errors["NOT_FOUND"], message=messages["NOT_FOUND"])
                return response.response(), 404
            blood_type = user.blood_type
            print(blood_type)
            user_city = user.city
            blood_types = can_donate(blood_type)
            matching_donations = db.session.query(Donation_order).filter(
                Donation_order.blood_type.in_(blood_types),
                Donation_order.city_name == user_city,
                Donation_order.status == "open"
            ).all()
            response = BaseResponse(data=[match.to_dict() for match in matching_donations], errors=None, message=messages["GENERAL_SUCCESS"])
            return response.response(), 200
    except Exception as e:
        print(e)
        response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
        return response.response(), 500


@app.route('/users/upload_photo/<string:username>', methods=['PUT'])
def upload_photo(username):

    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nome de arquivo vazio'}), 400

    # Salva o arquivo no servidor
    encoded_image = base64.b64encode(file.read()).decode('utf-8')
    user = User.query.filter_by(username=username).first()
    user.photo = encoded_image
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Arquivo recebido com sucesso'}), 200
