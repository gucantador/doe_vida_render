from flask_app import  db, jwt__
from flask import jsonify, request
from flask_app.models import Hospitals
from flask_app.utils import check_and_update_hospitals
from flask_jwt_extended import jwt_required, get_jwt_identity, create_refresh_token, create_access_token

def get_app():
    from flask_app import app
    return app

app = get_app()

@app.route("/hospitals")
def get_hospitals():
  hospitals = Hospitals.query.all()
  return jsonify(hospitals=[hospital.to_dict() for hospital in hospitals]), 200

@jwt_required()
@app.route("/hospitals/<hospital_name>")
def get_hospital_by_hospital_name(hospital_name):
  hospital = Hospitals.query.filter_by(hospital_name=hospital_name).first()
  if hospital is None:
    return jsonify({"error": "Hospital not found"}), 404
  else:
    return jsonify(hospital.to_dict()), 200

@jwt_required() 
@app.route("/hospitals", methods=["POST"])
def post_hospital():
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

  return jsonify(new_hospital.to_dict()), 200

@jwt_required()
@app.route("/hospitals/<string:hospital_name>", methods=["PUT"])
def update_hospital_by_hospital_name(hospital_name):
  hospital = Hospitals.query.filter_by(hospital_name=hospital_name).first()
  if hospital is None:
    return jsonify({"Error": "Hospital not found"}), 404
  changed_hospital_data = request.get_json()
  hospital = check_and_update_hospitals(hospital, **changed_hospital_data)
  db.session.add(hospital)
  db.session.commit()
  return jsonify(hospital.to_dict()), 200

@jwt_required()
@app.route("/hospitals/<string:hospital_name>", methods=["DELETE"])
def delete_hospital_by_hospital_name(hospital_name):
  hospital = Hospitals.query.filter_by(hospital_name=hospital_name).first()
  if hospital is None:
    return jsonify({"Error": "Hospital not found"}), 404
  db.session.delete(hospital)
  db.session.commit()
  return jsonify({"success": "Hospital deleted"}), 200