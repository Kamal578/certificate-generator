from PIL import Image

# What if the background is white-greyish? not pure white
# iterate over pixels and set a threshold for color similarity
def make_transparent_with_threshold(image_path, output_path, background_color=(255, 255, 255), threshold=30):
    """
    Makes the specified background color of an image transparent using a threshold.

    Args:
        image_path (str): Path to the input image (e.g., signature or stamp).
        output_path (str): Path to save the transparent image.
        background_color (tuple): RGB tuple of the color to make transparent (default is white).
        threshold (int): Threshold for color similarity.
    """
    try:
        img = Image.open(image_path).convert("RGBA")
        datas = img.getdata()

        new_data = []
        for item in datas:
            # Calculate the distance from the background color
            distance = sum((item[i] - background_color[i]) ** 2 for i in range(3)) ** 0.5
            if distance < threshold:
                new_data.append((255, 255, 255, 0))  # Fully transparent white
            else:
                new_data.append(item)  # Keep original pixel

        img.putdata(new_data)
        img.save(output_path, "PNG")
        print(f"Transparent image saved to: {output_path}")

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        

# Example usage with threshold:
make_transparent_with_threshold("image.png", "transparent_signature_threshold.png", threshold=60)