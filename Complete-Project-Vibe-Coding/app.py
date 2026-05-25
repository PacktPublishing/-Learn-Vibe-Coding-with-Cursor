import os
from flask import Flask, render_template, request, send_from_directory, url_for, jsonify
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class WatermarkConfig:
    def __init__(self, text="ZenvaResizer", font_size=36, 
                 color=(255, 255, 255), opacity=128, position="center", 
                 rotation=0, padding=20):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.opacity = opacity
        self.position = position
        self.rotation = rotation
        self.padding = padding

def apply_watermark(image, config):
    """Apply watermark to the image"""
    # Create a transparent layer for the watermark
    watermark = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)
    
    # Load default font
    try:
        font = ImageFont.truetype("arial.ttf", config.font_size)
    except:
        font = ImageFont.load_default()
    
    # Calculate text size
    text_bbox = draw.textbbox((0, 0), config.text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Calculate position based on config
    if config.position == "center":
        x = (image.size[0] - text_width) // 2
        y = (image.size[1] - text_height) // 2
    elif config.position == "top-left":
        x = config.padding
        y = config.padding
    elif config.position == "top-right":
        x = image.size[0] - text_width - config.padding
        y = config.padding
    elif config.position == "bottom-left":
        x = config.padding
        y = image.size[1] - text_height - config.padding
    elif config.position == "bottom-right":
        x = image.size[0] - text_width - config.padding
        y = image.size[1] - text_height - config.padding
    
    # Draw text
    draw.text((x, y), config.text, font=font, fill=(*config.color, config.opacity))
    
    # Rotate watermark if needed
    if config.rotation != 0:
        watermark = watermark.rotate(config.rotation, expand=True)
        # Recenter the rotated watermark
        x = (image.size[0] - watermark.size[0]) // 2
        y = (image.size[1] - watermark.size[1]) // 2
        watermark = watermark.crop((0, 0, image.size[0], image.size[1]))
    
    # Convert image to RGBA if it isn't already
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Composite watermark onto image
    return Image.alpha_composite(image, watermark)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'images[]' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('images[]')
    if len(files) > 5:
        return jsonify({'error': 'Maximum 5 files allowed'}), 400

    width = int(request.form.get('width', 800))
    height = int(request.form.get('height', 600))
    quality = int(request.form.get('quality', 85))
    rotation = int(request.form.get('rotation', 0))

    # Get watermark parameters
    watermark_text = request.form.get('watermark_text', 'ZenvaResizer')
    font_size = int(request.form.get('font_size', 36))
    color = tuple(map(int, request.form.get('color', '255,255,255').split(',')))
    opacity = int(request.form.get('opacity', 128))
    position = request.form.get('position', 'center')
    watermark_rotation = int(request.form.get('watermark_rotation', 0))
    padding = int(request.form.get('padding', 20))

    # Create watermark configuration
    watermark_config = WatermarkConfig(
        text=watermark_text,
        font_size=font_size,
        color=color,
        opacity=opacity,
        position=position,
        rotation=watermark_rotation,
        padding=padding
    )

    processed_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_filename = f'resized_{filename}'
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            file.save(input_path)
            
            with Image.open(input_path) as img:
                # Apply rotation if specified
                if rotation != 0:
                    img = img.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)
                # Resize after rotation to maintain aspect ratio
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                
                # Apply watermark
                img = apply_watermark(img, watermark_config)
                
                # Save the processed image
                img.save(output_path, quality=quality)
            
            processed_files.append(output_filename)
            os.remove(input_path)  # Clean up original file

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'files': processed_files})
    return render_template('results.html', files=processed_files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True) 