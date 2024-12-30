import tkinter as tk
from image_fetch_gui import run_image_fetch_gui  # Import the function to run the GUI

def run_image_fetch_main():
    """Initialize the main window for the Image Fetcher application."""
    root = tk.Tk()  # Create the root window
    root.title("Image Fetcher")  # Set the title of the window
    root.geometry("900x600")  # Set the dimensions of the window

    # Create a frame where the Image Fetcher GUI will run
    image_fetch_tab = tk.Frame(root)
    image_fetch_tab.pack(fill="both", expand=True)  # Fill the entire window

    # Run the GUI for the Image Fetcher
    run_image_fetch_gui(image_fetch_tab)

    root.mainloop()  # Start the Tkinter event loop to display the window

# Check if this script is being run directly
if __name__ == "__main__":
    run_image_fetch_main()  # Call the function to start the application
