import json
import cv2
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
from ultralytics import YOLO
import threading
import random
from datetime import datetime
import shutil
from tkinter import ttk
from tkinter import messagebox
import os
import shutil
import time
from PIL import Image
import torch
import torch.nn.functional as F  # Import the functional module from PyTorch



# Paths to directories and models
photos_dir = r'.\gallery\photos'
keypoints_dir = r'.\gallery\photos\keypoints'
model_keypoints_path = r'.\yolov8n-pose.pt'
model_classification_path = r'.\best.pt'

# Patient data directory
patient_data_dir = r".\patient_data"
global selected_patient_folder

# Load the YOLO models
model_keypoints = YOLO(model_keypoints_path).to('cuda')
model_classification = YOLO(model_classification_path).to('cuda')

# Define the color palette
colors = {
    "primary": "#7289da",
    "secondary": "#424549",
    "tertiary": "#36393e",
    "background": "#282b30",
    "text": "#FFFFFF"  # Changed to white for better visibility
}

# Define colors with all necessary keys
colors = {
    "background": "#2E2E2E",
    "tertiary": "#3A3A3A",
    "text": "#FFFFFF",  # Add your desired text color
}


def start_live_capture():
    global cap
    cap = cv2.VideoCapture(0)
    update_frame()

def stop_live_capture():
    global cap
    if cap is not None:
        cap.release()
        cap = None

good_posture_recommendations = [
    "Very good! Maintain your posture.",
    "You're doing well! Keep it up.",
    "Excellent posture! Keep it steady.",
    "Great job! Continue with this posture.",
    "Perfect alignment! Maintain this posture.",
    "Keep it up! Your posture is looking good.",
    "Well done! Your posture is spot on.",
    "Fantastic! Keep maintaining this posture.",
    "Nice work! Your posture is well-aligned.",
    "Good job! Stay consistent with this posture."
]

bad_posture_recommendations = [
    "Try to straighten your back.",
    "Keep your shoulders relaxed and down.",
    "Engage your core for better balance.",
    "Keep your head up and look forward.",
    "Adjust your seating position to support your lower back.",
    "Make sure both feet are flat on the ground.",
    "Practice gentle neck stretches to maintain alignment.",
    "Engage in gentle exercises to strengthen postural muscles."
    "Practice deep breathing to reduce tension in the body.",
    "Use a rolled towel to support the natural curve of your spine.",
    "Perform gentle stretching exercises throughout the day.",
    "Make sure your computer screen is at eye level.",
    "Use a footrest if your feet don’t reach the ground.",
    "Avoid sitting for prolonged periods; stand and stretch.",
    "Incorporate regular physical therapy exercises into your routine.",
    "Check your posture frequently throughout the day.",
    "Focus on keeping your weight balanced over your feet.",
    "Avoid leaning forward when sitting or standing.",
    "Perform seated leg lifts to engage core muscles.",
    "Use a posture brace if recommended by your therapist.",
    "Engage in strengthening exercises for your shoulders and back.",
    "Stand with a slight bend in your knees to avoid locking them.",
    "Ensure your chair height allows your elbows to be at desk level.",
    "Relax your arms by your sides when standing or walking.",
    "Practice walking with a straight back and head held high.",
    "Keep your knees aligned with your hips when sitting.",
    "Make sure your ears are in line with your shoulders.",
    "Place a small pillow behind your upper back for additional support.",
    "Perform gentle neck rotations to maintain flexibility.",
    "Incorporate core-strengthening exercises into your routine.",
    "Engage in regular stretching to maintain mobility."
]

def start_live_capture():
    global cap
    cap = cv2.VideoCapture(0)
    update_frame()

def stop_live_capture():
    global cap
    cap.release()

