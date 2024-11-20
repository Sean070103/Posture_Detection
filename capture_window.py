import customtkinter as ctk
import tkinter as tk
import threading
import cv2
from ultralytics import YOLO
from PIL import Image, ImageTk
from customtkinter import CTkImage, CTkLabel
import time
import os
import random
from tkinter import messagebox
import json
from Session_gallery import create_session_gallery_section
# from Patient_selection import Patient_selection

class Capture_window:
    def __init__(self, root, patient_selection_instance):
        self.patient_selection_instance = patient_selection_instance

        self.root = root
        self.cap = None
        self.capturing = False
        
        self.model_keypoints_path = r'yolov8n-pose.pt'
        self.model_keypoints = YOLO(self.model_keypoints_path)

        self.model_classification_path = r'best.pt'
        self.model_classification = YOLO(self.model_classification_path)

        self.capture_frame = ctk.CTkFrame(self.root, fg_color="#d3d3d3")
        self.live_label = ctk.CTkLabel(self.capture_frame, text="")
        self.gallery_frame = ctk.CTkFrame(self.root, fg_color="#2f3136")
        
        self.good_frame = ctk.CTkFrame(master=self.gallery_frame, fg_color="#36393e", corner_radius=10)
        

        self.good_gallery_scrollable = ctk.CTkScrollableFrame(master=self.good_frame, width=180, height=150, fg_color="#2f3136", corner_radius=10)
        
        # Recommendations
        self.good_posture_recommendations = [
            "Maintain a straight back.",
            "Keep your shoulders relaxed.",
            "Sit upright and evenly distribute weight."
        ]

        self.bad_posture_recommendations = [
            "Avoid slouching.",
            "Align your spine with your neck.",
            "Keep your shoulders back."
        ]
        self.bad_frame = ctk.CTkFrame(master=self.gallery_frame, fg_color="#36393e", corner_radius=10)
        self.bad_gallery_scrollable = ctk.CTkScrollableFrame(master=self.bad_frame, width=180, height=150, fg_color="#2f3136", corner_radius=10)

        self.colors = {
            "primary": "#7289da",
            "secondary": "#424549",
            "tertiary": "#36393e",
            "background": "#282b30",
            "text": "#FFFFFF"  # Changed to white for better visibility
        }
        
    def open_capture_window(self, name, patient_selection_instance):
        self.patient_selection_instance = patient_selection_instance
        # Left-side gallery frame con taining "Good" and "Bad" posture sections
        self.gallery_frame.grid(row=0, column=0, rowspan=2, sticky="nswe", padx=5, pady=5)

        # Good Posture Frame with Label, Minimize/Maximize Button, and Scrollable Area
        self.good_frame.pack(fill="x", padx=10, pady=(10, 5))

        good_label_frame = ctk.CTkFrame(master=self.good_frame, fg_color="#36393e")  # Header frame for title and buttons
        good_label_frame.pack(fill="x")

        good_label = ctk.CTkLabel(master=good_label_frame, text="Good Posture", fg_color="#36393e", font=("Arial", 12))
        good_label.pack(side="left", padx=10, pady=5)

        good_toggle_button = ctk.CTkButton(master=good_label_frame, text="Minimize", width=10, command=lambda: self.toggle_gallery_visibility(self.good_gallery_scrollable, good_toggle_button))
        good_toggle_button.pack(side="right", padx=5, pady=5)

        # Scrollable area for Good Posture images
        self.good_gallery_scrollable.pack(fill="x", padx=5, pady=(0, 5))

        # Specify the folder path containing the images
        folder_path = f"C:\\Users\\garci\\Desktop\\Sean_Thesis\\patient_data\\{name}\\Good_Posture"

        # Loop through all image files in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            # Check if the file is an image (you can extend this list with more extensions if needed)
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                try:
                    # Load the image and create a CTkImage
                    image = Image.open(file_path)
                    my_image = CTkImage(light_image=image, size=(100, 100))  # Adjust size as needed

                    # Create a label with the image and add it to the scrollable frame
                    image_label = CTkLabel(master=self.good_gallery_scrollable, image=my_image, text="")  # Text empty for image-only display
                    image_label.pack(padx=5, pady=5)

                except Exception as e:
                    print(f"Error loading image {file_name}: {e}")

        # Bad Posture Frame with Label, Minimize/Maximize Button, and Scrollable Area
        self.bad_frame.pack(fill="x", padx=10, pady=(5, 10))

        bad_label_frame = ctk.CTkFrame(master=self.bad_frame, fg_color="#36393e")  # Header frame for title and buttons
        bad_label_frame.pack(fill="x")

        bad_label = ctk.CTkLabel(master=bad_label_frame, text="Bad Posture", fg_color="#36393e", font=("Arial", 12))
        bad_label.pack(side="left", padx=10, pady=5)

        bad_toggle_button = ctk.CTkButton(master=bad_label_frame, text="Minimize", width=10, command=lambda: self.toggle_gallery_visibility(self.bad_gallery_scrollable, bad_toggle_button))
        bad_toggle_button.pack(side="right", padx=5, pady=5)

        # Scrollable area for Bad Posture images
        self.bad_gallery_scrollable.pack(fill="x", padx=5, pady=(0, 5))

        # Specify the folder path containing the images
        folder_path = f"C:\\Users\\garci\\Desktop\\Sean_Thesis\\patient_data\\{name}\\Bad_Posture"

        # Loop through all image files in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            # Check if the file is an image (you can extend this list with more extensions if needed)
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                try:
                    # Load the image and create a CTkImage
                    image = Image.open(file_path)
                    my_image = CTkImage(light_image=image, size=(100, 100))  # Adjust size as needed

                    # Create a label with the image and add it to the scrollable frame
                    image_label = CTkLabel(master=self.bad_gallery_scrollable, image=my_image, text="")  # Text empty for image-only display
                    image_label.pack(padx=5, pady=5)

                except Exception as e:
                    print(f"Error loading image {file_name}: {e}")


        # Center live capture frame
        self.capture_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Configure capture frame to expand with resizing
        self.capture_frame.grid_rowconfigure(0, weight=1)
        self.capture_frame.grid_columnconfigure(0, weight=1)


        # Label to show the live video feed
        self.live_label.grid(row=0, column=0, sticky="nsew")


        # Enlarged comment section at the bottom
        comment_section = ctk.CTkTextbox(self.root, height=75, fg_color="white", corner_radius=10)
        comment_section.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

        # Right-side button frame
        button_frame = ctk.CTkFrame(self.root, fg_color="#2f3136")
        button_frame.grid(row=0, column=2, rowspan=2, sticky="nswe", padx=5, pady=5)

        

        # Configure button frame grid for responsiveness
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=0)
        button_frame.grid_rowconfigure(2, weight=1)

        # Buttons with icons and commands
        button_container = ctk.CTkFrame(button_frame, fg_color="#2f3136")
        button_container.grid(row=1, column=0, padx=10, pady=10)

        # Update this section in open_capture_window
        button_capture = tk.Button(
            button_container, text="Capture", command=lambda: self.capture_image(name),
            bg="#424549", fg="white", width=20  # Adjust the styling for tk.Button
        )
        button_capture.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        button_start_live_capture = tk.Button(
            button_container, text="Start Live Capture", command=self.start_live_capture,
            bg="#424549", fg="white", width=20
        )
        button_start_live_capture.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        button_save_data = tk.Button(
            button_container, text="Save", command=self.save_data,
            bg="#424549", fg="white", width=20
        )
        button_save_data.grid(row=2, column=0, padx=10, pady=10, sticky="n")
 
        self.root.wm_protocol("WM_DELETE_WINDOW", lambda: self.on_close(name))
        
        self.root.mainloop()

    # def on_close(self, name):
    #     # Show a confirmation dialog
    #     if messagebox.askyesno("Confirm Exit", "Are you sure you want to close the application?"):
    #         # Close the capture window and return to patient selection section
    #         self.root.destroy()  # Close the capture window
    #         self.patient_selection_instance.create_patient_selection_section()  # Return to patient selection section
    #     else:
    #         pass  # Do nothing if the user cancels

    def on_close(self, name):
        # Show a confirmation dialog
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to close the application?"):
            self.root.destroy()  # Close the capture window

            # Import Patient_selection inside the method to avoid circular import
            from Patient_selection import Patient_selection

            # Create a new instance of Tk for patient selection
            new_root = ctk.CTk()  # New Tk window
            
            new_root.title("Session Gallery and Patient Selection")
            new_root.geometry("900x500")
            patients = {}

            with open('patients.json', 'r') as file:
                data = json.load(file)  # Parse JSON into a dictionary
                patients.update(data) 
            
            # Pass the new root to Patient_selection and initialize it
            self.patient_selection_instance = Patient_selection(patients, new_root)
            self.patient_selection_instance.create_patient_selection_section()

            create_session_gallery_section(new_root, name)

            # Start the new Tkinter main loop
            new_root.mainloop()
        else:
            pass  # Do nothing if the user cancels


    def save_data(self):
        print("Save button clicked")

    def start_live_capture(self):
        if not self.capturing:
            self.cap = cv2.VideoCapture(0)
            self.capturing = True
            self.update_frame()
    
    def update_frame(self):
        width, height = 640, 480
        if self.cap is not None and self.cap.isOpened():
            try:
                # Read a new frame
                ret, frame = self.cap.read()
                if ret:
                    # Perform keypoints detection using the current frame
                    keypoints_results = self.model_keypoints(frame)
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
                                classification_results = self.model_classification(roi)
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
                    self.live_label.imgtk = imgtk
                    self.live_label.configure(image=imgtk)
                    self.live_label.update_idletasks()

            except Exception as e:
                print(f"An error occurred in update_frame: {e}")

        self.live_label.after(10, self.update_frame)

    def toggle_gallery_visibility(self, frame, button):
        if frame.winfo_viewable():
            frame.pack_forget()
            button.configure(text="Expand")
        else:
            frame.pack(fill="both", padx=10, pady=10)
            button.configure(text="Collapse")

    def capture_image(self, name):
        for i in range(100):
            print(self.capturing)
        if self.capturing and self.cap is not None and self.cap.isOpened():
            self.capturing = True

            self.capture_task(name)
            # Start the capture task in a separate thread
            threading.Thread(target=self.capture_task).start()
    
    def capture_task(self, name):
        posture_text = "Good"  # Default text

        try:
            ret, frame = self.cap.read()
            if ret:
                # Perform keypoint detection
                keypoints_results = self.model_keypoints(frame)
                if keypoints_results and len(keypoints_results) > 0:
                    annotated_frame = keypoints_results[0].plot()
                    boxes = keypoints_results[0].boxes.xyxy

                    if boxes is not None:
                        for box in boxes:
                            x1, y1, x2, y2 = map(int, box)
                            roi = frame[y1:y2, x1:x2]

                            # Perform posture classification
                            classification_results = self.model_classification(roi)
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
                    
                    folder = f"C:\\Users\\garci\\Desktop\\Sean_Thesis\\patient_data\\{name}"
                    good_posture_folder = f"C:\\Users\\garci\\Desktop\\Sean_Thesis\\patient_data\\{name}\\Good_Posture"
                    bad_posture_folder = f"C:\\Users\\garci\\Desktop\\Sean_Thesis\\patient_data\\{name}\\Bad_Posture"
                    # folder = bad_posture_folder if posture_text == "Bad" else good_posture_folder
                    if posture_text == "Bad":
                        img_name = os.path.join(bad_posture_folder, f"image_with_keypoints_{timestamp}.png")
                    else:
                        img_name = os.path.join(good_posture_folder, f"image_with_keypoints_{timestamp}.png")
                    
                    # C:\Users\garci\Documents\GitHub\Bruh\Posture_Detection\patient_data\nigga
                    # img_name = os.path.join(folder, f"image_with_keypoints_{timestamp}.png")
                    
                    cv2.imwrite(img_name, annotated_frame)
                    # Update the gallery with the captured image immediately
                    self.gallery_frame_(img_name, posture_text)

                else:
                    print("No keypoints detected.")
            else:
                print("Failed to capture frame.")
        except Exception as e:
            print(f"Error during capture: {e}")
        finally:
            self.capturing = True



    def gallery_frame_(self, img_path, posture, text_wraplength=200, text_width=40, text_height=5):
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
                recommendation = random.choice(self.good_posture_recommendations)

                # Create a frame for the image and the recommendation text
                frame = tk.Frame(self.good_gallery_scrollable, bg=self.colors["tertiary"])

                # Image label
                image_label = tk.Label(frame, image=thumbnail, bg=self.colors["tertiary"])
                image_label.image = thumbnail  # Keep a reference to avoid garbage collection
                image_label.grid(row=0, column=0, padx=5)

                # Recommendations label for good posture
                text_label = tk.Label(
                    frame,
                    text=recommendation,
                    bg=self.colors["tertiary"],
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
                self.good_gallery_scrollable.img_refs = getattr(self.good_gallery_scrollable, 'img_refs', []) + [img_ref]

            else:
                # Get a random recommendation for bad posture
                recommendation = random.choice(self.bad_posture_recommendations)

                # Create a frame for the image and the recommendation text
                frame = tk.Frame(self.bad_gallery_scrollable, bg=self.colors["tertiary"])

                # Image label
                image_label = tk.Label(frame, image=thumbnail, bg=self.colors["tertiary"])
                image_label.image = thumbnail  # Keep a reference to avoid garbage collection
                image_label.grid(row=0, column=0, padx=5)

                # Recommendations label for bad posture
                text_label = tk.Label(
                    frame,
                    text=recommendation,
                    bg=self.colors["tertiary"],
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
                self.bad_gallery_scrollable.img_refs = getattr(self.bad_gallery_scrollable, 'img_refs', []) + [img_ref]

        except Exception as e:
            print(f"Error updating gallery: {e}")


# a = Capture_window()
# a.open_capture_window("qwe")