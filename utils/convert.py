from PIL import Image

def convert_tif_to_png(input_tif_path, output_png_path):
    try:
        # Open the TIFF image
        img = Image.open(input_tif_path)

        # Save the image as PNG
        img.save(output_png_path, format="PNG")

        print(f"Successfully converted '{input_tif_path}' to '{output_png_path}'")
    except FileNotFoundError:
        print(f"Error: Input file '{input_tif_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_file = "CERTIFICATE 1.tif"  # Replace with your TIFF file name
output_file = "CERTIFICATE 1.png" # Replace with your desired PNG file name

convert_tif_to_png(input_file, output_file)