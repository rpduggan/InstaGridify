# InstaGridify
Effortlessly split images into Instagram-friendly grids without distorting the main subject. InstaGridify is a powerful Python script that allows you to seamlessly split images into grids suitable for Instagram, ensuring that the main subjects in the images are not distorted. Perfect for creating stunning and eye-catching Instagram posts and stories. It can be used for platforms other than Instagram but proportions may not be correct.

## Features
- Split images into customizable grid sizes (e.g., 3x3, 2x2, etc.).
- Preserve the integrity of the main subject in the image.
- Easy-to-use command-line interface.
- Flexible grid size recommendations based on image dimensions.
- Option for custom grid sizes.
- Error handling for various edge cases (e.g., non-existing images, non-image files, etc.).

## Installation
To use InstaGridify, you need Python installed on your system. Clone or download this repository to your local machine and have any packages installed on python.

```bash
git clone https://github.com/rpduggan/InstaGridify.git
cd InstaGridify
python -m pip install -r requirements.txt
```

## Usage
Navigate to the directory containing `insta_gridify.py` and run the script with the following command:

```bash
python insta_gridify.py <image_path> [optional: columns rows]
```

- `<image_path>`: Path to the image you want to split.
- `optional: columns rows`: Optional grid size. If not provided, the script will recommend grid sizes.

for example:

```bash
python insta_gridify.py image.png 3 3
```

If you leave off the optional column and row numbers, it will estimate the best grids for you and give you some options to choose from.

## Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.
