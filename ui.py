from customtkinter import *
from tkinter import messagebox, Menu
import os
import json
import tkinter as tk
from tkinter import messagebox 
import os
import capture_window


# Set the application appearance to dark mode
set_appearance_mode("dark")  # Dark theme
set_default_color_theme("dark-blue")  # Optionally set color theme

curr_root = ""

# Directory and file paths
patient_data_dir = "./Patient_Data"
patient_info_file = "./patients.json"

# Dictionary to store patient data
patients = {}

# Load existing patient data from the JSON file
def load_patient_data_from_file():
    global patients
    if os.path.exists(patient_info_file):
        with open(patient_info_file, "r") as file:
            patients = json.load(file)
           



    

# Save the updated patient data to the JSON file
def save_patient_data_to_file():
    with open(patient_info_file, "w") as file:
        json.dump(patients, file, indent=4)
    messagebox.showinfo("Success", "Patient data saved successfully.")

# Function to create the Session Gallery section (Left Frame)
def create_session_gallery_section(master):
    gallery_frame = CTkFrame(master=master, fg_color="#2C2F33")
    gallery_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    gallery_frame.grid_rowconfigure(3, weight=1)
    gallery_frame.grid_columnconfigure(0, weight=1)
    gallery_frame.grid_columnconfigure(1, weight=1)

    gallery_title = CTkLabel(master=gallery_frame, text="Session Gallery", font=("Poppins", 16), text_color="white")
    gallery_title.grid(row=0, column=0, columnspan=2, pady=(10, 5))

    divider = CTkLabel(master=gallery_frame, text="____________________________________________________________________________________________________", text_color="white")
    divider.grid(row=1, column=0, columnspan=2, pady=(0, 5))

    good_label = CTkLabel(master=gallery_frame, text="Good", font=("Poppins", 14), text_color="white")
    good_label.grid(row=2, column=0, padx=20)

    bad_label = CTkLabel(master=gallery_frame, text="Bad", font=("Poppins", 14), text_color="white")
    bad_label.grid(row=2, column=1, padx=20)

    good_scrollable_frame = CTkScrollableFrame(master=gallery_frame, fg_color="#A9A9A9")
    good_scrollable_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    bad_scrollable_frame = CTkScrollableFrame(master=gallery_frame, fg_color="#A9A9A9")
    bad_scrollable_frame.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

def get_app(root):
    curr_root = root
    return curr_root

# Function to create the Patient Selection section (Right Frame)
def create_patient_selection_section(master):
    master.grid_columnconfigure(0, weight=1)  # Left space
    master.grid_columnconfigure(1, weight=1)  # Center where patient_frame is placed
    master.grid_columnconfigure(2, weight=1)  # Right space

