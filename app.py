import os
import io
import secrets
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from flask_socketio import SocketIO, emit
from PIL import Image
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
socketio = SocketIO(app, async_mode='eventlet')

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DELIMITER = b"###NAVEENCRYPT###"

def message_to_bits(message_bytes):
    return ''.join(format(b, '08b') for b in message_bytes)

def bits_to_bytes(bits):
    bytes_ = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        bytes_.append(int(byte, 2))
    return bytes(bytes_)

def aes_encrypt(key: bytes, data: bytes):
    aesgcm = AESGCM(key.ljust(32, b'\0')[:32])
    nonce = secrets.token_bytes(12)
    ct = aesgcm.encrypt(nonce, data, None)
    return nonce + ct

def aes_decrypt(key: bytes, data: bytes):
    aesgcm = AESGCM(key.ljust(32, b'\0')[:32])
    nonce = data[:12]
    ct = data[12:]
    return aesgcm.decrypt(nonce, ct, None)

def embed_message_in_image(image: Image.Image, message_bytes: bytes):
    message_bytes += DELIMITER
    bits = message_to_bits(message_bytes)
    pixels = list(image.getdata())
    max_bits = len(pixels) * 4
    if len(bits) > max_bits:
        return None
    new_pixels = []
    bit_idx = 0
    for pixel in pixels:
        r, g, b, a = pixel
        new_pixel = []
        for color in (r, g, b, a):
            if bit_idx < len(bits):
                new_color = (color & 0xFE) | int(bits[bit_idx])
                bit_idx += 1
            else:
                new_color = color
            new_pixel.append(new_color)
        new_pixels.append(tuple(new_pixel))
    new_img = Image.new(image.mode, image.size)
    new_img.putdata(new_pixels)
    return new_img

def extract_message_from_image(image: Image.Image):
    pixels = list(image.getdata())
    bits = ""
    for pixel in pixels:
        for color in pixel[:4]:
            bits += str(color & 1)
    delimiter_bits = message_to_bits(DELIMITER)
    idx = bits.find(delimiter_bits)
    if idx == -1:
        return None
    message_bits = bits[:idx]
    return bits_to_bytes(message_bits)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/embed', methods=['GET', 'POST'])
def embed():
    if request.method == 'POST':
        imgfile = request.files.get('image')
        message = request.form.get('message_text', '')
        password = request.form.get('password', '')
        if not imgfile or imgfile.filename == '':
            flash("Please select an image file.", 'error')
            return redirect(url_for('embed'))
        if not (imgfile.filename.lower().endswith('.png') or imgfile.filename.lower().endswith('.bmp')):
            flash("Please upload a PNG or BMP image.", 'error')
            return redirect(url_for('embed'))
        if not message.strip():
            flash("Please enter a message to embed.", 'error')
            return redirect(url_for('embed'))
        try:
            image = Image.open(imgfile.stream).convert("RGBA")
            message_bytes = message.encode('utf-8')
            if password:
                message_bytes = aes_encrypt(password.encode('utf-8'), message_bytes)
            encoded_img = embed_message_in_image(image, message_bytes)
            if encoded_img is None:
                flash("Message too large to embed in the image.", 'error')
                return redirect(url_for('embed'))
            img_io = io.BytesIO()
            encoded_img.save(img_io, 'PNG')
            img_io.seek(0)
            return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='encoded_image.png')
        except Exception as e:
            flash(f"Error: {str(e)}", 'error')
            return redirect(url_for('embed'))
    return render_template('embed.html')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    extracted_message = None
    if request.method == 'POST':
        imgfile = request.files.get('image')
        password = request.form.get('password', '')
        if not imgfile or imgfile.filename == '':
            flash("Please select an image file.", 'error')
            return redirect(url_for('extract'))
        if not (imgfile.filename.lower().endswith('.png') or imgfile.filename.lower().endswith('.bmp')):
            flash("Please upload a PNG or BMP image.", 'error')
            return redirect(url_for('extract'))
        try:
            image = Image.open(imgfile.stream).convert("RGBA")
            message_bytes = extract_message_from_image(image)
            if message_bytes is None:
                flash("No hidden message found in the image.", 'error')
                return redirect(url_for('extract'))
            if password:
                try:
                    message_bytes = aes_decrypt(password.encode('utf-8'), message_bytes)
                except Exception:
                    flash("Decryption failed. Invalid password or corrupted data.", 'error')
                    return redirect(url_for('extract'))
            try:
                extracted_message = message_bytes.decode('utf-8')
            except:
                extracted_message = f"<Binary data of {len(message_bytes)} bytes extracted>"
        except Exception as e:
            flash(f"Error: {str(e)}", 'error')
            return redirect(url_for('extract'))
    return render_template('extract.html', extracted_message=extracted_message)

@app.route('/password')
def password():
    return render_template('password.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
