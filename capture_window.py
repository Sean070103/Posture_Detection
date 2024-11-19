import customtkinter as ctk
from tkinter import Label
from PIL import Image, ImageTk
import cv2
import threading
import os
from ultralytics import YOLO
from tkinter import filedialog
import time
import json
import random
import tkinter as tk
from customtkinter import CTkImage
import ui


# Define file paths
model_keypoints_path = r'yolov8n-pose.pt'
model_classification_path = r'best.pt'
keypoints_dir = r'gallery\photos\keypoints'
patient_data_dir = r"patient_data"

live_label = None
good_gallery_scrollable = None
bad_gallery_scrollable = None

# Load YOLO models
model_keypoints = YOLO(model_keypoints_path)
model_classification = YOLO(model_classification_path)

# Initialize customtkinter application
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# Initialize the main window
root = ctk.CTk()
root.title("Live Posture Detection")
root.geometry("1200x800")

# Configure grid
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Global variables
# cap = None
capturing = False

# Recommendations
good_posture_recommendations = [
    "Maintain a straight back.",
    "Keep your shoulders relaxed.",
    "Sit upright and evenly distribute weight."
]
bad_posture_recommendations = [
    "Avoid slouching.",
    "Align your spine with your neck.",
    "Keep your shoulders back."
]



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


colors = {
    "background": "#36393e",
    "text": "white",
    "tertiary": "#424549"
}










# Start live capturing
def start_live_capture():
    global cap, capturing
    if not capturing:
        cap = cv2.VideoCapture(0)
        capturing = True
        update_frame()

# Stop live capturing
def stop_live_capture():
    global cap, capturing
    capturing = False
    if cap is not None and cap.isOpened():
        cap.release()
        cap = None

# Update the live feed
def update_frame():
    global cap
    global live_label
    width, height = 640, 480
    if cap is not None and cap.isOpened():
        try:
            # Read a new frame
            ret, frame = cap.read()
            if ret:
                # Perform keypoints detection using the current frame
                keypoints_results = model_keypoints(frame)
                if keypoints_results and len(keypoints_results) > 0:
                    # Draw keypoints and lines (skeleton) on the frame
                    annotated_frame = keypoints_results[0].plot()

                    # Perform posture classification using the frame
                    boxes = keypoints_results[0].boxes.xyxy
                    if boxes is not None:
                        for box in boxes:
                            
                            x1, y1, x2, y2 = map(int, box)
                            # print(x1)
                            # print(x2)
                            # print(y1)
                            # print(y2)
                            roi = frame[y1:y2, x1:x2]

                            # Perform posture classification on the ROI
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

                # Convert frame for display in the GUI
                cv2image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                # imgtk = ImageTk.PhotoImage(image=img)
                imgtk = CTkImage(img, size=(width, height))
                live_label.imgtk = imgtk
                live_label.configure(image=imgtk)
                live_label.update_idletasks()





        except Exception as e:
            print(f"An error occurred in update_frame: {e}")

    live_label.after(10, update_frame)

patient_id=""






