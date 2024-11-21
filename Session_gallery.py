from customtkinter import CTkLabel, CTkFrame, CTkScrollableFrame, CTkImage
from PIL import Image, ImageTk
import os
import customtkinter as ctk


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


# Function to open an image in a new window
def open_image(full_path):
    """Opens the image in a new window when clicked using CustomTkinter."""
    top = ctk.CTkToplevel()  # Create a new Toplevel window in CustomTkinter
    top.geometry("1000x1500")  # Set window size
    top.title("Image Viewer")

    img = Image.open(full_path)
    img = img.resize((1000, 1000), Image.Resampling.LANCZOS)  # Resize image for full display
    photo = ImageTk.PhotoImage(img)

    label = ctk.CTkLabel(top, image=photo, text="")  # Create a label with the image
    label.image = photo  # Keep reference to avoid garbage collection
    label.pack(padx=10, pady=10)  # Add padding around the image for better layout


# Function to create the Session Gallery section (Left Frame)
def create_session_gallery_section(master, name):
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

    # Specify the folder path containing the images
    folder_path_good = f"patient_data\\{name}\\Good_Posture"

    # Loop through all image files in the folder
    for file_name in os.listdir(folder_path_good):
        file_path = os.path.join(folder_path_good, file_name)

        # Check if the file is an image (you can extend this list with more extensions if needed)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            try:
                # Load the image and create a CTkImage
                image = Image.open(file_path)
                my_image = CTkImage(light_image=image, size=(200, 200))  # Adjust size as needed

                # Create a label with the image and add it to the scrollable frame
                image_label = CTkLabel(master=good_scrollable_frame, image=my_image, text="")
                image_label.pack(padx=5, pady=5)

                # Bind a click event to open the image
                image_label.bind("<Button-1>", lambda e, path=file_path: open_image(path))

            except Exception as e:
                print(f"Error loading image {file_name}: {e}")

    bad_scrollable_frame = CTkScrollableFrame(master=gallery_frame, fg_color="#A9A9A9")
    bad_scrollable_frame.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

    # Specify the folder path containing the images
    folder_path_bad = f"patient_data\\{name}\\Bad_Posture"

    # Loop through all image files in the folder
    for file_name in os.listdir(folder_path_bad):
        file_path = os.path.join(folder_path_bad, file_name)

        # Check if the file is an image (you can extend this list with more extensions if needed)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            try:
                # Load the image and create a CTkImage
                image = Image.open(file_path)
                my_image = CTkImage(light_image=image, size=(200, 200))  # Adjust size as needed

                # Create a label with the image and add it to the scrollable frame
                image_label = CTkLabel(master=bad_scrollable_frame, image=my_image, text="")
                image_label.pack(padx=5, pady=5)

                # Bind a click event to open the image
                image_label.bind("<Button-1>", lambda e, path=file_path: open_image(path))

            except Exception as e:
                print(f"Error loading image {file_name}: {e}")