def update_frame():
    global cap
    if cap is not None and cap.isOpened():
        try:
            # Read a new frame
            ret, frame = cap.read()
            if ret:
                # Convert frame to tensor, normalize, and move to GPU
                frame_gpu = torch.from_numpy(frame).float().div(255).to('cuda')  # Convert to float and normalize to [0, 1]

                # Permute dimensions to convert from HWC (Height, Width, Channels) to CHW (Channels, Height, Width)
                frame_gpu = frame_gpu.permute(2, 0, 1).unsqueeze(0)  # Add batch dimension

                # Resize the frame to 640x640 (YOLO model requirement)
                frame_gpu = F.interpolate(frame_gpu, size=(640, 640), mode='bilinear', align_corners=False)

                # Perform keypoints detection using the current frame on the GPU
                keypoints_results = model_keypoints(frame_gpu)

                if keypoints_results and len(keypoints_results) > 0:
                    # Draw keypoints and lines (skeleton) on the frame
                    annotated_frame = keypoints_results[0].plot()

                    # Perform posture classification using the frame
                    boxes = keypoints_results[0].boxes.xyxy
                    if boxes is not None:
                        for box in boxes:
                            x1, y1, x2, y2 = map(int, box)
                            roi = frame[y1:y2, x1:x2]

                            # Move the ROI to GPU for posture classification
                            roi_gpu = torch.from_numpy(roi).float().div(255).to('cuda')  # Normalize ROI

                            # Permute and resize the ROI tensor
                            roi_gpu = roi_gpu.permute(2, 0, 1).unsqueeze(0)  # Add batch dimension
                            roi_gpu = F.interpolate(roi_gpu, size=(640, 640), mode='bilinear', align_corners=False)

                            # Perform posture classification on the ROI
                            classification_results = model_classification(roi_gpu)

                            if classification_results:
                                for cls_result in classification_results:
                                    if len(cls_result.boxes.cls) > 0:
                                        label = cls_result.names[int(cls_result.boxes.cls[0])]
                                        posture_text = "Bad" if label.lower() != "good" else "Good"
                                        color = (0, 255, 0) if posture_text == "Good" else (0, 0, 255)
                                    else:
                                        posture_text = "Good"
                                        color = (0, 255, 0)

                                    # Draw the classification result on the annotated frame
                                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                                    text_position_x = int((x1 + x2) / 2) - 20
                                    cv2.putText(annotated_frame, posture_text, (text_position_x, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Convert frame for display in the GUI
                cv2image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                live_label.imgtk = imgtk
                live_label.config(image=imgtk)
                live_label.update_idletasks()

        except Exception as e:
            print(f"An error occurred in update_frame: {e}")

    # Continue updating the frame every 10 milliseconds
    live_label.after(10, update_frame)

def capture_image():
    global capturing
    if not capturing and cap is not None and cap.isOpened():
        capturing = True
        def capture_task():
            global capturing
            try:
                ret, frame = cap.read()
                if ret:
                    keypoints_results = model_keypoints(frame)
                    if keypoints_results and len(keypoints_results) > 0:
                        annotated_frame = keypoints_results[0].plot()
                        boxes = keypoints_results[0].boxes.xyxy
                        if boxes is not None:
                            for box in boxes:
                                x1, y1, x2, y2 = map(int, box)
                                roi = frame[y1:y2, x1:x2]

                                classification_results = model_classification(roi)
                                if classification_results:
                                    for cls_result in classification_results:
                                        if len(cls_result.boxes.cls) > 0:
                                            label = cls_result.names[int(cls_result.boxes.cls[0])]
                                            posture_text = "Bad" if label.lower() != "good" else "Good"
                                            color = (0, 255, 0) if posture_text == "Good" else (0, 0, 255)
                                        else:
                                            posture_text = "Good"
                                            color = (0, 255, 0)

                                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                                        text_position_x = int((x1 + x2) / 2) - 20
                                        cv2.putText(annotated_frame, posture_text, (text_position_x, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                    # Use a timestamp to create unique filenames
                    timestamp = int(time.time())
                    
                    if posture_text == "Bad":
                        img_name = os.path.join(bad_posture_folder, f"image_with_keypoints_{timestamp}.png")
                    else:
                        img_name = os.path.join(good_posture_folder, f"image_with_keypoints_{timestamp}.png")
                    
                    cv2.imwrite(img_name, annotated_frame)

                    keypoints = keypoints_results[0].keypoints.xy.cpu().numpy()
                    json_name = os.path.join(keypoints_dir, f"keypoints_{timestamp}.json")
                    with open(json_name, 'w') as f:
                        json.dump(keypoints.tolist(), f, indent=4)

                    update_gallery(img_name, posture_text)  # Corrected function call here

            except Exception as e:
                print(f"An error occurred in capture_image: {e}")
            finally:
                capturing = False

        threading.Thread(target=capture_task, daemon=True).start()

def update_gallery(img_path, posture, text_wraplength=200, text_width=40, text_height=5):
    """
    Updates the gallery with the captured image and adds it to the corresponding section
    based on posture classification. Also includes an adjustable recommendation text for both good and bad posture.

    Parameters:
    img_path (str): Path to the image to be added.
    posture (str): Either 'good' or 'bad' posture.
    text_wraplength (int): The wrap length for the recommendation text (in pixels).
    text_width (int): The width of the recommendation text label (in characters).
    text_height (int): The height of the recommendation text label (in lines).
    """
    try:
        # Create a thumbnail for the gallery
        thumbnail_size = (200, 200)
        img = Image.open(img_path)
        img.thumbnail(thumbnail_size)
        thumbnail = ImageTk.PhotoImage(img)

        if posture.lower() == "good":
            # Get a random recommendation for good posture
            recommendation = random.choice(good_posture_recommendations)

            # Create a frame for the image and the recommendation text
            frame = tk.Frame(gallery_good_list, bg=colors["tertiary"])

            # Image label
            image_label = tk.Label(frame, image=thumbnail, bg=colors["tertiary"])
            image_label.image = thumbnail  # Keep a reference to avoid garbage collection
            image_label.grid(row=0, column=0, padx=5)

            # Recommendations label for good posture
            text_label = tk.Label(
                frame, 
                text=recommendation, 
                bg=colors["tertiary"], 
                fg="white", 
                justify=tk.LEFT, 
                anchor='w', 
                wraplength=text_wraplength,  # Adjusts text wrapping based on passed parameter
                width=text_width,            # Adjusts the width of the label (in characters)
                height=text_height           # Adjusts the height of the label (in lines)
            )
            text_label.grid(row=0, column=1, padx=10, sticky='w')

            # Add hover effect to the recommendation text
            def on_enter(e):
                text_label.config(bg=colors["secondary"], fg="yellow")

            def on_leave(e):
                text_label.config(bg=colors["tertiary"], fg="white")

            text_label.bind("<Enter>", on_enter)
            text_label.bind("<Leave>", on_leave)

            # Add frame to the good posture gallery
            frame.grid(row=len(gallery_good_list.grid_slaves()), column=0, pady=5, padx=5, sticky='n')

        else:
            # Get a random recommendation for bad posture
            recommendation = random.choice(bad_posture_recommendations)

            # Create a frame for the image and the recommendation text
            frame = tk.Frame(gallery_bad_list, bg=colors["tertiary"])

            # Image label
            image_label = tk.Label(frame, image=thumbnail, bg=colors["tertiary"])
            image_label.image = thumbnail  # Keep a reference to avoid garbage collection
            image_label.grid(row=0, column=0, padx=5)

            # Recommendations label for bad posture
            text_label = tk.Label(
                frame, 
                text=recommendation, 
                bg=colors["tertiary"], 
                fg="white", 
                justify=tk.LEFT, 
                anchor='w', 
                wraplength=text_wraplength,  # Adjusts text wrapping based on passed parameter
                width=text_width,            # Adjusts the width of the label (in characters)
                height=text_height           # Adjusts the height of the label (in lines)
            )
            text_label.grid(row=0, column=1, padx=10, sticky='w')

            # Add hover effect to the recommendation text
            def on_enter(e):
                text_label.config(bg=colors["secondary"], fg="yellow")

            def on_leave(e):
                text_label.config(bg=colors["tertiary"], fg="white")

            text_label.bind("<Enter>", on_enter)
            text_label.bind("<Leave>", on_leave)

            # Add frame to the bad posture gallery
            frame.grid(row=len(gallery_bad_list.grid_slaves()), column=0, pady=5, padx=5, sticky='n')

        # Update the canvas scroll region to include new items
        gallery_canvas_good.update_idletasks()
        gallery_canvas_bad.update_idletasks()
        gallery_canvas_good.configure(scrollregion=gallery_canvas_good.bbox("all"))
        gallery_canvas_bad.configure(scrollregion=gallery_canvas_bad.bbox("all"))

    except Exception as e:
        print(f"Error updating gallery: {e}")
 

def load_icon(path):
    if os.path.exists(path):
        return ImageTk.PhotoImage(Image.open(path).resize((50, 50), Image.Resampling.LANCZOS))
    else:
        default_icon = Image.new("RGB", (50, 50), colors["secondary"])
        return ImageTk.PhotoImage(default_icon)

capture_icon_path = r'.\icon\capture.png'
record_icon_path = r'.\icon\video-camera.png'
save_icon_path = r'.\icon\upload.png'
patient_data_dir = r".\patient_data"


def open_progress_window():
    global patient_name_label  # Declare global to update in the main interface later
    patient_data_dir = r".\patient_data"
    
    # Ensure the directory exists
    if not os.path.exists(patient_data_dir):
        os.makedirs(patient_data_dir)  # Create the directory if it does not exist

    # Create a new window for progress
    progress_window = tk.Toplevel()
    progress_window.title("Progress Window")
    progress_window.geometry("1000x700")
    progress_window.configure(bg=colors["background"])

    # Patient selection section
    patient_label = tk.Label(progress_window, text="Select Patient", font=("Helvetica", 14), bg=colors["background"], fg=colors["text"])
    patient_label.pack(pady=10)

    patient_var = tk.StringVar()
    patient_dropdown = ttk.Combobox(progress_window, textvariable=patient_var)
    patient_dropdown['values'] = os.listdir(patient_data_dir)  # Assuming patient directories are named accordingly
    patient_dropdown.pack(pady=5)

    def load_patient_data():
        patient_id = patient_var.get()
        if not patient_id:
            messagebox.showerror("Error", "Please select a patient.")
            return

        # Clear previous data
        for widget in gallery_content_1.winfo_children():
            widget.destroy()
        for widget in gallery_content_2.winfo_children():
            widget.destroy()
        for widget in file_content.winfo_children():
            widget.destroy()

        # Reload galleries and data
        display_gallery(patient_id)
        display_patient_data(patient_id)

        # Update the patient name in the main interface
        update_patient_name_display(patient_id)

        # Confirmation dialog to start capturing data
        start_capture = messagebox.askyesno("Start Capturing Data", f"Do you want to start capturing data for {patient_id}?")
        if start_capture:
            
            start_capturing(patient_id)  # Call the function to start capturing data
        else:
            messagebox.showinfo("Action Canceled", "Data capturing has not started.")

    load_button = tk.Button(progress_window, text="Load Patient Data", command=load_patient_data)
    load_button.pack(pady=5)

    # Adding new patient section
    add_patient_label = tk.Label(progress_window, text="Add New Patient", font=("Helvetica", 14), bg=colors["background"], fg=colors["text"])
    add_patient_label.pack(pady=10)

    new_patient_name = tk.StringVar()
    add_patient_entry = tk.Entry(progress_window, textvariable=new_patient_name, width=30)
    add_patient_entry.pack(pady=5)

    def add_patient():
        patient_name = new_patient_name.get().strip()
        if not patient_name:
            messagebox.showerror("Error", "Patient name cannot be empty.")
            return  # Don't create folders for empty names

        # Create folder structure for the new patient
        new_patient_folder = os.path.join(patient_data_dir, patient_name)
        if not os.path.exists(new_patient_folder):
            os.makedirs(os.path.join(new_patient_folder, "Good_Posture"))
            os.makedirs(os.path.join(new_patient_folder, "Bad_Posture"))
            
            # Create the details.txt file
            details_file = os.path.join(new_patient_folder, "details.txt")
            with open(details_file, "w") as f:
                f.write("Physical therapist comments:\n")
                
            # Refresh the patient dropdown
            patient_dropdown['values'] = os.listdir(patient_data_dir)
            new_patient_name.set("")  # Clear the entry field
            messagebox.showinfo("Success", f"Patient {patient_name} added successfully.")
        else:
            messagebox.showerror("Error", f"Patient {patient_name} already exists.")

    add_patient_button = tk.Button(progress_window, text="Add Patient", command=add_patient)
    add_patient_button.pack(pady=5)

    # Clear patient data section
    clear_patient_label = tk.Label(progress_window, text="Clear Patient Data", font=("Helvetica", 14), bg=colors["background"], fg=colors["text"])
    clear_patient_label.pack(pady=10)

    def clear_patient_data():
        patient_name = patient_var.get()
        if not patient_name:
            messagebox.showerror("Error", "Please select a patient to clear.")
            return  # If no patient is selected, do nothing
        
        # Confirm with the user before deletion
        confirm = messagebox.askyesno("Clear Patient Data", f"Are you sure you want to delete all data for {patient_name}?")
        if confirm:
            # Delete the entire patient folder
            patient_folder = os.path.join(patient_data_dir, patient_name)
            if os.path.exists(patient_folder):
                shutil.rmtree(patient_folder)
                messagebox.showinfo("Patient Data Deleted", f"Data for {patient_name} has been cleared.")
                
                # Refresh the patient dropdown
                patient_dropdown['values'] = os.listdir(patient_data_dir)
                patient_var.set("")  # Clear the selection
                update_patient_name_display("")  # Clear the displayed patient name
                selected_patient_folder == patient_folder
        else:
            messagebox.showinfo("Action Canceled", "The patient data was not deleted.")
    
    clear_data_button = tk.Button(progress_window, text="Clear Patient Data", command=clear_patient_data)
    clear_data_button.pack(pady=5)

    # Gallery Section
    gallery_label = tk.Label(progress_window, text="Session Gallery", font=("Helvetica", 14), bg=colors["background"], fg=colors["text"])
    gallery_label.pack(pady=10)

    # gallery_frame = tk.Frame(progress_window, bg=colors["tertiary"])
    # gallery_frame.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)
    
    # bad and good posture frame
    gallery_frame = tk.Frame(progress_window, bg=colors["tertiary"])
    gallery_frame.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)

    # Canvas for gallery
    gallery_canvas = tk.Canvas(gallery_frame, bg=colors["tertiary"], highlightthickness=0)
    gallery_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar for gallery
    scrollbar = tk.Scrollbar(gallery_frame, command=gallery_canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    gallery_canvas.config(yscrollcommand=scrollbar.set)

    global gallery_content_1
    gallery_content_1 = tk.Frame(gallery_canvas, bg=colors["tertiary"], bd=2, relief="solid")
    gallery_canvas.create_window((0, 0), window=gallery_content_1, anchor="nw")
    
    global gallery_content_2
    gallery_content_2 = tk.Frame(gallery_canvas, bg=colors["tertiary"], bd=2, relief="solid")
    gallery_canvas.create_window((600, 0), window=gallery_content_2, anchor="nw")

    #
    #this is where the problem is
    #
    def display_gallery(patient_id):
        global patient_folder, good_posture_folder, bad_posture_folder
        patient_folder = os.path.join(patient_data_dir, patient_id)
        good_posture_folder = os.path.join(patient_folder, "Good_Posture")
        bad_posture_folder = os.path.join(patient_folder, "Bad_Posture")

        # l1 = tk.Label(gallery_content, text="number 1")
        # l2 = tk.Label(gallery_content, text="number 2")
        
        # l1.grid(row=0, column=0,  pady=2)
        # l2.grid(row=0, column=1,  pady=2)
        
        # Display good posture images
        display_images(good_posture_folder, "Good Posture", gallery_content_1)

        # Display bad posture images
        display_images(bad_posture_folder, "Bad Posture", gallery_content_2)
        print("display bad")
    #
    #this is where the problem is
    #

    def display_images(folder_path, posture_type, gallery_content):
        if not os.path.exists(folder_path):
            return

        posture_label = tk.Label(gallery_content, text=posture_type, font=("Helvetica", 12), bg=colors["tertiary"], fg=colors["text"])
        posture_label.pack(padx=5, pady=5)
        # posture_label.grid(row=0, column=num,  pady=2)
        # Load and display images
        image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
        for img_path in image_files:
            image = Image.open(img_path)
            image.thumbnail((150, 150))  # Resize image to thumbnail size
            img = ImageTk.PhotoImage(image)
            img_label = tk.Label(gallery_content, image=img, bg=colors["tertiary"])
            img_label.image = img  # Keep reference to avoid garbage collection
            img_label.pack(padx=5, pady=5)

    # File Section for Patient Data
    file_section_label = tk.Label(progress_window, text="Therapist Comments", font=("Helvetica", 14), bg=colors["background"], fg=colors["text"])
    file_section_label.pack(pady=10)

    file_frame = tk.Frame(progress_window, bg=colors["tertiary"])
    file_frame.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)

    # Scrollable area for patient data files
    file_canvas = tk.Canvas(file_frame, bg=colors["tertiary"], highlightthickness=0)
    file_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    file_scrollbar = tk.Scrollbar(file_frame, command=file_canvas.yview)
    file_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    file_canvas.config(yscrollcommand=file_scrollbar.set)

    global file_content
    file_content = tk.Frame(file_canvas, bg=colors["tertiary"])
    file_canvas.create_window((0, 0), window=file_content, anchor="nw")

    def display_patient_data(patient_id):
        patient_folder = os.path.join(patient_data_dir, patient_id)
        details_file = os.path.join(patient_folder, "details.txt")
        if os.path.exists(details_file):
            with open(details_file, "r") as f:
                comments = f.read()
            comments_label = tk.Label(file_content, text=comments, bg=colors["tertiary"], fg=colors["text"], justify="left", wraplength=700)
            comments_label.pack(pady=5)

    # Statistics Section
    stats_label = tk.Label(progress_window, text="Posture Statistics", font=("Helvetica", 14), bg=colors["background"], fg=colors["text"])
    stats_label.pack(pady=10)

    # Dummy data for demonstration, calculate dynamically in real implementation
    good_posture_count = 10
    bad_posture_count = 5

    stats_frame = tk.Frame(progress_window, bg=colors["tertiary"])
    stats_frame.pack(padx=20, pady=10)

    good_posture_label = tk.Label(stats_frame, text=f"Good Posture Sessions: {good_posture_count}", font=("Helvetica", 12), bg=colors["tertiary"], fg=colors["text"])
    good_posture_label.grid(row=0, column=0, padx=10, pady=5)
    
    bad_posture_label = tk.Label(stats_frame, text=f"Bad Posture Sessions: {bad_posture_count}", font=("Helvetica", 12), bg=colors["tertiary"], fg=colors["text"])
    bad_posture_label.grid(row=0, column=1, padx=10, pady=5)

    # Export Data Section
    def export_patient_data():
        patient_name = patient_var.get()
        if not patient_name:
            messagebox.showerror("Error", "Please select a patient to export.")
            return

        # Define the folder to export the patient's data
        patient_folder = os.path.join(patient_data_dir, patient_name)
        export_folder = filedialog.askdirectory(title="Select folder to export data")
        if not export_folder:
            return  # If user cancels, do nothing
        
        # Export patient data
        export_path = os.path.join(export_folder, f"{patient_name}_data.zip")
        shutil.make_archive(os.path.splitext(export_path)[0], 'zip', patient_folder)
        messagebox.showinfo("Export Successful", f"Data for {patient_name} has been exported to {export_path}.")

    export_button = tk.Button(progress_window, text="Export Patient Data", command=export_patient_data)
    export_button.pack(pady=10)

    patient_name_label = tk.Label(progress_window, text="", font=("Helvetica", 16), bg=colors["background"], fg=colors["text"])
    patient_name_label.pack(pady=10)

    def update_patient_name(*args):
        patient_name = patient_var.get()
        update_patient_name_display(patient_name)

    patient_var.trace_add("write", update_patient_name)

    # Function to update the patient name in the main interface
    def update_patient_name_display(name):
        patient_name_label.config(text=f"Selected Patient: {name}")

    # Progress Bar
    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=20)

    def load_patient_data_with_progress():
        patient_id = patient_var.get()
        if not patient_id:
            messagebox.showerror("Error", "Please select a patient.")
            return

        progress_bar.start(10)  # Start progress bar

        try:
            # Clear previous data
            for widget in gallery_content_1.winfo_children():
                widget.destroy()
            for widget in file_content.winfo_children():
                widget.destroy()

            display_gallery(patient_id)  # Load gallery
            display_patient_data(patient_id)  # Load patient data
        finally:
            progress_bar.stop()  # Stop the progress bar when done

    load_button = tk.Button(progress_window, text="Load Patient Data", command=load_patient_data_with_progress)
    load_button.pack(pady=5)
    
# Define a placeholder function for starting data capturing
def start_capturing(patient_id):
    # Placeholder for actual data capturing logic
    messagebox.showinfo("Capturing Data", f"Started capturing data for {patient_id}.")

# Call the function to open the progress window
open_progress_window()

# Start the GUI event loop
tk.mainloop()


def initialize_gui():
    global live_label, gallery_good_list, gallery_bad_list, gallery_canvas_good, gallery_canvas_bad

    root = tk.Tk()
    root.title("Posture Detection System")
    root.geometry("1280x720")
    root.configure(bg=colors["background"])

    # Gallery Frame
    gallery_frame = tk.Frame(root, bg=colors["tertiary"], bd=2, relief="solid")
    gallery_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Now, inside the gallery frame, ensure that thumbnails and recommendations take up more space
    gallery_frame.grid_rowconfigure(0, weight=1)
    gallery_frame.grid_columnconfigure(0, weight=1)

    # Good Posture Gallery Frame
    gallery_good_frame = tk.Frame(gallery_frame, bg=colors["tertiary"], width=350, bd=2, relief="solid")
    gallery_good_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Bad Posture Gallery Frame
    gallery_bad_frame = tk.Frame(gallery_frame, bg=colors["tertiary"], width=350)
    gallery_bad_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Canvas and Scrollbar for Good Posture Gallery
    gallery_canvas_good = tk.Canvas(gallery_good_frame, bg=colors["tertiary"])
    scrollbar_good = ttk.Scrollbar(gallery_good_frame, orient="vertical", command=gallery_canvas_good.yview)
    gallery_canvas_good.configure(yscrollcommand=scrollbar_good.set)

    gallery_good_list = tk.Frame(gallery_canvas_good, bg=colors["tertiary"])
    gallery_canvas_good.create_window((0, 0), window=gallery_good_list, anchor="nw")

    gallery_canvas_good.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_good.pack(side=tk.RIGHT, fill=tk.Y)

    # Canvas and Scrollbar for Bad Posture Gallery
    gallery_canvas_bad = tk.Canvas(gallery_bad_frame, bg=colors["tertiary"])
    scrollbar_bad = ttk.Scrollbar(gallery_bad_frame, orient="vertical", command=gallery_canvas_bad.yview)
    gallery_canvas_bad.configure(yscrollcommand=scrollbar_bad.set)

    gallery_bad_list = tk.Frame(gallery_canvas_bad, bg=colors["tertiary"])
    gallery_canvas_bad.create_window((0, 0), window=gallery_bad_list, anchor="nw")

    gallery_canvas_bad.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_bad.pack(side=tk.RIGHT, fill=tk.Y)

    # Function to open images in a new window
    def open_image(full_path):
        """Opens the image in a new window when clicked."""
        top = tk.Toplevel()
        img = Image.open(full_path)
        img = img.resize((500, 500), Image.Resampling.LANCZOS)  # Resize image for full display
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(top, image=photo)
        label.image = photo  # Keep reference to avoid garbage collection
        label.pack()

    # Function to add thumbnails to the gallery
    def add_thumbnails_to_gallery(folder_path, gallery_frame):
        """Adds thumbnails to the gallery section."""
        if not os.path.exists(folder_path):
            return

        image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
        for i, img_path in enumerate(image_files):
            image = Image.open(img_path)
            image.thumbnail((200, 150))  # Create a thumbnail size
            img_thumb = ImageTk.PhotoImage(image)

            # Frame for each thumbnail
            frame = tk.Frame(gallery_frame, bg=colors["tertiary"])
            frame.grid(row=i // 3, column=i % 3, padx=10, pady=10)

            # Thumbnail label
            img_label = tk.Label(frame, image=img_thumb, bg=colors["tertiary"])
            img_label.image = img_thumb  # Keep reference
            img_label.pack()

            # Bind thumbnail click to open the full-size image
            img_label.bind("<Button-1>", lambda e, path=img_path: open_image(path))

    # Add thumbnails to the good and bad posture galleries
    good_posture_folder = "path_to_good_posture_images"  # Replace with actual path
    bad_posture_folder = "path_to_bad_posture_images"    # Replace with actual path

    add_thumbnails_to_gallery(good_posture_folder, gallery_good_list)  # Thumbnails for good posture
    add_thumbnails_to_gallery(bad_posture_folder, gallery_bad_list)    # Thumbnails for bad posture

    # Live Camera View Frame
    live_frame = tk.Frame(root, bg=colors["tertiary"])
    live_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 200))


    root.grid_columnconfigure(0, weight=1)  # This is for the gallery or recommendation section
    root.grid_columnconfigure(1, weight=2)  # This is for the live camera view to take less space
    root.grid_rowconfigure(0, weight=1)     # Ensures vertical expansion

    # Live Label for the live camera feed
    live_label = tk.Label(live_frame, bg=colors["tertiary"])
    live_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Control Buttons Frame (right of live frame, aligned to top-right edge)
    button_frame = tk.Frame(root, bg=colors["tertiary"])
    button_frame.place(relx=0.98, rely=0.05, anchor="ne")

    # Load Icons for the buttons
    capture_icon = load_icon(capture_icon_path)
    record_icon = load_icon(record_icon_path)
    save_icon = load_icon(save_icon_path)

    # Button Style: Make buttons white for better visibility
    button_bg_color = "white"

    # Hamburger Menu Button (top-right, larger size, now vertically aligned)
    hamburger_menu = tk.Menubutton(button_frame, text="☰", bg=button_bg_color, fg=colors["text"], relief=tk.FLAT, font=("Helvetica", 28))
    hamburger_menu.pack(side=tk.TOP, padx=5, pady=5)

    # Capture Button
    capture_button = tk.Button(button_frame, image=capture_icon, command=capture_image, bg=button_bg_color, relief=tk.FLAT)
    capture_button.image = capture_icon
    capture_button.pack(side=tk.TOP, padx=5, pady=5)

    # Record Button
    start_button = tk.Button(button_frame, image=record_icon, command=start_live_capture, bg=button_bg_color, relief=tk.FLAT)
    start_button.image = record_icon
    start_button.pack(side=tk.TOP, padx=5, pady=5)

    # Save Button
    stop_button = tk.Button(button_frame, image=save_icon, command=stop_live_capture, bg=button_bg_color, relief=tk.FLAT)
    stop_button.image = save_icon
    stop_button.pack(side=tk.TOP, padx=5, pady=5)

    # Create the dropdown Menu for the hamburger button
    menu = tk.Menu(hamburger_menu, tearoff=0)
    hamburger_menu.config(menu=menu)

    # Add options to the hamburger menu
    menu.add_command(label="Home", command=lambda: print("Home clicked"))
    menu.add_command(label="Progress", command=open_progress_window)
    menu.add_command(label="Settings", command=lambda: print("Settings clicked"))
    menu.add_separator()
    menu.add_command(label="Exit", command=root.quit)

    # Run the Tkinter main loop
    root.mainloop()


if __name__ == "__main__":
    initialize_gui()