def capture_image(name):
    global capturing
    global patient_id
    for i in range(100):
        print(capturing)
    if capturing and cap is not None and cap.isOpened():
        
        

        capturing = True

        def capture_task():
            global capturing
            posture_text = "Good"  # Default text

            try:
                ret, frame = cap.read()
                if ret:
                    # Perform keypoint detection
                    keypoints_results = model_keypoints(frame)
                    if keypoints_results and len(keypoints_results) > 0:
                        annotated_frame = keypoints_results[0].plot()
                        boxes = keypoints_results[0].boxes.xyxy

                        if boxes is not None:
                            for box in boxes:
                                x1, y1, x2, y2 = map(int, box)
                                roi = frame[y1:y2, x1:x2]

                                # Perform posture classification
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

                                        # Annotate image
                                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                                        text_position_x = int((x1 + x2) / 2) - 20
                                        cv2.putText(
                                            annotated_frame,
                                            posture_text,
                                            (text_position_x, y1 - 10),
                                            cv2.FONT_HERSHEY_SIMPLEX,
                                            0.5,
                                            color,
                                            2,
                                        )

                        # Save annotated image and keypoints
                        timestamp = int(time.time())
                        print(name != "nigga")
                        print(name)
                        print("bruh")
                        
                        folder = f"C:\\Users\\garci\\Documents\\GitHub\\Bruh\\Posture_Detection\\patient_data\\{name}"
                        good_posture_folder = f"C:\\Users\\garci\\Documents\\GitHub\\Bruh\\Posture_Detection\\patient_data\\{name}\\good_posture"
                        bad_posture_folder = f"C:\\Users\\garci\\Documents\\GitHub\\Bruh\\Posture_Detection\\patient_data\\{name}\\bad_posture"
                        # folder = bad_posture_folder if posture_text == "Bad" else good_posture_folder
                        if posture_text == "Bad":
                            img_name = os.path.join(bad_posture_folder, f"image_with_keypoints_{timestamp}.png")
                        else:
                            img_name = os.path.join(good_posture_folder, f"image_with_keypoints_{timestamp}.png")
                        
                        # C:\Users\garci\Documents\GitHub\Bruh\Posture_Detection\patient_data\nigga
                        # img_name = os.path.join(folder, f"image_with_keypoints_{timestamp}.png")
                        
                        cv2.imwrite(img_name, annotated_frame)
                        # Update the gallery with the captured image immediately
                        gallery_frame(img_name, posture_text)

                    else:
                        print("No keypoints detected.")
                else:
                    print("Failed to capture frame.")
            except Exception as e:
                print(f"Error during capture: {e}")
            finally:
                capturing = True

        # Start the capture task in a separate thread
        threading.Thread(target=capture_task).start()







def gallery_frame(img_path, posture, text_wraplength=200, text_width=40, text_height=5):
    global good_gallery_scrollable
    global bad_gallery_scrollable
    """
    Updates the gallery with the captured image and adds it to the corresponding section
    based on posture classification. Also includes an adjustable recommendation text for both good and bad posture.

    Parameters:
    img_path (str): Path to the image to be added.
    posture (str): Either 'good' or 'bad' posture.
    """
    try:
        # Create a thumbnail for the gallery
        thumbnail_size = (200, 200)
        img = Image.open(img_path)
        img.thumbnail(thumbnail_size)
        thumbnail = ImageTk.PhotoImage(img)

        # Store a reference to the image to prevent garbage collection
        img_ref = {"image": thumbnail}

        if posture.lower() == "good":
            # Get a random recommendation for good posture
            recommendation = random.choice(good_posture_recommendations)

            # Create a frame for the image and the recommendation text
            frame = tk.Frame(good_gallery_scrollable, bg=colors["tertiary"])

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
                wraplength=text_wraplength,
                width=text_width,
                height=text_height
            )
            text_label.grid(row=0, column=1, padx=10, sticky='w')

            # Add frame to the good posture gallery
            frame.pack(pady=5, padx=5, anchor="w")

            # Store image reference in the scrollable frame for persistence
            good_gallery_scrollable.img_refs = getattr(good_gallery_scrollable, 'img_refs', []) + [img_ref]

        else:
            # Get a random recommendation for bad posture
            recommendation = random.choice(bad_posture_recommendations)

            # Create a frame for the image and the recommendation text
            frame = tk.Frame(bad_gallery_scrollable, bg=colors["tertiary"])

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
                wraplength=text_wraplength,
                width=text_width,
                height=text_height
            )
            text_label.grid(row=0, column=1, padx=10, sticky='w')

            # Add frame to the bad posture gallery
            frame.pack(pady=5, padx=5, anchor="w")

            # Store image reference in the scrollable frame for persistence
            bad_gallery_scrollable.img_refs = getattr(bad_gallery_scrollable, 'img_refs', []) + [img_ref]

    except Exception as e:
        print(f"Error updating gallery: {e}")





