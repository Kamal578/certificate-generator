import os
import time
import warnings
import traceback
import pandas as pd
import multiprocessing
from tqdm import tqdm
from pdfmerge import pdfmerge
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont, ImageFile, UnidentifiedImageError

from settings import settings

# Suppress specific warnings related to the "openpyxl" module
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Get the number of CPU cores available for multithreading
max_threads = multiprocessing.cpu_count()

# Load the data from the Excel file into a DataFrame
df = pd.read_excel(settings['excel'])

def clean_name(name: str) -> str:
    """
    Clean and format the participant's name for display on the certificate.

    Args:
        name (str): The original name from the Excel file.

    Returns:
        str: The cleaned and formatted name.
    """
    if isinstance(name, str):
        name = name.replace('Host ', '').strip()  # Remove 'Host ' prefix and strip whitespace
        if name.startswith('*'):
            name = name[1:]  # Remove leading asterisk if present
        parts = name.split()
        if len(parts) > 2:
            name = ' '.join(parts[:2])  # Use only the first two parts of the name if more than two
        return name.title().rstrip()  # Convert to title case and remove trailing whitespace
    return name

def log_error(message: str) -> None:
    """
    Log error messages to a log file.

    Args:
        message (str): The error message to log.
    """
    with open(settings['error_log_file'], "a") as log_file:
        log_file.write(message + "\n")

def load_template_image() -> Image.Image:
    """
    Load the certificate template image from the specified path.

    Returns:
        Image.Image: The loaded template image object.

    Raises:
        Exception: If the template image fails to load.
    """
    try:
        template = Image.open(settings['template'])
        template.load()  # Ensure image is fully loaded
        return template
    except Exception as e:
        log_error(f"Error loading template image: {e}")
        raise

def verify_image(image_path: str) -> bool:
    """
    Verify that the image at the given path is a valid image.

    Args:
        image_path (str): The file path to the image to verify.

    Returns:
        bool: True if the image is valid, False otherwise.
    """
    try:
        with Image.open(image_path) as img:
            img.verify()  # Check if image is intact and not corrupted
        return True
    except (UnidentifiedImageError, OSError):
        log_error(f"Error verifying image file {image_path}.")
        return False

def generate_certificate(name: str) -> None:
    """
    Generate a certificate for a given name and save it as a PNG and PDF file.

    Args:
        name (str): The participant's name to be added to the certificate.
    """
    attempts = 0
    while attempts < settings['max_retries']:
        try:
            # Load a fresh copy of the template image
            certificate_template = load_template_image()
            certificate = certificate_template.copy()
            draw = ImageDraw.Draw(certificate)

            # Calculate the position to center the text within the specified text box
            bbox = font.getbbox(name)  # Get the bounding box of the text
            text_x = text_box_x + (settings['text_box_width'] - bbox[2] - bbox[0]) // 2
            text_y = text_box_y + (settings['text_box_height'] - bbox[3] - bbox[1]) // 2
            draw.text((text_x, text_y), name, font=font, fill='black')

            # Save the certificate as a PNG file
            output_path_png = os.path.join(settings['output_dir'], f"{name.replace(' ', '_')}_certificate.png")
            certificate.save(output_path_png)

            # Verify the generated PNG image
            if not verify_image(output_path_png):
                attempts += 1
                continue

            # Convert the PNG to PDF
            output_path_pdf = os.path.join(settings['output_dir'], f"{name.replace(' ', '_')}_certificate.pdf")
            Image.open(output_path_png).convert('RGB').save(output_path_pdf, 'PDF')
            os.remove(output_path_png)  # Remove the PNG after conversion
            break

        except Exception as e:
            log_error(f"Error processing {name}: {e} (Attempt {attempts + 1})")
            log_error(traceback.format_exc())
            attempts += 1

    if attempts == settings['max_retries']:
        log_error(f"Failed to generate certificate for {name} after {settings['max_retries']} attempts.")

def main() -> None:
    """
    Main function to orchestrate the certificate generation process.
    """
    # Prepare output directory and error log
    os.makedirs(settings['output_dir'], exist_ok=True)
    ImageFile.LOAD_TRUNCATED_IMAGES = True  # Handle truncated images
    open(settings['error_log_file'], "w").close()  # Clear the error log file

    # Process names and generate certificates using multithreading
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=max_threads) as executor: 
        list(tqdm(executor.map(generate_certificate, names), total=len(names), desc="Generating Certificates"))

    print(f"Time taken to generate certificates: {time.time() - start_time:.2f} seconds")

    # Merge individual PDFs into a single PDF
    pdfs = [os.path.join(settings['output_dir'], f"{name.replace(' ', '_')}_certificate.pdf") for name in names if pd.notna(name)]
    pdfmerge(pdfs, output="all_certificates.pdf")
    print("All certificates have been generated and merged into a single PDF.")

    # Cleanup if individual certificate files are not to be kept
    if not settings['keep_singles']:
        for pdf in pdfs:
            if os.path.exists(pdf):
                os.remove(pdf)

    # Remove output directory if empty
    if not os.listdir(settings['output_dir']):
        os.rmdir(settings['output_dir'])
        print("Output directory removed successfully.")

    # Handle error log cleanup
    if os.stat(settings['error_log_file']).st_size == 0:
        print("No errors occurred during certificate generation!")
        os.remove(settings['error_log_file'])
    else:
        print("Errors occurred during certificate generation. Please check the error log for details.")

if __name__ == "__main__":
    # Prepare the list of cleaned names for certificate generation
    names = df['Ad, soyad'].dropna().apply(clean_name).drop_duplicates().tolist()

    # Load template image and calculate dimensions for text placement
    certificate_template = Image.open(settings['template'])
    image_width, image_height = certificate_template.size
    text_box_x = (image_width // 2) + settings['offset_x']
    text_box_y = (image_height // 2) - settings['offset_y']

    # Load the font to be used for certificate text
    font = ImageFont.truetype(settings['font'], settings['font_size'])

    # Run the main function to start the certificate generation process
    main() 