from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
from qr import generate_qr_with_logo
import qrcode

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qr-generator-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['STATIC_FOLDER'], 'generated'), exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_error_correction(level):
    levels = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H
    }
    return levels.get(level, qrcode.constants.ERROR_CORRECT_H)

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_qr_api():
    """AJAX endpoint for QR generation - no page refresh"""
    try:
        qr_type = request.form.get('qr_type', 'url')
        fill_color = request.form.get('fill_color', '#000000')
        back_color = request.form.get('back_color', '#FFFFFF')
        box_size = int(request.form.get('box_size', 25))
        error_correction = request.form.get('error_correction', 'H')
        logo_file = request.files.get('logo')
        
        # Build data dict based on QR type
        data = {}
        if qr_type == 'url':
            data['url'] = request.form.get('url', '')
            if not data['url']:
                return jsonify({'success': False, 'error': 'Please enter a URL'})
        elif qr_type == 'text':
            data['text'] = request.form.get('text', '')
        elif qr_type == 'email':
            data['email'] = request.form.get('email', '')
            data['subject'] = request.form.get('subject', '')
            data['body'] = request.form.get('body', '')
        elif qr_type == 'phone':
            data['phone'] = request.form.get('phone', '')
        elif qr_type == 'wifi':
            data['ssid'] = request.form.get('ssid', '')
            data['password'] = request.form.get('password', '')
            data['encryption'] = request.form.get('encryption', 'WPA')
        elif qr_type == 'vcard':
            data['name'] = request.form.get('name', '')
            data['phone'] = request.form.get('vcard_phone', '')
            data['email'] = request.form.get('vcard_email', '')
            data['organization'] = request.form.get('organization', '')
            data['title'] = request.form.get('title', '')
        elif qr_type == 'whatsapp':
            data['phone'] = request.form.get('whatsapp_phone', '')
            data['message'] = request.form.get('whatsapp_message', '')
        
        # Save uploaded logo if provided
        logo_path = None
        if logo_file and allowed_file(logo_file.filename):
            filename = secure_filename(logo_file.filename)
            logo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            logo_file.save(logo_path)
        
        # Generate unique filename
        import time
        timestamp = int(time.time())
        output_filename = f'qr_{timestamp}.png'
        output_path = os.path.join(app.config['STATIC_FOLDER'], 'generated', output_filename)
        
        # Generate QR code
        result = generate_qr_with_logo(
            qr_type=qr_type,
            data=data,
            logo_path=logo_path,
            output_filename=output_path,
            version=7,
            box_size=box_size,
            border=4,
            logo_proportion=4,
            border_size=0,
            fill_color=hex_to_rgb(fill_color),
            back_color=hex_to_rgb(back_color),
            error_correction=get_error_correction(error_correction)
        )
        
        return jsonify({
            'success': True,
            'filename': f'generated/{output_filename}',
            'download_url': f'/download/generated/{output_filename}',
            'image_url': f'/static/generated/{output_filename}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/preview', methods=['POST'])
def preview_qr_api():
    """Quick preview endpoint for real-time QR updates"""
    try:
        qr_type = request.form.get('qr_type', 'url')
        fill_color = request.form.get('fill_color', '#000000')
        back_color = request.form.get('back_color', '#FFFFFF')
        box_size = int(request.form.get('box_size', 15))  # Smaller for preview
        
        # Build data dict based on QR type
        data = {}
        if qr_type == 'url':
            data['url'] = request.form.get('url', 'https://example.com')
        elif qr_type == 'text':
            data['text'] = request.form.get('text', 'Sample Text')
        elif qr_type == 'email':
            data['email'] = request.form.get('email', 'test@example.com')
            data['subject'] = request.form.get('subject', '')
            data['body'] = request.form.get('body', '')
        elif qr_type == 'phone':
            data['phone'] = request.form.get('phone', '+1234567890')
        elif qr_type == 'wifi':
            data['ssid'] = request.form.get('ssid', 'MyWiFi')
            data['password'] = request.form.get('password', 'password')
            data['encryption'] = request.form.get('encryption', 'WPA')
        elif qr_type == 'vcard':
            data['name'] = request.form.get('name', 'John Doe')
            data['phone'] = request.form.get('vcard_phone', '+1234567890')
            data['email'] = request.form.get('vcard_email', 'john@example.com')
            data['organization'] = request.form.get('organization', '')
            data['title'] = request.form.get('title', '')
        elif qr_type == 'whatsapp':
            data['phone'] = request.form.get('whatsapp_phone', '+1234567890')
            data['message'] = request.form.get('whatsapp_message', 'Hello')
        
        # Generate unique filename for preview
        import time
        timestamp = int(time.time())
        output_filename = f'preview_qr_{timestamp}.png'
        output_path = os.path.join(app.config['STATIC_FOLDER'], 'generated', output_filename)
        
        # Generate QR code quickly with smaller size for preview
        result = generate_qr_with_logo(
            qr_type=qr_type,
            data=data,
            logo_path=None,  # No logo for preview
            output_filename=output_path,
            version=5,
            box_size=box_size,
            border=2,
            logo_proportion=4,
            border_size=0,
            fill_color=hex_to_rgb(fill_color),
            back_color=hex_to_rgb(back_color),
            error_correction=qrcode.constants.ERROR_CORRECT_M
        )
        
        return jsonify({
            'success': True,
            'image_url': f'/static/generated/{output_filename}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download/<path:filename>')
def download_qr(filename):
    return send_file(os.path.join(app.config['STATIC_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