gallery_good_list = []  # List to store good posture images
gallery_bad_list = []   # List to store bad posture images


gallery_canvas_good = tk.Canvas(root, width=300, height=300)
gallery_canvas_bad = tk.Canvas(root, width=300, height=300)


bad_posture_folder = f".\\patient_data\\{patient_id}\\bad_posture"
good_posture_folder = f".\\patient_data\\{patient_id}\\good_posture"


 # Ensure the directories exist
os.makedirs( f".\\patient_data\\{patient_id}\\bad_posture", exist_ok=True)
os.makedirs(f".\\patient_data\\{patient_id}\\good_posture", exist_ok=True)



























# Initialize patient ID and folders properly
patient_id = ""

def initialize_patient_folders():
    global patient_id
    if not patient_id:
        print("Patient ID is not set.")
        return
    
    # Create patient-specific directories
    global bad_posture_folder, good_posture_folder
    bad_posture_folder = f".\\patient_data\\{patient_id}\\bad_posture"
    good_posture_folder = f".\\patient_data\\{patient_id}\\good_posture"
    os.makedirs(bad_posture_folder, exist_ok=True)
    os.makedirs(good_posture_folder, exist_ok=True)














def prompt_patient_id():
    global patient_id
    patient_id = input("Enter Patient ID: ").strip()
    initialize_patient_folders()







                   











def save_data():
    print("Save button clicked")



def toggle_gallery_visibility(frame, button):
    if frame.winfo_viewable():
        frame.pack_forget()
        button.configure(text="Expand")
    else:
        frame.pack(fill="both", padx=10, pady=10)
        button.configure(text="Collapse")

