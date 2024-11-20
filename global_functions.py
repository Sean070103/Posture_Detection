import json
from Patient_selection import Patient_selection
from Session_gallery import create_session_gallery_section

patients = {}
def get_patients():

    with open('patients.json', 'r') as file:
        data = json.load(file)  # Parse JSON into a dictionary
        patients.update(data) 
    return patients

def initialize_patient(root, name):
    a = Patient_selection(get_patients(), root)
    a.create_patient_selection_section()
    create_session_gallery_section(root, name)