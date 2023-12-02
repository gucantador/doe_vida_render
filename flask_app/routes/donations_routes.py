from flask_app import  db, jwt__
from flask import jsonify, request
from flask_app.models import Donation_order, Hospitals, User
from flask_app.utils.utils import check_and_update_donations, check_hospital_db, check_and_update_donation_status, jwt_handling
from flask_jwt_extended import jwt_required, get_jwt
from . import BaseResponse
from flask_app.constants import errors, messages

def get_app():
    from flask_app import app
    return app

app = get_app()

@app.route("/donations_orders")
def get_donations_orders():
  try:
    donations_orders = Donation_order.query.all()
    response = BaseResponse(data=[donation_order.to_dict() for donation_order in donations_orders],
                            errors=None, message=messages["GENERAL_SUCCESS"])
    return response.response(), 200
  except Exception as e:
    print(e)
    response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
    return response.response()

@app.route("/donations_orders/<int:donation_order_id>", methods=["GET"])
def get_donation_order_by_id(donation_order_id):
  try:
    donation_order = Donation_order.query.get(donation_order_id)
    if donation_order is None:
        response = BaseResponse(data=None, errors=errors["NOT_FOUND"], message=messages["NOT_FOUND"])
        return response.response(), 404  
    else:
      response = BaseResponse(data=donation_order.to_dict(), errors=None, message=messages["GENERAL_SUCCESS"])
      return response.response(), 200
  except Exception as e:
    print(e)
    response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
    return response.response()

@app.route("/donations_orders", methods=["POST"])
@jwt_handling
def post_donation_order():
  try:
    patient_name = request.json["patient_name"]
    blood_type = request.json["blood_type"]
    description = request.json["description"]
    qty_bags = request.json["qty_bags"]
    hospital = request.json["hospital"]
    requester = request.json["requester"]

    requester = User.query.get(requester)
    claims = get_jwt()
    if claims["role"]=='user' and claims['sub'] != requester.username:
      response = BaseResponse(data=None, errors=errors["NOT_ACCESS_ERROR"], message=messages["NOT_ACCESS_ERROR_MESSAGE"])
      return response.response(), 403

    hospital = Hospitals.query.filter_by(hospital_name=hospital).first()
    if hospital.donations_orders is None:
      hospital.donations_orders = 1
    else:
      hospital.donations_orders = hospital.donations_orders + 1
    db.session.add(hospital)
    db.session.commit()
    
    new_donation_order = Donation_order(
      patient_name=patient_name,
      blood_type=blood_type,
      description=description,
      qty_bags=qty_bags,
      hospitals=hospital,
      user=requester,
      city_name=hospital.city_name
    )

    db.session.add(new_donation_order)
    db.session.commit()
    
    response = BaseResponse(data=new_donation_order.to_dict(), errors=None, message=messages["GENERAL_SUCCESS"])

    return response.response(), 200
  
  except Exception as e:
    print(e)
    response = BaseResponse(data=None, errors=errors["INTERNAL_ERROR"], message=messages["INTERNAL_ERROR"])
    return response.response()

@app.route("/donations_orders/<int:donation_order_id>", methods=["PUT"])
@jwt_handling
def update_donation_order(donation_order_id):
  claims = get_jwt()
  donation_order = Donation_order.query.filter_by(id=donation_order_id).first()
  if claims["role"]=='user' and claims['sub'] != requester.username:
    response = BaseResponse(data=None, errors=errors["NOT_ACCESS_ERROR"], message=messages["NOT_ACCESS_ERROR_MESSAGE"])
    return response.response(), 403  
  if donation_order is None:
    response = BaseResponse(data=None, errors=errors["NOT_FOUND"], message=messages["NOT_FOUND"])
    return response.response(), 404
  changed_donation_order_data = request.get_json()
  donation_order = check_and_update_donations(donation_order, **changed_donation_order_data)
  db.session.add(donation_order)
  db.session.commit()
  check_and_update_donation_status(donation_order)
  response = BaseResponse(data=donation_order.to_dict(), errors=None, message=messages["GENERAL_SUCCESS"])
  return response.response(), 200