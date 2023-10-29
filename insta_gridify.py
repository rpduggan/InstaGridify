import sys
from PIL import Image
import os
import math

def recommend_grid_sizes(width, height, max_columns=3):
    aspect_ratio = width / height
    recommended_sizes = []

    # Check if the image is nearly square
    if 0.9 <= aspect_ratio <= 1.1:
        recommended_sizes.extend([(2, 2), (3, 3)])

    # Calculate grid sizes based on aspect ratio
    for columns in range(1, max_columns + 1):
        rows = max(1, round(height / width * columns))
        recommended_sizes.append((columns, rows))

    # Remove duplicate sizes and 1x1 (if there are alternatives)
    unique_sizes = list(set(recommended_sizes))
    if len(unique_sizes) > 1 and (1, 1) in unique_sizes:
        unique_sizes.remove((1, 1))

    return unique_sizes

def split_image_for_instagram(image_path, grid_size=(3, 3)):
    # Load the image
    img = Image.open(image_path)

    # Extract the base name of the image file without extension
    image_name = os.path.splitext(os.path.basename(image_path))[0]

    # Find the center of the image
    center_x, center_y = img.width // 2, img.height // 2

    # Determine the size of the square to crop
    side_length = min(img.width, img.height)

    # Crop the square from the center
    left = center_x - side_length // 2
    upper = center_y - side_length // 2
    right = center_x + side_length // 2
    lower = center_y + side_length // 2
    cropped_img = img.crop((left, upper, right, lower))

    # Resize the cropped image to be divisible by the grid size
    new_size = side_length + (grid_size[0] - side_length % grid_size[0])
    resized_img = cropped_img.resize((new_size, new_size))

    # Split the image into a grid
    grid_width, grid_height = new_size // grid_size[0], new_size // grid_size[1]
    output_folder = os.path.dirname(image_path) or '.'
    for i in reversed(range(grid_size[1])):
        for j in reversed(range(grid_size[0])):
            box = (j * grid_width, i * grid_height, (j + 1) * grid_width, (i + 1) * grid_height)
            grid_img = resized_img.crop(box)
            grid_img.save(f"{output_folder}/{image_name}_{grid_size[1]-1-i}_{grid_size[0]-1-j}.jpg")

def parse_arguments(args):
    if len(args) < 2 or len(args) > 4:
        print("Usage: python script.py image.jpg [columns rows]")
        print("       Leave [columns rows] blank to see suggested grid options.")

        sys.exit(1)
    return args[1], args[2:]

def check_image_exists(image_path):
    if not os.path.exists(image_path):
        print(f"Error: The file '{image_path}' does not exist.")
        sys.exit(1)

def load_image(image_path):
    try:
        img = Image.open(image_path)
    except IOError:
        print(f"Error: The file '{image_path}' is not a valid image or the format is not supported.")
        sys.exit(1)
    return img

def get_user_grid_choice(recommended_sizes):
    while True:
        print("\nRecommended grid sizes:")
        for i, size in enumerate(recommended_sizes, start=1):
            print(f"{i}. {size[0]} columns x {size[1]} rows")

        print("\nOptions:")
        print(f"1 to {len(recommended_sizes)}. Select one of the recommended grid sizes.")
        print(f"{len(recommended_sizes) + 1}. Input your own grid size.")
        print(f"{len(recommended_sizes) + 2}. Cancel the operation.")
        choice = input("Please enter your choice: ").strip()

        if not choice:
            print("No input provided. Please make a selection.")
        elif choice.isdigit() and 1 <= int(choice) <= len(recommended_sizes):
            return recommended_sizes[int(choice) - 1]
        elif choice == str(len(recommended_sizes) + 1):
            custom_columns_input = input("Enter the number of columns: ").strip()
            custom_rows_input = input("Enter the number of rows: ").strip()
            if not custom_columns_input or not custom_rows_input:
                print("\nNo input provided. Please enter valid numbers for columns and rows.")
                continue
            try:
                custom_columns = int(custom_columns_input)
                custom_rows = int(custom_rows_input)
                if custom_columns < 1 or custom_rows < 1:
                    raise ValueError("\nColumns and rows must be positive integers.")
                return (custom_columns, custom_rows)
            except ValueError as e:
                print(f"\nInvalid input: {e}. Please enter valid numbers for columns and rows.")
        elif choice == str(len(recommended_sizes) + 2):
            print("Operation cancelled.")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please make a valid selection.")



if __name__ == "__main__":
    image_path, args = parse_arguments(sys.argv)
    check_image_exists(image_path)
    img = load_image(image_path)

    width, height = img.size
    if width * height > 6000 * 6000:
        print("Warning: The image is extremely large and processing may take a significant amount of time.")

    if len(args) == 2:
        try:
            columns = int(args[0])
            rows = int(args[1])
        except ValueError:
            print("Error: Invalid grid size. Columns and rows must be integers.")
            sys.exit(1)

        if columns < 1 or rows < 1:
            print("Error: Invalid grid size. Columns and rows must be positive integers.")
            sys.exit(1)

        grid_size = (columns, rows)
    else:
        recommended_sizes = recommend_grid_sizes(width, height)
        grid_size = get_user_grid_choice(recommended_sizes)

    try:
        split_image_for_instagram(image_path, grid_size)
        print(f"Finished gridifying {image_path}")
    except PermissionError:
        print(f"Error: Permission denied when trying to save images in the directory '{os.path.dirname(image_path) or '.'}'.")
        sys.exit(1)

