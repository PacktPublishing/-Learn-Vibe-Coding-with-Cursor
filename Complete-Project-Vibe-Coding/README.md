# ZenvaResizer

A modern, neon-themed web application for batch image processing with a sleek user interface. Built with Flask and Pillow, ZenvaResizer allows you to resize, rotate, and optimize multiple images simultaneously.

## Features

- 🖼️ **Batch Processing**: Upload and process up to 5 images at once
- 📐 **Custom Dimensions**: Set custom width and height for your images
- 🔄 **Rotation**: Rotate images by any angle (0-359 degrees)
- 🎯 **Quality Control**: Adjust output image quality (1-100)
- 🎨 **Modern UI**: Sleek neon-themed interface with smooth animations
- 🚀 **Fast Processing**: Efficient image processing using Pillow
- 📱 **Responsive Design**: Works on both desktop and mobile devices

## Requirements

- Python 3.7+
- Flask
- Pillow (PIL)
- Werkzeug

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/zenvaresizer.git
cd zenvaresizer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Use the web interface to:
   - Select up to 5 images
   - Set desired dimensions
   - Adjust quality settings
   - Apply rotation if needed
   - Process and download the results

## API Endpoints

- `GET /`: Main application interface
- `POST /upload`: Process uploaded images
  - Parameters:
    - `images[]`: Image files (max 5)
    - `width`: Target width in pixels
    - `height`: Target height in pixels
    - `quality`: Output quality (1-100)
    - `rotation`: Rotation angle in degrees (0-359)
- `GET /uploads/<filename>`: Access processed images

## Supported Image Formats

- PNG
- JPEG/JPG

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Pillow](https://python-pillow.org/)
- [Werkzeug](https://werkzeug.palletsprojects.com/)

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/zenvaresizer](https://github.com/yourusername/zenvaresizer) 