# Configure rows for vertical centering (optional)
    master.grid_rowconfigure(0, weight=1)
    master.grid_rowconfigure(1, weight=1)
    patient_frame = CTkFrame(master=master, fg_color="#2C2F33")
    patient_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    patient_frame.grid_columnconfigure(0, weight=1)
    patient_frame.grid_rowconfigure(14, weight=1)

    icon = CTkLabel(master=patient_frame, text="🏥", font=("Poppins", 40), text_color="white")
    icon.grid(row=0, column=0, pady=(10, 5), sticky="n")

    select_patient_title = CTkLabel(master=patient_frame, text="Select Patient", font=("Poppins", 16), text_color="white")
    select_patient_title.grid(row=1, column=0, pady=(5, 10), sticky="n")

    patient_names = list(patients.keys())
    patient_dropdown = CTkComboBox(master=patient_frame, values=patient_names)
    patient_dropdown.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="ew")

    add_patient_label = CTkLabel(master=patient_frame, text="Add New Patient", font=("Poppins", 14), text_color="white")
    add_patient_label.grid(row=3, column=0, pady=(10, 5))

    name_label = CTkLabel(master=patient_frame, text="Name", font=("Poppins", 12), text_color="white")
    name_label.grid(row=4, column=0, pady=(5, 0), sticky="n")
    name_entry = CTkEntry(master=patient_frame)
    name_entry.grid(row=5, column=0, padx=10, pady=(5, 10), sticky="ew")

    age_label = CTkLabel(master=patient_frame, text="Age", font=("Poppins", 12), text_color="white")
    age_label.grid(row=6, column=0, pady=(5, 0), sticky="n")
    age_entry = CTkEntry(master=patient_frame)
    age_entry.grid(row=7, column=0, padx=10, pady=(5, 10), sticky="ew")

    condition_label = CTkLabel(master=patient_frame, text="Condition", font=("Poppins", 12), text_color="white")
    condition_label.grid(row=8, column=0, pady=(5, 0), sticky="n")
    condition_entry = CTkEntry(master=patient_frame)
    condition_entry.grid(row=9, column=0, padx=10, pady=(5, 10), sticky="ew")

    patient_info_display = CTkTextbox(master=patient_frame, width=200, height=100, fg_color="#2C2F33")
    patient_info_display.grid(row=13, column=0, padx=10, pady=(10, 20), sticky="nsew")
    patient_info_display.insert("1.0", "Patient Information:\n\nName:\nAge:\nCondition:")
    patient_info_display.configure(state="disabled")

    def update_patient_info(name):
        if name in patients:
            patient_data = patients[name]
            age = patient_data.get("Age", "N/A")
            condition = patient_data.get("Condition", "N/A")
            patient_info_display.configure(state="normal")
            patient_info_display.delete("1.0", "end")
            patient_info_display.insert("1.0", f"Patient Information:\n\nName: {name}\nAge: {age}\nCondition: {condition}")
            patient_info_display.configure(state="disabled")
            create_session_gallery_section(master)


            result = messagebox.askyesno("Start Capturing", "Do you want to start capturing?")
        if result:
            # capture_window()  # Placeholder for capture functionality
            messagebox.showinfo("Capture", "Starting the capturing process!")
            capture_window.open_capture_window(curr_root)





            

    def clear_patient_data():
        patient_dropdown.set("")
        patient_info_display.configure(state="normal")
        patient_info_display.delete("1.0", "end")
        patient_info_display.insert("1.0", "Patient Information:\n\nName:\nAge:\nCondition:")
        patient_info_display.configure(state="disabled")
        name_entry.delete(0, "end")
        age_entry.delete(0, "end")
        condition_entry.delete(0, "end")

    # Function to add a new patient
    def add_patient_data():
        name = name_entry.get().strip()
        age = age_entry.get().strip()
        condition = condition_entry.get().strip()

        if not name or not age or not condition:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        if name in patients:
            messagebox.showwarning("Warning", "Patient already exists.")
            return

        # Add patient data to dictionary
        patients[name] = {"Age": age, "Condition": condition}
        save_patient_data_to_file()  # Save to file

        # Update the dropdown with the new patient and clear entries
        patient_dropdown.configure(values=list(patients.keys()))
        clear_patient_data()
        messagebox.showinfo("Success", "Patient added successfully.")




        load_button = CTkButton(
        master=patient_frame,
        text="Load Patient Data",
        fg_color="#7289da",
        command=lambda: load_and_start_capturing()
    )
        load_button.grid(row=10, column=0, pady=(10, 5), sticky="ew")

    def load_and_start_capturing():
        selected_patient = patient_dropdown.get()
        if not selected_patient:
            messagebox.showwarning("Warning", "Please select a patient to load data.")
            return
        update_patient_info(selected_patient)  # Load patient info
        messagebox.showinfo("Info", "Patient data loaded. Starting capture...")
        # Add code to start capturing process if necessary

    

    load_button = CTkButton(master=patient_frame, text="Load Patient Data", fg_color="#7289da", command=lambda: update_patient_info(patient_dropdown.get()))
    load_button.grid(row=10, column=0, pady=(10, 5), sticky="ew")                                                   
     
 

    add_button = CTkButton(master=patient_frame, text="Add Patient Data", fg_color="#34c759", command=add_patient_data)
    add_button.grid(row=11, column=0, pady=(5, 5), sticky="ew")

    clear_button = CTkButton(master=patient_frame, text="Clear Patient Data", fg_color="#d9534f", command=clear_patient_data)
    clear_button.grid(row=12, column=0, pady=(5, 10), sticky="ew")


# Main application window
root = CTk()
root.geometry("1000x600")
root.title("Posture Detection System")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

menu_bar = Menu(root)
options_menu = Menu(menu_bar, tearoff=0)
options_menu.add_command(label="Save", command=save_patient_data_to_file)
menu_bar.add_cascade(label="Options", menu=options_menu)
root.config(menu=menu_bar)
load_patient_data_from_file()
# create_session_gallery_section(root)
create_patient_selection_section(root)

root.mainloop()
