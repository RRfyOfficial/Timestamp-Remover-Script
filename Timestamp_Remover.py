import re
import os
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox, simpledialog
import pdfplumber  # Library for extracting text from PDFs

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            # Extract text from each page and split into lines
            page_text = page.extract_text()
            if page_text:
                lines = page_text.split('\n')
                # Filter out lines that are likely headers or footers
                filtered_lines = [
                    line for line in lines
                    if not re.search(r'(vimeo\.com|https?://|Page \d+ of \d+|^\s*$)', line)
                ]
                # Combine the filtered lines back into text
                text += '\n'.join(filtered_lines) + '\n'
    return text

def remove_timestamps_from_text(text):
    """Remove timestamps from the extracted text."""
    # Define regex pattern to remove timestamps (e.g., 00:00.000 --> 00:00.000)
    timestamp_pattern = r'\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}\.\d{2,3}'
    
    # Remove all timestamps from the content
    cleaned_text = re.sub(timestamp_pattern, '', text)

    # Remove any extra whitespace created by the removal of timestamps
    cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text)

    return cleaned_text

def process_pdf(input_file_path):
    # Extract text from the PDF file
    text = extract_text_from_pdf(input_file_path)
    
    # Remove timestamps from the extracted text
    cleaned_text = remove_timestamps_from_text(text)

    # Prompt the user for the desired output file name
    output_file_name = simpledialog.askstring("Output File Name", "Enter the desired name for the cleaned transcript (without extension):")
    
    if output_file_name:
        # Ensure the output file has a .txt extension
        output_file_name += '.txt'

        # Get the Downloads folder path
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        output_file_path = os.path.join(downloads_folder, output_file_name)

        # Write the cleaned content to the output file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_text)

        # Show a success message
        messagebox.showinfo("Success", f"Timestamps removed. Cleaned transcript saved to {output_file_path}")

def select_file():
    # Open a file dialog to select the input PDF file
    input_file_path = filedialog.askopenfilename(title="Select Transcript PDF", filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*")))
    
    if input_file_path:
        process_pdf(input_file_path)

# Create the GUI window
root = Tk()
root.title("PDF Timestamp Remover")

# Add a label and button to the window
label = Label(root, text="Click the button to select the transcript PDF file:")
label.pack(pady=10)

button = Button(root, text="Select File", command=select_file)
button.pack(pady=10)

# Run the GUI loop
root.mainloop()