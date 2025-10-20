

# generate_qr.py
import qrcode
import socket
from PIL import Image, ImageDraw, ImageFont
import os

# Use the same port as in server1.py
PORT = 9500
OUTPUT_DIR = "qr_codes"

def get_local_ip():
    """Get local IP address"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            if not ip.startswith('127.'):
                return ip
    except:
        pass
    
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        if not ip.startswith('127.'):
            return ip
    except:
        pass
    
    return '127.0.0.1'

def generate_qr_code(data, filename):
    """Generate a QR code with checkpoint name label"""
    ip = get_local_ip()
    url = f"http://{ip}:{PORT}/scan?qr_code={data}"
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image and convert to RGB
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Create image with text label
    label_height = 50  # Space for text
    img_width = qr_img.width
    img_height = qr_img.height + label_height
    
    # Create blank image with space for text
    combined_img = Image.new('RGB', (img_width, img_height), 'white')
    
    # Add text label
    draw = ImageDraw.Draw(combined_img)
    try:
        # Try different fonts for better compatibility
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.truetype("LiberationSans-Regular.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    text = f"Sunset Mkuu: {data}"
    text_width = draw.textlength(text, font=font)
    text_x = (img_width - text_width) // 2  # Center text
    
    draw.text((text_x, 10), text, font=font, fill="black")
    
    # Paste QR code below text (convert to tuple for position)
    combined_img.paste(qr_img, (0, label_height))
    
    # Save the image
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, filename)
    combined_img.save(output_path)
    
    print(f"Generated QR code for '{data}' saved as {output_path}")

if __name__ == '__main__':
    # Generate test QR codes
    try:
        for i in range(1, 15):
            generate_qr_code(f"Checkpoint_{i}", f"checkpoint_{i}.png")
        generate_qr_code("VISITOR_123", "visitor_123.png")
    except Exception as e:
        print(f"Error generating QR codes: {e}")
        print("Make sure you have all required dependencies installed:")
        print("pip install qrcode pillow")