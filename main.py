from customtkinter import CTk, set_appearance_mode
import ui  # Importing the ui module
import capture_window

# Initialize the main app window
app = CTk()
app.geometry("900x500")
app.title("Session Gallery and Patient Selection")
set_appearance_mode("dark")

# Configure main window grid layout
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=3)  # Left frame takes more width
app.grid_columnconfigure(1, weight=2)  # Right frame takes less width

# Initialize each section from the ui module
ui.create_session_gallery_section(app)
ui.create_patient_selection_section(app)
ui.get_app(app)

# Start the application loop
app.mainloop()
  
