from customtkinter import CTkLabel, CTkFrame, CTkScrollableFrame, CTkImage
from PIL import Image
import os

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
                image_label = CTkLabel(master=good_scrollable_frame, image=my_image, text="")  # Text empty for image-only display
                image_label.pack(padx=5, pady=5)

            except Exception as e:
                print(f"Error loading image {file_name}: {e}")
    # my_image = CTkImage(light_image=Image.open(f"C:\\Users\\garci\\Desktop\\Sean_Thesis\\patient_data\\{name}\\Good_Posture\\image_with_keypoints_1732110018.png"), size=(30, 30))

    # # Create a label with the image and add it to the scrollable frame
    # image_label = CTkLabel(master=good_scrollable_frame, image=my_image, text="")  # Set text to empty for image-only display
    # image_label.pack(padx=5, pady=5) 

    bad_scrollable_frame = CTkScrollableFrame(master=gallery_frame, fg_color="#A9A9A9")
    bad_scrollable_frame.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
