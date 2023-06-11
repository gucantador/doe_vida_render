import re
import jwt
from flask import jsonify, request
from functools import wraps
from . import app, db
from flask_app.models import Hospitals

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('Token')

        print(request.url)
        print(token)

        if not token:
            return jsonify({'mensagem': 'Token ausente!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'mensagem': 'Token inválido!'}), 403

        return f(*args, **kwargs)

    return decorated


def is_valid_email(email):
    """
    Checks if the given email address is valid.
    Parameters:
        email (str): The email address to check.
    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def check_username(email):
    """
    Checks if the given email address is in codition to be saved in the database.
    Parameters:
        email (str): The email address to check.
    Returns:
        An error message or None in case everythign is ok.
    """
    if len(email) > 80:
        return {"Erro": "Seu email precisa ter menos que 80 caracteres."}
    if email is None or len(email) == 0:
        return {"Erro": "O campo e-mail não pode estar vazio."}
    if is_valid_email(email) == False:
        return {"Erro": "O e-mail não é válido."}
    return None

def check_and_update(user, **json_data):
    """
    Checks which expected keys are present in a JSON data.
    Parameters:
        user (object); **json_data (dict);
    Returns:
        user object updated.
    """
    if json_data.get('first_name') is not None:
        user.first_name = json_data['first_name']
    if json_data.get('last_name') is not None:
        user.last_name = json_data['last_name']
    if json_data.get('birthdate') is not None:
        user.birthdate = json_data['birthdate']
    if json_data.get('blood_type') is not None:
        user.blood_type = json_data['blood_type']
    if json_data.get('phone') is not None:
        user.phone = json_data['phone']
    if json_data.get('sex') is not None:
        user.sex = json_data['sex']
    if json_data.get('qty_donations') is not None:
        user.qty_donations = json_data['qty_donations']
    if json_data.get('date_last_donation') is not None:
        user.date_last_donation = json_data['date_last_donation']
    if json_data.get('state') is not None:
        user.state = json_data['state']
    if json_data.get('city') is not None:
        user.city = json_data['city']
    return user

def check_and_update_hospitals(hospital, **json_data):
  """
  Checks which expected keys are present in a JSON data and updates the hospital object accordingly.

  Parameters:
      hospital (object): The hospital object to update.
      json_data (dict): The JSON data to check.

  Returns:
      The updated hospital object.
  """
  if json_data.get('hospital_name') is not None:
    hospital.hospital_name = json_data['hospital_name']
  if json_data.get('city_name') is not None:
    hospital.city_name = json_data['city_name']
  if json_data.get('state') is not None:
    hospital.state = json_data['state']
  if json_data.get('donations_orders') is not None:
    hospital.donations_orders = json_data['donations_orders']
  if json_data.get('donations_orders_done') is not None:
    hospital.donations_orders_done = json_data['donations_orders_done']
  if json_data.get('donations_orders_cancelled') is not None:
    hospital.donations_orders_cancelled = json_data['donations_orders_cancelled']
  return hospital

def check_hospital_db(hospital, city_name, state):
    """
    Checks if the hospital is already in the database.

    Parameters:
        hospital (string): The hospital name.
        city_name (string): The city name where the hospital is located.
        state (int): The state where the hospital is located.

    Returns:
        Bool: True if the hospital is already in the databse, false otherwise.
    """
    try:
        hospital = Hospitals.query.filter_by(hospital_name=hospital).first()
        if hospital.city_name == city_name and hospital.state == state:
            return True
    except:
        return False
    
def check_and_update_donations(donation_order, **json_data):
  """
  Checks which expected keys are present in a JSON data and updates the hospital object accordingly.

  Parameters:
      donation_order (object): The donation_order object to update.
      json_data (dict): The JSON data to check.

  Returns:
      The updated donation order object.
  """
  if json_data.get('patient_name') is not None:
    donation_order.patient_name = json_data['patient_name']
  if json_data.get('blood_type') is not None:
    donation_order.blood_type = json_data['blood_type']
  if json_data.get('description') is not None:
    donation_order.description = json_data['description']
  if json_data.get('qty_bags') is not None:
    donation_order.qty_bags = json_data['qty_bags']
  if json_data.get('date_donation_order') is not None:
    donation_order.date_donation_order = json_data['date_donation_order']
  if json_data.get('city_name') is not None:
    donation_order.city_name = json_data['city_name']
  if json_data.get('state') is not None:
    donation_order.state = json_data['state']
  if json_data.get('hospital') is not None:
    donation_order.hospital = json_data['hospital']
  if json_data.get('requester') is not None:
    donation_order.requester = json_data['requester']
  if json_data.get('status') is not None:
    donation_order.status = json_data['status']
  return donation_order

def check_and_update_donation_status(order):
  """
  Checks the status of the donation order and uptdate in the database if needded.

  Parameters:
      order (object): The donation_order object to update.
  """
  if order.status == "completed":
    print(order.hospital)
    hospital = Hospitals.query.get(order.hospital)
    print(hospital)
    if hospital.donations_orders_done is None:
        hospital.donations_orders_done = 1
    else:
        hospital.donations_orders_done = hospital.donations_orders_done + 1 
    db.session.add(hospital)
    db.session.commit()

    order.status = 'completed'
    db.session.add(order)
    db.session.commit()

  if order.status == "cancelled":
    hospital = Hospitals.query.get(order.hospital)
    if hospital.donations_orders_cancelled is None:
        hospital.donations_orders_cancelled = 1
    else:
        hospital.donations_orders_cancelled = hospital.donations_orders_cancelled + 1 
    db.session.add(hospital)
    db.session.commit()

    order.status = 'cancelled'
    db.session.add(order)
    db.session.commit()

def load_roles():
  
  roles = {
      'admin': {
          'role': 'admin',
          'can_view_all_users': True,
          'can_edit_all_users': True,
      },
      'user': {
          'role': 'user',
          'can_view_own_data': True,
          'can_edit_own_data': True,
      },
  }

  return roles