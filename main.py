import customtkinter
from Session_gallery import create_session_gallery_section
from Patient_selection import Patient_selection
import json
def main():
    app = customtkinter.CTk()
    app.title("Session Gallery and Patient Selection")
    app.geometry("900x500")
    patients = {}
    with open('patients.json', 'r') as file:
        data = json.load(file)  # Parse JSON into a dictionary
        patients.update(data) 
    
    a = Patient_selection(patients, app)
    a.create_patient_selection_section()
    # create_session_gallery_section(app)

    app.mainloop()

if __name__ == "__main__":
    main()