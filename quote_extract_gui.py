from paddleocr import PaddleOCR
from PIL import Image
import os
import sqlite3
import json
import re
import tkinter as tk
from tkinter import messagebox, ttk

# SQLite DB setup
DB_FILE = 'quotes.db'  # Name of the database file

# Initialize PaddleOCR
ocr_model = PaddleOCR(use_angle_cls=True, lang='en')  # OCR model for extracting text from images

def create_db():
    """Create the quotes database if it doesn't already exist."""
    conn = sqlite3.connect(DB_FILE)  # Connect to the database
    c = conn.cursor()  # Create a cursor to execute SQL commands
    c.execute('''CREATE TABLE IF NOT EXISTS quotes
                 (file_name TEXT, quote TEXT)''')  # Define the database schema
    conn.commit()  # Save changes
    conn.close()  # Close the connection

def insert_quote(file_name, quote):
    """Insert a new quote into the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO quotes (file_name, quote) VALUES (?, ?)", (file_name, quote))
    conn.commit()
    conn.close()

def get_all_quotes():
    """Retrieve all quotes from the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM quotes")
    quotes = c.fetchall()  # Fetch all rows
    conn.close()
    return quotes

def clear_quotes():
    """Delete all quotes from the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM quotes")  # SQL command to clear all rows
    conn.commit()
    conn.close()

def clean_text(text):
    """Clean and format the extracted text."""
    # Replace extra spaces and fix punctuation spacing
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"([.,!?])([a-zA-Z])", r"\1 \2", text)
    text = re.sub(r"([a-zA-Z])([.,!?])", r"\1 \2", text)
    text = text.replace(" .", ".").replace(" ,", ",").replace(" !", "!").replace(" ?", "?")
    text = re.sub(r"\s+([.,!?])", r"\1", text)
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    return text.strip().capitalize()  # Capitalize the first letter of the cleaned text

def extract_text_from_images():
    """Extract quotes from images in the downloads folder using PaddleOCR."""
    extracted_data = []  # List to store results
    downloads_folder = "./downloads"  # Path to the folder with images

    if not os.path.exists(downloads_folder):
        print(f"The folder '{downloads_folder}' does not exist.")
        return []

    for filename in os.listdir(downloads_folder):
        file_path = os.path.join(downloads_folder, filename)

        # Check if the file is an image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            try:
                # Use PaddleOCR to process the image
                results = ocr_model.ocr(file_path, cls=True)
                raw_text = " ".join([res[1][0] for res in results[0]])  # Extract detected text
                cleaned_text = clean_text(raw_text)
                extracted_data.append((filename, cleaned_text))  # Add the filename and text to the list
            except Exception as e:
                extracted_data.append((filename, f"Error: {e}"))  # Handle errors gracefully

    return extracted_data

def run_quote_extract_gui(tab_frame):
    """Setup the Quote Extractor GUI in the provided frame."""
    label = tk.Label(tab_frame, text="Extract quotes from images:", font=("Comic Sans MS", 16))
    label.pack(pady=10)

    def process_quotes():
        """Extract quotes from images and display them in the table."""
        extracted_data = extract_text_from_images()  # Call the OCR function

        if extracted_data:
            # Clear any existing entries in the table
            for row in treeview.get_children():
                treeview.delete(row)

            # Add the new quotes to the table
            for filename, quote in extracted_data:
                treeview.insert("", "end", values=(filename, quote[:100]))  # Clip long quotes to 100 characters

            # Save the extracted quotes to the database
            for filename, quote in extracted_data:
                insert_quote(filename, quote)

        else:
            messagebox.showinfo("No Quotes", "No quotes were extracted.")  # Show a message if no quotes are found

    # Button to trigger the quote extraction process
    extract_button = tk.Button(
        tab_frame, text="✨ Extract Quotes", font=("Comic Sans MS", 12), bg="#ff69b4", fg="white", command=process_quotes
    )
    extract_button.pack(pady=10)

    # Label for the table section
    extracted_label = tk.Label(tab_frame, text="Extracted Quotes:", font=("Comic Sans MS", 14, "bold"))
    extracted_label.pack(pady=10)

    # Table to display extracted quotes
    columns = ("File Name", "Quote")
    table_frame = tk.Frame(tab_frame)
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    treeview = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
    treeview.pack(side="left", fill="both", expand=True)

    # Configure table columns
    treeview.column("File Name", width=100, anchor="center")
    treeview.column("Quote", width=300, anchor="w", stretch=True)

    # Set column headers
    treeview.heading("File Name", text="File Name")
    treeview.heading("Quote", text="Quote")

    # Scrollbar for the table
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=treeview.yview)
    scrollbar.pack(side="right", fill="y")
    treeview.config(yscrollcommand=scrollbar.set)

    # Buttons for clearing and exporting quotes
    button_frame = tk.Frame(tab_frame)
    button_frame.pack(pady=10)

    # Clear all quotes button
    clear_button = tk.Button(
        button_frame, text="🧹 Clear Quotes", font=("Comic Sans MS", 12), bg="#ff69b4", fg="white", command=lambda: clear_all_quotes(treeview)
    )
    clear_button.pack(side="left", padx=10)

    # Export quotes button
    export_button = tk.Button(
        button_frame, text="📦 Export Quotes", font=("Comic Sans MS", 12), bg="#ff69b4", fg="white", command=export_to_json
    )
    export_button.pack(side="left", padx=10)

    create_db()  # Initialize the database
    for row in get_all_quotes():  # Load quotes from the database into the table
        treeview.insert("", "end", values=row)

def export_to_json():
    """Export all quotes to a JSON file."""
    quotes = get_all_quotes()  # Get all quotes from the database
    quotes_list = []
    for quote in quotes:
        quotes_list.append({
            'file_name': quote[0],
            'quote': quote[1]
        })

    try:
        with open('quotes_export.json', 'w') as f:  # Write the quotes to a JSON file
            json.dump(quotes_list, f, indent=4)
        messagebox.showinfo("Success", "Quotes exported successfully to quotes_export.json")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export quotes: {str(e)}")

def clear_all_quotes(treeview):
    """Clear all quotes from the table and database."""
    clear_quotes()  # Clear the database
    for row in treeview.get_children():  # Remove entries from the table
        treeview.delete(row)
