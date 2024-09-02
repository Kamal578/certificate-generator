# Certificate Generation Project

## Overview

This project automates the process of generating certificates for participants based on their names listed in an Excel file. It uses a certificate template image, inserts participant names with a specified font, and saves the certificates as PDF files. Additionally, it merges all individual certificates into a single PDF document. The script is designed with multithreading to enhance performance and includes robust error handling.

## Features

- **Automatic Certificate Generation**: Reads participant names from an Excel file and generates certificates using a predefined template and font.
- **Multithreading Support**: Utilizes multiple threads to speed up certificate generation.
- **Error Handling**: Logs errors to a file and retries certificate generation up to a specified number of times.
- **PDF Merging**: Combines all generated certificates into a single PDF file.
- **Customizable Settings**: Easily configure paths, font size, text positioning, and more.

## Requirements

- **Python 3.12.4 64-bit** (this specific version was used for development)
- **Docker** and **Docker Compose** (optional, if you prefer using Docker)
- **Python Packages**:
  - The project was developed using the following versions of Python packages, but these specific versions are not strictly required:
    - pandas==2.2.2
    - tqdm==4.66.5
    - pdfmerge==1.0.0
    - openpyxl==3.1.5
    - numpy==2.0.1
    - pillow==10.4.0

## Installation

### Local Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Kamal578/certificate-generator.git
   cd certificate-generator
   ```

2. **Install Python dependencies**:

   Ensure you have Python 3.12.4 installed (or a compatible version). Then, use `pip` to install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare the required files**:
   - Excel file containing participant names (e.g., `fake_names.xlsx`).
   - Certificate template image (e.g., `template.png`).
   - TrueType font file (e.g., `noto.ttf`).

### Docker Setup

To run the project using Docker, you can either build and run the Docker container manually or use Docker Compose for simplified management.

#### 1. Build and Run the Docker Container

First, ensure Docker is installed and running on your machine.

1. **Build the Docker image**:

   ```bash
   docker build -t certificate-generator .
   ```

2. **Run the Docker container**:

   ```bash
   docker run --rm -v $(pwd):/app certificate-generator
   ```

   - `--rm`: Automatically removes the container when it exits.
   - `-v $(pwd):/app`: Mounts the current directory to the `/app` directory in the container, allowing access to local files.

#### 2. Using Docker Compose

1. **Run the service**:

   ```bash
   docker-compose up --build
   ```

   This command builds the Docker image and runs the container as defined in the `docker-compose.yml` file.

2. **Stop the service**:

   Press `Ctrl+C` to stop the running service, or run:

   ```bash
   docker-compose down
   ```

## Configuration

Modify the `settings` dictionary in your Python script to customize the certificate generation process:

```python
settings = {
    'excel': './fake_names.xlsx',      # Path to the Excel file containing names
    'template': './template.png',      # Path to the certificate template image
    'font': 'noto.ttf',                # Path to the font file to be used for text
    'output_dir': './certificates/',   # Directory to save generated certificates
    'error_log_file': './errors.log',  # File to log errors during certificate generation
    'font_size': 80,                   # Font size for the text on the certificate
    'max_retries': 3,                  # Maximum number of retries for generating a certificate
    'text_box_width': 500,             # Width of the text box for name placement
    'text_box_height': 100,            # Height of the text box for name placement
    'offset_x': 180,                   # Horizontal offset for text placement
    'offset_y': 100,                   # Vertical offset for text placement
    'keep_singles': False              # Whether to keep individual certificate files after merging into a PDF
}
```

## Usage

### Local Execution

Run the Python script directly:

```bash
python generate_certificates.py
```

### Docker Execution

To run the script using Docker:

```bash
docker run --rm -v $(pwd):/app certificate-generator
```

Or, using Docker Compose:

```bash
docker-compose up --build
```

## Functions

### 1. `clean_name(name: str) -> str`

Cleans and formats the participant's name for display on the certificate.

- **Parameters**: 
  - `name` (str): The original name from the Excel file.
- **Returns**: 
  - `str`: The cleaned and formatted name.

### 2. `log_error(message: str) -> None`

Logs error messages to a log file.

- **Parameters**: 
  - `message` (str): The error message to log.

### 3. `load_template_image() -> Image.Image`

Loads the certificate template image from the specified path.

- **Returns**: 
  - `Image.Image`: The loaded template image object.
- **Raises**: 
  - Exception if the template image fails to load.

### 4. `verify_image(image_path: str) -> bool`

Verifies that the image at the given path is a valid image.

- **Parameters**: 
  - `image_path` (str): The file path to the image to verify.
- **Returns**: 
  - `bool`: True if the image is valid, False otherwise.

### 5. `generate_certificate(name: str) -> None`

Generates a certificate for a given name and saves it as a PNG and PDF file.

- **Parameters**: 
  - `name` (str): The participant's name to be added to the certificate.

### 6. `main() -> None`

Orchestrates the certificate generation process.

## Error Handling

Errors encountered during the process are logged into a specified log file (`errors.log`). The script attempts to generate certificates up to a maximum number of retries defined in the settings (`max_retries`).

## Performance Optimization

The script uses multithreading via the `ThreadPoolExecutor` to significantly reduce the time taken to generate certificates, particularly for large datasets.

## Output

- **Generated Certificates**: Saved as individual PDF files in the specified output directory (`certificates/`).
- **Merged PDF**: A single PDF file (`all_certificates.pdf`) containing all certificates.
- **Error Log**: An error log file (`errors.log`) that records any issues encountered during the process.

## Cleanup

The script can clean up by removing individual certificate files and the output directory if it becomes empty after merging the certificates into a single PDF. The error log is also removed if no errors occurred.