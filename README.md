# pdf everything for linux

A lightweight command-line tool to convert various file formats to PDF on Linux systems.

## Features

- Convert multiple file formats to PDF with minimal dependencies
- Supports text files (TXT, MD, CSV)
- Supports images (JPG, PNG, BMP, GIF)
- Supports documents (DOCX, DOC) via AbiWord
- Minimal resource usage compared to LibreOffice-based solutions
- Simple command-line interface


## Requirements

- Python 3.6+
- AbiWord (for document conversion)
- Python packages:
    - fpdf
    - Pillow


## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/pdf-everything-linux.git
cd pdf-everything-linux
```


### 2. Install AbiWord

On Arch Linux:

```bash
sudo pacman -S abiword
```

On Debian/Ubuntu:

```bash
sudo apt-get install abiword
```

On Fedora:

```bash
sudo dnf install abiword
```


### 3. Set up Python environment

#### Option A: Using a virtual environment (recommended)

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Linux/macOS
# or
.\venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```


#### Option B: System-wide installation

On Arch Linux:

```bash
yay -S python-fpdf python-pillow
```

On Debian/Ubuntu:

```bash
sudo apt-get install python3-fpdf python3-pil
```


## Usage

1. Place the script in the folder containing your files
2. Run the script:
```bash
# If using virtual environment
source venv/bin/activate
python pdfify.py

# Or directly
./pdfify.py
```

3. Find converted PDFs in the `pdf_output` folder

## Supported File Types

- Text files: `.txt`, `.md`, `.csv`
- Images: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`
- Documents: `.docx`, `.doc`


## How It Works

- Text files are converted using FPDF
- Images are converted using Pillow and FPDF
- Documents are converted using AbiWord's command-line interface


## Advantages Over the Original Windows Version

- No dependency on Microsoft Office or LibreOffice
- Significantly smaller footprint
- Faster conversion for simple documents
- Works on headless servers


## Limitations

- AbiWord may not preserve all formatting from complex DOCX files
- No support for PowerPoint files (PPT/PPTX)
- No support for Excel files (XLS/XLSX)


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
