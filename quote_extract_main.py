import tkinter as tk
from quote_extract_gui import run_quote_extract_gui  # Import the function to run the Quote Extractor GUI

def run_quote_extract_main():
    """Initialize the main window for the Quote Extractor application."""
    root = tk.Tk()  # Create the root window
    root.title("Quote Extractor")  # Set the title of the application
    root.geometry("900x600")  # Set the size of the window

    # Create a frame where the Quote Extractor GUI will run
    quote_extract_tab = tk.Frame(root)
    quote_extract_tab.pack(fill="both", expand=True)  # Fill the entire window with this frame

    # Run the GUI for the Quote Extractor
    run_quote_extract_gui(quote_extract_tab)

    root.mainloop()  # Start the Tkinter event loop to keep the window open

# Check if this script is run directly (not imported)
if __name__ == "__main__":
    run_quote_extract_main()  # Call the function to start the application
