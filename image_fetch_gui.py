import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from utils.image_fetcher import fetch_images_bing
from zipfile import ZipFile
import os

# Constants
fetching_images = False  # A flag to prevent multiple fetch operations at once
DOWNLOAD_FOLDER = "./downloads"  # Folder where images will be saved
THUMBNAIL_SIZE = (150, 150)  # Size for thumbnail previews

def fetch_images(search_entry, num_images_entry):
    """Fetch images based on user input."""
    global fetching_images
    if fetching_images:
        return  # If an operation is already running, exit this function

    # Get the search query and number of images from the input fields
    search_query = search_entry.get()
    num_images = int(num_images_entry.get())

    # Validate user input
    if not search_query or not num_images:
        messagebox.showerror("Error", "Please provide both search query and number of images.")
        return

    fetching_images = True  # Set the flag to indicate an operation is running
    clear_folder()  # Remove any previously fetched images
    fetch_images_bing(search_query, num_images, DOWNLOAD_FOLDER)  # Call the fetcher function
    fetching_images = False  # Reset the flag after operation is done

    # Check if any images were actually downloaded
    if not os.listdir(DOWNLOAD_FOLDER):
        messagebox.showerror("Error", "No images found. Please try a different search term.")
    else:
        update_file_list()  # Refresh the file list display
        messagebox.showinfo("✨ Success", f"Images fetched and saved to {os.path.abspath(DOWNLOAD_FOLDER)}")

def clear_folder():
    """Delete all files in the download folder."""
    for widget in file_list_frame.winfo_children():
        widget.destroy()  # Clear any displayed files
    for filename in os.listdir(DOWNLOAD_FOLDER):
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)  # Remove the file
    update_file_list()  # Update the display

def update_file_list():
    """Refresh the list of files in the download folder."""
    for widget in file_list_frame.winfo_children():
        widget.destroy()

    # If the folder is empty, display a message
    if not os.listdir(DOWNLOAD_FOLDER):
        tk.Label(file_list_frame, text="No files found", font=("Comic Sans MS", 12, "bold"), bg="#fff9f9").pack()
        return

    # Display each file in the folder
    for filename in os.listdir(DOWNLOAD_FOLDER):
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        file_size = os.path.getsize(file_path) / 1024  # Calculate size in KB
        file_size = round(file_size, 2)  # Round to 2 decimal places

        # Create a container for the file info
        file_container = tk.Frame(file_list_frame, bg="#ffe4f8", bd=5, relief="groove")
        file_container.pack(fill="x", padx=50, pady=5)

        # Add a shadow effect
        shadow_container = tk.Frame(file_container, bg="#bdbdbd")
        shadow_container.pack(side="left", padx=(2, 0), pady=2)

        # Add a thumbnail preview if the file is an image
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            thumbnail = create_thumbnail(file_path)
            if thumbnail:
                thumbnail_label = tk.Label(shadow_container, image=thumbnail, bg="#ffffff")
                thumbnail_label.image = thumbnail
                thumbnail_label.pack(side="left", padx=2, pady=2)

        # Display file name and size
        file_label = tk.Label(file_container, text=f"{filename} ({file_size} KB)", font=("Comic Sans MS", 10, "bold"), bg="#ffe4f8")
        file_label.pack(side="left", padx=10, pady=5)

        # Add buttons to open or delete the file
        open_button = tk.Button(file_container, text="🔓 Open Image", font=("Comic Sans MS", 10), bg="#ff6f91", fg="white",
                                command=lambda f=file_path: open_image(f))
        open_button.pack(side="left", padx=5, pady=5)

        delete_button = tk.Button(file_container, text="🗑️ Delete", font=("Comic Sans MS", 10), bg="#ff6f91", fg="white",
                                  command=lambda f=file_path: delete_file(f))
        delete_button.pack(side="left", padx=5, pady=5)

