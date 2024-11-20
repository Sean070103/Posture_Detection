from customtkinter import CTkFrame, CTkLabel, CTkComboBox, CTkEntry, CTkTextbox, CTkButton
from tkinter import messagebox
import os
import json
from Session_gallery import create_session_gallery_section
from Capture_window import Capture_window
# Function to create the Patient Selection section (Right Frame)

class Patient_selection2:
    def __init__(self, patients, root):
        self.patients = patients
        self.root = root
        self.patient_frame = CTkFrame(root, fg_color="#2C2F33")
        self.patient_names = list(patients.keys())
        self.patient_dropdown = CTkComboBox(self.patient_frame, values=self.patient_names)
        self.name_entry = CTkEntry(self.patient_frame)
        self.age_entry = CTkEntry(self.patient_frame)
        self.patient_info_display = CTkTextbox(self.patient_frame, width=200, height=100, fg_color="#2C2F33")
        self.condition_entry = CTkEntry(self.patient_frame)
        self.patient_info_file = "./patients.json"
        print("created")
    

    # Load existing patient data from the JSON file
    def load_patient_data_from_file(self):
        if os.path.exists(self.patient_info_file):
            with open(self.patient_info_file, "r") as file:
                self.patients = json.load(file)


    def save_patient_data_to_file(self):
        with open(self.patient_info_file, "w") as file:
            json.dump(self.patients, file, indent=4)
        messagebox.showinfo("Success", "Patient data saved successfully.")
  
    def get_patient_frame(self):
        return self.patient_frame

    def get_patient_dropdown(self):
        return self.patient_dropdown

    def create_patient_selection_section(self):
        self.root.grid_columnconfigure(0, weight=1)  # Left space
        self.root.grid_columnconfigure(1, weight=1)  # Center where patient_frame is placed
        self.root.grid_columnconfigure(2, weight=1)  # Right space

    # Configure rows for vertical centering (optional)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # patient_frame = self.get_patient_frame()
        self.patient_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.patient_frame.grid_columnconfigure(0, weight=1)
        self.patient_frame.grid_rowconfigure(14, weight=1)

        icon = CTkLabel(self.patient_frame, text="🏥", font=("Poppins", 40), text_color="white")
        icon.grid(row=0, column=0, pady=(10, 5), sticky="n")

        select_patient_title = CTkLabel(self.patient_frame, text="Select Patient", font=("Poppins", 16), text_color="white")
        select_patient_title.grid(row=1, column=0, pady=(5, 10), sticky="n")

        
        # patient_dropdown = CTkComboBox(self.patient_frame, values=self.patient_names)
        self.patient_dropdown.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="ew")

        add_patient_label = CTkLabel(self.patient_frame, text="Add New Patient", font=("Poppins", 14), text_color="white")
        add_patient_label.grid(row=3, column=0, pady=(10, 5))

        name_label = CTkLabel(self.patient_frame, text="Name", font=("Poppins", 12), text_color="white")
        name_label.grid(row=4, column=0, pady=(5, 0), sticky="n")
        
        self.name_entry.grid(row=5, column=0, padx=10, pady=(5, 10), sticky="ew")
        
        age_label = CTkLabel(self.patient_frame, text="Age", font=("Poppins", 12), text_color="white")
        age_label.grid(row=6, column=0, pady=(5, 0), sticky="n")
        
        self.age_entry.grid(row=7, column=0, padx=10, pady=(5, 10), sticky="ew")

        condition_label = CTkLabel(self.patient_frame, text="Condition", font=("Poppins", 12), text_color="white")
        condition_label.grid(row=8, column=0, pady=(5, 0), sticky="n")
        
        self.condition_entry.grid(row=9, column=0, padx=10, pady=(5, 10), sticky="ew")

        
        self.patient_info_display.grid(row=13, column=0, padx=10, pady=(10, 20), sticky="nsew")
        self.patient_info_display.insert("1.0", "Patient Information:\n\nName:\nAge:\nCondition:")
        self.patient_info_display.configure(state="disabled")

        # self.update_patient_info()

        load_button = CTkButton(self.patient_frame, text="Load Patient Data", fg_color="#7289da", command=lambda: self.update_patient_info(self.patient_dropdown.get()))
        load_button.grid(row=10, column=0, pady=(10, 5), sticky="ew")                                                   

        add_button = CTkButton(self.patient_frame, text="Add Patient Data", fg_color="#34c759", command=self.add_patient_data)
        add_button.grid(row=11, column=0, pady=(5, 5), sticky="ew")

        clear_button = CTkButton(self.patient_frame, text="Clear Patient Data", fg_color="#d9534f", command=self.clear_patient_data)
        clear_button.grid(row=12, column=0, pady=(5, 10), sticky="ew")

    def update_patient_info(self, name):
        if name in self.patients:
            patient_data = self.patients[name]
            age = patient_data.get("Age", "N/A")
            condition = patient_data.get("Condition", "N/A")
            self.patient_info_display.configure(state="normal")
            self.patient_info_display.delete("1.0", "end")
            self.patient_info_display.insert("1.0", f"Patient Information:\n\nName: {name}\nAge: {age}\nCondition: {condition}")
            self.patient_info_display.configure(state="disabled")
            # create_session_gallery_section(master)
            # print(patient_data)

            result = messagebox.askyesno("Start Capturing", "Do you want to start capturing?")
        if result:
            # capture_window()  # Placeholder for capture functionality
            print(self.patient_dropdown.get())
            messagebox.showinfo("Capture", "Starting the capturing process!")
            create_session_gallery_section(self.root, self.patient_dropdown.get())
            
            a = Capture_window(self.root)
            a.open_capture_window(self.patient_dropdown.get())

            # capture_window.open_capture_window(curr_root, name)
                      
    def clear_patient_data(self):
        self.patient_dropdown.set("")
        self.patient_info_display.configure(state="normal")
        self.patient_info_display.delete("1.0", "end")
        self.patient_info_display.insert("1.0", "Patient Information:\n\nName:\nAge:\nCondition:")
        self.patient_info_display.configure(state="disabled")
        self.name_entry.delete(0, "end")
        self.age_entry.delete(0, "end")
        self.condition_entry.delete(0, "end")

        # # Function to add a new patient
    def add_patient_data(self):
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        condition = self.condition_entry.get().strip()

        if not name or not age or not condition:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        if name in self.patients:
            messagebox.showwarning("Warning", "Patient already exists.")
            return

        # Add patient data to dictionary
        self.patients[name] = {"Age": age, "Condition": condition}
        self.save_patient_data_to_file()  # Save to file

        # Create the patient folder with subfolders for good and bad posture
        base_path = r"C:\Users\garci\Desktop\Sean_Thesis\patient_data"
        patient_folder = os.path.join(base_path, name)
        
        try:
            os.makedirs(os.path.join(patient_folder, "Good_Posture"), exist_ok=True)
            os.makedirs(os.path.join(patient_folder, "Bad_Posture"), exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create folders: {str(e)}")
            return

        # Update the dropdown with the new patient and clear entries
        self.patient_dropdown.configure(values=list(self.patients.keys()))
        self.clear_patient_data()
        messagebox.showinfo("Success", "Patient added successfully.")




        load_button = CTkButton(
        master=self.patient_frame,
        text="Load Patient Data",
        fg_color="#7289da",
        command=lambda: self.load_and_start_capturing()
        )
        load_button.grid(row=10, column=0, pady=(10, 5), sticky="ew")

    

    # def add_patient():
    #     patient_name = new_patient_name.get().strip()
    #     if not patient_name:
    #         messagebox.showerror("Error", "Patient name cannot be empty.")
    #         return  # Don't create folders for empty names

    #     # Create folder structure for the new patient
    #     new_patient_folder = os.path.join(patient_data_dir, patient_name)
    #     if not os.path.exists(new_patient_folder):
    #         os.makedirs(os.path.join(new_patient_folder, "Good_Posture"))
    #         os.makedirs(os.path.join(new_patient_folder, "Bad_Posture"))
            
    #         # Create the details.txt file
    #         details_file = os.path.join(new_patient_folder, "details.txt")
    #         with open(details_file, "w") as f:
    #             f.write("Physical therapist comments:\n")
                
    #         # Refresh the patient dropdown
    #         patient_dropdown['values'] = os.listdir(patient_data_dir)
    #         new_patient_name.set("")  # Clear the entry field
    #         messagebox.showinfo("Success", f"Patient {patient_name} added successfully.")
    #     else:
    #         messagebox.showerror("Error", f"Patient {patient_name} already exists.")

    def load_and_start_capturing(self):
        selected_patient = self.patient_dropdown.get()
        if not selected_patient:
            messagebox.showwarning("Warning", "Please select a patient to load data.")
            return
        self.update_patient_info(selected_patient)  # Load patient info
        messagebox.showinfo("Info", "Patient data loaded. Starting capture...")
        # Add code to start capturing process if necessary




