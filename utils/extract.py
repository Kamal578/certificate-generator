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
make_transparent_with_threshold("./image.png", "./transparent_signature_threshold.png", threshold=60)

# In the result image, find average color for the non-transparent pixels
# recolor all non-transparent pixels to that average color
def recolor_non_transparent_to_average(image_path, output_path):
    """
    Recolors all non-transparent pixels of an image to their average color.

    Args:
        image_path (str): Path to the input image with transparency.
        output_path (str): Path to save the recolored image.
    """
    try:
        img = Image.open(image_path).convert("RGBA")
        datas = img.getdata()

        r_total, g_total, b_total, count = 0, 0, 0, 0
        for item in datas:
            if item[3] != 0:  # Non-transparent pixel
                r_total += item[0]
                g_total += item[1]
                b_total += item[2]
                count += 1

        if count == 0:
            print("No non-transparent pixels found.")
            return

        avg_color = (r_total // count, g_total // count, b_total // count)

        new_data = []
        for item in datas:
            if item[3] != 0:  # Non-transparent pixel
                new_data.append((avg_color[0], avg_color[1], avg_color[2], item[3]))
            else:
                new_data.append(item)  # Keep transparent pixel

        img.putdata(new_data)
        img.save(output_path, "PNG")
        print(f"Recolored image saved to: {output_path}")

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
# Example usage of recoloring:
recolor_non_transparent_to_average("./transparent_signature_threshold.png", "./recolored_signature.png")

# Make the average color darker, make it more visible on light backgrounds
def darken_image_colors(image_path, output_path, factor=0.7):
    """
    Darkens the colors of an image by a specified factor.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the darkened image.
        factor (float): Factor by which to darken the colors (0 < factor < 1).
    """
    try:
        img = Image.open(image_path).convert("RGBA")
        datas = img.getdata()

        new_data = []
        for item in datas:
            if item[3] != 0:  # Non-transparent pixel
                new_r = int(item[0] * factor)
                new_g = int(item[1] * factor)
                new_b = int(item[2] * factor)
                new_data.append((new_r, new_g, new_b, item[3]))
            else:
                new_data.append(item)  # Keep transparent pixel

        img.putdata(new_data)
        img.save(output_path, "PNG")
        print(f"Darkened image saved to: {output_path}")

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
# Example usage of darkening:
darken_image_colors("./recolored_signature.png", "./darkened_signature.png", factor=0.5)