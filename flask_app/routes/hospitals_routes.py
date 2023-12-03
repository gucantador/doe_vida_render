from flask_app import  db, jwt__
from flask import jsonify, request
from flask_app.models import Hospitals
from flask_app.utils.utils import check_and_update_hospitals, jwt_handling, parse_hospital_name
from flask_jwt_extended import get_jwt
from flask_app.constants import errors, messages
from . import BaseResponse
from flask_jwt_extended import jwt_required

def get_app():
    from flask_app import app
    return app

app = get_app()

@app.route("/hospitals")
def get_hospitals():
  try:
    hospitals = Hospitals.query.all()
    response = BaseResponse(data=[hospital.to_dict() for hospital in hospitals], 
                            errors=None, message=messages["GENERAL_SUCCESS"])
    return response.response(), 200
  except Exception as e:
    print(e)
    response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
    return response.response()

@app.route("/hospitals/<hospital_name>")
@jwt_handling
def get_hospital_by_hospital_name(hospital_name):  #TODO parse hospital name to underline instead of blank spaces
  try:
    
    hospital = Hospitals.query.filter_by(hospital_name=hospital_name).first()
    claims = get_jwt()
    
    if claims["role"] == 'user' and claims['sub'] != hospital.username:
        response = BaseResponse(data=None, errors=errors["NOT_ACCESS_ERROR"], message=messages["NOT_ACCESS_ERROR_MESSAGE"])
        return response.response(), 403  
    
    if hospital is None:
      response = BaseResponse(data=None, errors=errors["NOT_FOUND"], message=messages["GENERAL_SUCCESS"])
      return response.response(), 404
    else:
      response = BaseResponse(data=hospital.to_dict(), errors=None, message=messages["GENERAL_SUCCESS"])
      return response.response(), 200
  except Exception as e:
    print(e)
    response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
    return response.response()
  
@app.route("/hospitals/<int:id>")
@jwt_handling
def get_hospital_by_id(id):
  try:
    claims = get_jwt()
    user = Hospitals.query.get(id)
    
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
    return response.response()

@app.route("/hospitals", methods=["POST"])
@jwt_handling
def post_hospital():
  try:
    claims = get_jwt()
    if claims["role"] == 'user':
          response = BaseResponse(data=None, errors=errors["NOT_ACCESS_ERROR"], message=messages["NOT_ACCESS_ERROR_MESSAGE"])
          return response.response(), 403 

    hospital_name = request.json["hospital_name"]
    city_name = request.json["city_name"]
    state = request.json["state"]

    hospital_name = request.json["hospital_name"]
    city_name = request.json["city_name"]
    state = request.json["state"]

    donations_orders = request.json.get("donations_orders")
    donations_orders_done = request.json.get("donations_orders_done")
    donations_orders_cancelled = request.json.get("donations_orders_cancelled")


    new_hospital = Hospitals(
      hospital_name=hospital_name,
      city_name=city_name,
      state=state,
      donations_orders=donations_orders,
      donations_orders_done=donations_orders_done,
      donations_orders_cancelled=donations_orders_cancelled,
    )

    db.session.add(new_hospital)
    db.session.commit()

    response = BaseResponse(data=new_hospital.to_dict(), errors=None, message=messages["GENERAL_SUCCESS"])

    return response.response(), 200
  
  except Exception as e:
    print(e)
    response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
    return response.response()

@app.route("/hospitals/<string:hospital_name>", methods=["PUT"])
@jwt_handling
def update_hospital_by_hospital_name(hospital_name):
  try:
    claims = get_jwt()
    if claims["role"] == 'user':
          response = BaseResponse(data=None, errors=errors["NOT_ACCESS_ERROR"], message=messages["NOT_ACCESS_ERROR_MESSAGE"])
          return response.response(), 403 
        
    hospital = Hospitals.query.filter_by(hospital_name=hospital_name).first()
    if hospital is None:
      response = BaseResponse(data=None, errors=errors["NOT_FOUND"], message=messages["GENERAL_SUCCESS"])
      return response.response(), 404
    
    changed_hospital_data = request.get_json()
    hospital = check_and_update_hospitals(hospital, **changed_hospital_data)
    db.session.add(hospital)
    db.session.commit()
    response = BaseResponse(data=hospital.to_dict(), errors=None, message=messages["GENERAL_SUCCESS"]), 200
    return response.response(), 200
  except Exception as e:
    print(e)
    response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
    return response.response()

@app.route("/hospitals/<string:hospital_name>", methods=["DELETE"])
@jwt_required()
def delete_hospital_by_hospital_name(hospital_name):
  try:
    claims = get_jwt()
    if claims["role"] == 'user':
          response = BaseResponse(data=None, errors=errors["NOT_ACCESS_ERROR"], message=messages["NOT_ACCESS_ERROR_MESSAGE"])
          return response.response(), 403 
    hospital = Hospitals.query.filter_by(hospital_name=hospital_name).first()
    if hospital is None:
      response = BaseResponse(data=None, errors=errors["NOT_FOUND"], message=messages["GENERAL_SUCCESS"])
      return response.response(), 404
    db.session.delete(hospital)
    db.session.commit()
    response = BaseResponse(data={"success": "Hospital deleted"}, errors=None, message=messages["GENERAL_SUCCESS"])
    return response.response(), 200
  
  except Exception as e:
    print(e)
    response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
    return response.response()