def create_thumbnail(image_path, size=(150, 150)):
    """Create a thumbnail of an image for preview."""
    try:
        img = Image.open(image_path)
        img.thumbnail(size)  # Resize the image
        return ImageTk.PhotoImage(img)  # Return the thumbnail
    except Exception as e:
        print(f"Error creating thumbnail for {image_path}: {e}")
        return None

def delete_file(file_path):
    """Delete a file from the folder."""
    try:
        os.remove(file_path)
        update_file_list()  # Refresh the file list
        messagebox.showinfo("Success", "Image deleted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting file: {str(e)}")

def open_image(image_path):
    """Open an image using the system's default viewer."""
    try:
        os.startfile(image_path)  # For Windows
    except AttributeError:
        subprocess.call(["open", image_path])  # For macOS/Linux

def export_all():
    """Export all images in the download folder to a ZIP file."""
    output_file = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip")])
    if output_file:
        try:
            with ZipFile(output_file, 'w') as zipf:
                for root, dirs, files in os.walk(DOWNLOAD_FOLDER):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, DOWNLOAD_FOLDER))
            messagebox.showinfo("Success", f"Images exported successfully to {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting images: {str(e)}")

def run_image_fetch_gui(tab_frame):
    """Setup the Image Fetcher GUI."""
    global search_entry, num_images_entry, file_list_frame

    root = tab_frame

    # Background setup
    bg_image = Image.open("assets/background.png")
    bg_image = bg_image.resize((900, 600), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)  # Ensure it covers the entire root window
    root.bg_image = bg_photo  # Keep a reference to prevent garbage collection

    # Create a frame for search inputs
    search_frame = tk.Frame(root, bg="#fff9f9", bd=5, relief="ridge")
    search_frame.place(relx=0.5, rely=0.1, anchor="n", width=800, height=200)

    # Add labels and input fields for search query and number of images
    tk.Label(search_frame, text="🔍 Search Query:", font=("Comic Sans MS", 14, "bold"), bg="#fff9f9").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    search_entry = ttk.Entry(search_frame, font=("Comic Sans MS", 14), width=30)
    search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tk.Label(search_frame, text="📸 Number of Images:", font=("Comic Sans MS", 14, "bold"), bg="#fff9f9").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    num_images_entry = ttk.Entry(search_frame, font=("Comic Sans MS", 14), width=10)
    num_images_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # Buttons for fetching, clearing, and exporting images
    button_frame = tk.Frame(search_frame, bg="#fff9f9")
    button_frame.grid(row=2, column=0, columnspan=2, pady=10)

    fetch_button = tk.Button(
        button_frame, text="✨ Fetch Images", font=("Comic Sans MS", 12, "bold"), bg="#ff69b4", fg="white",
        command=lambda: fetch_images(search_entry, num_images_entry)
    )
    fetch_button.pack(side="left", padx=10)

    clear_button = tk.Button(
        button_frame, text="🧹 Clear Folder", font=("Comic Sans MS", 12), bg="#ff69b4", fg="white",
        command=clear_folder
    )
    clear_button.pack(side="left", padx=10)

    export_button = tk.Button(
        button_frame, text="📦 Export All", font=("Comic Sans MS", 12), bg="#ff69b4", fg="white",
        command=export_all
    )
    export_button.pack(side="left", padx=10)

    # File list section
    file_list_label = tk.Label(root, text="📂 Downloaded Files:", font=("Comic Sans MS", 14, "bold"), bg="#fff9f9", fg="#333")
    file_list_label.place(relx=0.5, rely=0.45, anchor="n")

    file_list_container = tk.Frame(root, bg="#fff9f9", bd=3, relief="groove")
    file_list_container.place(relx=0.5, rely=0.5, anchor="n", relwidth=0.8, relheight=0.5)

    canvas = tk.Canvas(file_list_container, bg="#fff9f9")
    scrollbar = ttk.Scrollbar(file_list_container, orient="vertical", command=canvas.yview)

    file_list_frame = tk.Frame(canvas, bg="#fff9f9")
    file_list_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=file_list_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    update_file_list()  # Initialize the file list
