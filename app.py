"""
ColorCrypt Web Application
Flask-based web interface for file steganography
"""
from flask import Flask, render_template, request, send_file, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import tempfile
import shutil
from colorcrypt import ColorCrypt

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
app.config['OUTPUT_FOLDER'] = tempfile.mkdtemp()

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


def allowed_file(filename, allowed_extensions):
    """Check if file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    """Encrypt files into PNG images (supports bulk upload)."""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        password = request.form.get('password', '').strip() or None
        use_individual_passwords = request.form.get('use_individual_passwords') == 'true'
        
        results = []
        
        for idx, file in enumerate(files):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{idx}_{filename}")
            file.save(input_path)
            
            # Get individual password if applicable
            file_password = None
            if use_individual_passwords:
                file_password = request.form.get(f'password_{idx}', '').strip() or None
            elif password:
                file_password = password
            
            # Generate output filename
            output_filename = f"{Path(filename).stem}_encrypted.png"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{idx}_{output_filename}")
            
            # Encrypt
            ColorCrypt.encrypt_file_to_image(input_path, output_path, file_password)
            
            # Get file size
            file_size = os.path.getsize(output_path)
            
            # Clean up input file
            os.remove(input_path)
            
            results.append({
                'original_name': filename,
                'filename': output_filename,
                'size': file_size,
                'download_url': f'/download/{Path(output_path).name}',
                'protected': file_password is not None
            })
        
        if len(results) == 1:
            return jsonify({
                'success': True,
                **results[0]
            })
        else:
            return jsonify({
                'success': True,
                'bulk': True,
                'files': results,
                'count': len(results)
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/decrypt', methods=['POST'])
def decrypt():
    """Decrypt a PNG image back to the original file."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate it's a PNG
        if not allowed_file(file.filename, {'png'}):
            return jsonify({'error': 'Please upload a PNG image'}), 400
        
        password = request.form.get('password', '').strip() or None
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Decrypt
        try:
            output_path = ColorCrypt.decrypt_image_to_file(input_path, app.config['OUTPUT_FOLDER'], password)
        except ValueError as e:
            # Clean up input file
            os.remove(input_path)
            error_msg = str(e)
            if "password protected" in error_msg.lower():
                return jsonify({'error': error_msg, 'requires_password': True}), 400
            return jsonify({'error': error_msg}), 400
        
        # Get file info
        output_filename = Path(output_path).name
        file_size = os.path.getsize(output_path)
        
        # Clean up input file
        os.remove(input_path)
        
        return jsonify({
            'success': True,
            'filename': output_filename,
            'size': file_size,
            'download_url': f'/download/{output_filename}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download(filename):
    """Download an encrypted or decrypted file."""
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        response = send_file(file_path, as_attachment=True, download_name=filename)
        
        # Clean up file after sending
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except:
                pass
        
        return response
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/static/<path:path>')
def send_static(path):
    """Serve static files."""
    return send_from_directory('static', path)


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error."""
    return jsonify({'error': 'File too large. Maximum size is 100MB'}), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


def cleanup_old_files():
    """Clean up temporary files on startup."""
    for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                try:
                    os.remove(os.path.join(folder, file))
                except:
                    pass


if __name__ == '__main__':
    cleanup_old_files()
    print("🌈 ColorCrypt Web Server Starting...")
    print("📍 Open your browser to: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
