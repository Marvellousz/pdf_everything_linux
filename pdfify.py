#!/usr/bin/env python3
"""
PDF-Everything for Linux - Lightweight Implementation
Convert various file formats to PDF without heavy dependencies
"""

import os
import sys
import subprocess
from fpdf import FPDF
from PIL import Image

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        # Check for abiword
        subprocess.run(['which', 'abiword'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("AbiWord is installed.")
    except subprocess.CalledProcessError:
        print("WARNING: AbiWord is not installed. DOCX conversion will not work.")
        print("Install with: sudo apt-get install abiword")

def convert_txt_to_pdf(input_file, output_file):
    """Convert text files to PDF using FPDF"""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Read the text file with proper encoding handling
        with open(input_file, 'r', encoding='utf-8', errors='replace') as file:
            for line in file:
                # Clean the line to avoid FPDF encoding issues
                clean_line = ''.join(char for char in line if ord(char) < 128)
                pdf.cell(0, 10, txt=clean_line.strip(), ln=True)

        pdf.output(output_file)
        return True
    except Exception as e:
        print(f"Error converting text file: {e}")
        return False

def convert_image_to_pdf(input_file, output_file):
    """Convert image files to PDF using PIL and FPDF"""
    try:
        # Open the image and get dimensions
        image = Image.open(input_file)
        width, height = image.size

        # Convert to RGB if needed (for transparency handling)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Save as temporary JPEG for FPDF compatibility
        temp_jpg = input_file + ".temp.jpg"
        image.save(temp_jpg, "JPEG")

        # Create PDF with image dimensions
        pdf = FPDF(unit="pt", format=[width, height])
        pdf.add_page()
        pdf.image(temp_jpg, 0, 0, width, height)
        pdf.output(output_file)

        # Clean up temporary file
        os.remove(temp_jpg)
        return True
    except Exception as e:
        print(f"Error converting image: {e}")
        return False

def convert_docx_to_pdf(input_file, output_file):
    """Convert DOCX to PDF using AbiWord (lightweight alternative)"""
    try:
        # Get the directory of the output file
        output_dir = os.path.dirname(output_file)
        if not output_dir:
            output_dir = "."

        # AbiWord will create the PDF with the same base name in the current directory
        # So we need to run it from the output directory
        current_dir = os.getcwd()
        os.chdir(output_dir)

        # Run AbiWord for conversion
        result = subprocess.run(
            ['abiword', '--to=pdf', input_file],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Get back to the original directory
        os.chdir(current_dir)

        # AbiWord creates the PDF with the same name but .pdf extension
        # Check if the file exists and matches our expected output path
        base_name = os.path.basename(input_file)
        name_without_ext = os.path.splitext(base_name)[0]
        expected_pdf = os.path.join(output_dir, name_without_ext + '.pdf')

        if os.path.exists(expected_pdf) and expected_pdf != output_file:
            os.rename(expected_pdf, output_file)

        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running AbiWord: {e}")
        print(f"STDERR: {e.stderr.decode('utf-8', errors='replace')}")
        return False
    except Exception as e:
        print(f"Error converting DOCX: {e}")
        return False

def convert_to_pdf(input_file, output_dir):
    """Convert a file to PDF based on its extension"""
    # Get file details
    file_name = os.path.basename(input_file)
    name_without_ext = os.path.splitext(file_name)[0]
    extension = os.path.splitext(file_name)[1].lower()

    # Create output file path
    output_file = os.path.join(output_dir, name_without_ext + '.pdf')

    print(f"Converting {file_name} to {output_file}...")

    # Convert based on file type
    if extension in ['.txt', '.md', '.csv']:
        success = convert_txt_to_pdf(input_file, output_file)
    elif extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
        success = convert_image_to_pdf(input_file, output_file)
    elif extension in ['.docx', '.doc']:
        success = convert_docx_to_pdf(input_file, output_file)
    else:
        print(f"Unsupported file format: {extension}")
        return None

    if success:
        return output_file
    else:
        return None

def main():
    """Main function to process files"""
    # Check if dependencies are installed
    check_dependencies()

    # Get current directory
    current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, "pdf_output")

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Define supported file extensions
    supported_extensions = [
        '.txt', '.md', '.csv',  # Text files
        '.jpg', '.jpeg', '.png', '.bmp', '.gif',  # Image files
        '.docx', '.doc'  # Document files
    ]

    # Track conversion results
    converted_files = []
    failed_files = []

    # Process all files in the current directory
    for file_name in os.listdir(current_dir):
        file_path = os.path.join(current_dir, file_name)

        # Skip directories and the script itself
        if os.path.isdir(file_path) or file_name == os.path.basename(__file__):
            continue

        # Check if the file extension is supported
        extension = os.path.splitext(file_name)[1].lower()
        if extension in supported_extensions:
            output_file = convert_to_pdf(file_path, output_dir)
            if output_file and os.path.exists(output_file):
                converted_files.append(file_name)
                print(f"✓ Successfully converted: {file_name}")
            else:
                failed_files.append(file_name)
                print(f"✗ Failed to convert: {file_name}")

    # Print summary
    print("\n=== Conversion Summary ===")
    print(f"Total files processed: {len(converted_files) + len(failed_files)}")
    print(f"Successfully converted: {len(converted_files)}")
    print(f"Failed conversions: {len(failed_files)}")

    if converted_files:
        print("\nConverted files can be found in the 'pdf_output' directory")

if __name__ == "__main__":
    main()
