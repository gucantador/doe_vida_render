# TODO Implement google maps API to get a more accurate localization and create a match based on a radius

class LocalizationHandler():
    
    def __init__(self, donation_object, user_object):
        self.hospital_adress = None
        self.hospital_coordenates = None
        self.donator_adress = None
        self.donator_coordenates = None
        self.hospital_name = donation_object.hospitals.hospital_name
        self.donator_city = user_object.city
        self.hospital_city = donation_object.hospitals.city_name
        self.match = self.donator_city == self.hospital_city

    def get_distance(self):
        pass

    def _get_coordenates_by_adress(self):
        pass