from .geoloc import LocalizationHandler


class Match():

    def __init__(self, donation_object, donor_object):
        self.donor_blood_type = self._blood_type_conversor(donor_object.blood_type)
        self.requester_blood_type = donation_object.blood_type
        self.localization_match = LocalizationHandler(donation_object, donor_object).match
        self.blood_type_match = self.donor_blood_type == self.requester_blood_type
        self.match = True if self.localization_match and self.blood_type_match else False

    def _blood_type_conversor(self, blood_type):
        blood_types = {
            "A+": 1,
            "A-": 2,
            "B+": 3,
            "B-": 4,
            "AB+": 5,
            "AB-": 6,
            "O+": 7,
            "O-": 8
        }
        return blood_types[blood_type]