def open_capture_window(master, name):
    print(name)
    global root
    global good_gallery_scrollable
    global bad_gallery_scrollable
    global live_label
    # Left-side gallery frame containing "Good" and "Bad" posture sections
    gallery_frame = ctk.CTkFrame(root, fg_color="#2f3136")
    gallery_frame.grid(row=0, column=0, rowspan=2, sticky="nswe", padx=5, pady=5)

    # Good Posture Frame with Label, Minimize/Maximize Button, and Scrollable Area
    good_frame = ctk.CTkFrame(master=gallery_frame, fg_color="#36393e", corner_radius=10)
    good_frame.pack(fill="x", padx=10, pady=(10, 5))

    good_label_frame = ctk.CTkFrame(master=good_frame, fg_color="#36393e")  # Header frame for title and buttons
    good_label_frame.pack(fill="x")

    good_label = ctk.CTkLabel(master=good_label_frame, text="Good Posture", fg_color="#36393e", font=("Arial", 12))
    good_label.pack(side="left", padx=10, pady=5)

    good_toggle_button = ctk.CTkButton(master=good_label_frame, text="Minimize", width=10,
                                    command=lambda: toggle_gallery_visibility(good_gallery_scrollable, good_toggle_button))
    good_toggle_button.pack(side="right", padx=5, pady=5)

    # Scrollable area for Good Posture images
    good_gallery_scrollable = ctk.CTkScrollableFrame(master=good_frame, width=180, height=150, fg_color="#2f3136", corner_radius=10)
    good_gallery_scrollable.pack(fill="x", padx=5, pady=(0, 5))

    # Bad Posture Frame with Label, Minimize/Maximize Button, and Scrollable Area
    bad_frame = ctk.CTkFrame(master=gallery_frame, fg_color="#36393e", corner_radius=10)
    bad_frame.pack(fill="x", padx=10, pady=(5, 10))

    bad_label_frame = ctk.CTkFrame(master=bad_frame, fg_color="#36393e")  # Header frame for title and buttons
    bad_label_frame.pack(fill="x")

    bad_label = ctk.CTkLabel(master=bad_label_frame, text="Bad Posture", fg_color="#36393e", font=("Arial", 12))
    bad_label.pack(side="left", padx=10, pady=5)

    bad_toggle_button = ctk.CTkButton(master=bad_label_frame, text="Minimize", width=10,
                                    command=lambda: toggle_gallery_visibility(bad_gallery_scrollable, bad_toggle_button))
    bad_toggle_button.pack(side="right", padx=5, pady=5)

    # Scrollable area for Bad Posture images
    bad_gallery_scrollable = ctk.CTkScrollableFrame(master=bad_frame, width=180, height=150, fg_color="#2f3136", corner_radius=10)
    bad_gallery_scrollable.pack(fill="x", padx=5, pady=(0, 5))


    # Center live capture frame
    capture_frame = ctk.CTkFrame(root, fg_color="#d3d3d3")
    capture_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")











    # Configure capture frame to expand with resizing
    capture_frame.grid_rowconfigure(0, weight=1)
    capture_frame.grid_columnconfigure(0, weight=1)


    # Label to show the live video feed
    live_label = ctk.CTkLabel(capture_frame, text="")
    live_label.grid(row=0, column=0, sticky="nsew")


    # Enlarged comment section at the bottom
    comment_section = ctk.CTkTextbox(root, height=75, fg_color="white", corner_radius=10)
    comment_section.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

    # Right-side button frame
    button_frame = ctk.CTkFrame(root, fg_color="#2f3136")
    button_frame.grid(row=0, column=2, rowspan=2, sticky="nswe", padx=5, pady=5)

    # Configure button frame grid for responsiveness
    button_frame.grid_rowconfigure(0, weight=1)
    button_frame.grid_rowconfigure(1, weight=0)
    button_frame.grid_rowconfigure(2, weight=1)




    # # Buttons with icons and commands
    # buttons = [
    #     ("Capture", capture_image),
    #     ("Start Live Capture", start_live_capture),
    #     ("Save", save_data),

    # ]

    # button_container = ctk.CTkFrame(button_frame, fg_color="#2f3136")
    # button_container.grid(row=1, column=0, padx=10, pady=10)

    # for i, (text, command) in enumerate(buttons):
    #     button = ctk.CTkButton(button_container, text=text, command=command, fg_color="#424549", text_color="white", width=150)
    #     button.grid(row=i, column=0, padx=10, pady=10, sticky="n")



    # Buttons with icons and commands
    button_container = ctk.CTkFrame(button_frame, fg_color="#2f3136")
    button_container.grid(row=1, column=0, padx=10, pady=10)

    # # Manually initialize each button
    # button_capture = ctk.CTkButton(
    #     button_container, text="Capture", command=capture_image, 
    #     fg_color="#424549", text_color="white", width=150
    # )

    # button_capture.grid(row=0, column=0, padx=10, pady=10, sticky="n")

    # button_start_live_capture = ctk.CTkButton(
    #     button_container, text="Start Live Capture", command=start_live_capture, 
    #     fg_color="#424549", text_color="white", width=150
    # )
    # button_start_live_capture.grid(row=1, column=0, padx=10, pady=10, sticky="n")

    # button_save = ctk.CTkButton(
    #     button_container, text="Save", command=save_data, 
    #     fg_color="#424549", text_color="white", width=150
    # )
    # button_save.grid(row=2, column=0, padx=10, pady=10, sticky="n")


    # Update this section in open_capture_window
    button_capture = tk.Button(
        button_container, text="Capture", command=lambda: capture_image(name),
        bg="#424549", fg="white", width=20  # Adjust the styling for tk.Button
    )
    button_capture.grid(row=0, column=0, padx=10, pady=10, sticky="n")

    button_start_live_capture = tk.Button(
        button_container, text="Start Live Capture", command=start_live_capture,
        bg="#424549", fg="white", width=20
    )
    button_start_live_capture.grid(row=1, column=0, padx=10, pady=10, sticky="n")

    button_save_data = tk.Button(
        button_container, text="Save", command=save_data,
        bg="#424549", fg="white", width=20
    )
    button_save_data.grid(row=2, column=0, padx=10, pady=10, sticky="n")

# shi()


    # Run the application
    root.mainloop()  