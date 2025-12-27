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
import config

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
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


@app.route('/api/limits')
def get_limits():
    """Get current file size limits."""
    return jsonify(config.get_limits_info())


@app.route('/encrypt', methods=['POST'])
def encrypt():
    """Encrypt files into PNG images (supports bulk upload)."""
    print(f"🔵 Received encryption request")
    try:
        if 'files' not in request.files:
            print(f"❌ No files in request")
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        print(f"📦 Received {len(files)} file(s)")
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        # Validate number of files
        if len(files) > config.MAX_FILES_PER_BATCH:
            return jsonify({
                'error': f'Too many files. Maximum {config.MAX_FILES_PER_BATCH} files per batch.'
            }), 400
        
        # Validate total size for bulk uploads
        total_size = sum(file.content_length or 0 for file in files)
        if len(files) > 1 and total_size > config.MAX_BULK_TOTAL_SIZE:
            return jsonify({
                'error': f'Total file size exceeds limit. Maximum {config.format_size(config.MAX_BULK_TOTAL_SIZE)} for bulk upload.'
            }), 400
        
        password = request.form.get('password', '').strip() or None
        use_individual_passwords = request.form.get('use_individual_passwords') == 'true'
        
        results = []
        
        for idx, file in enumerate(files):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{idx}_{filename}")
            file.save(input_path)
            
            # Check input file size
            file_size = os.path.getsize(input_path)
            
            # Determine if chunking is needed
            needs_chunking = config.ENABLE_AUTO_CHUNKING and file_size > config.CHUNK_SIZE
            
            if needs_chunking:
                # Calculate number of chunks
                num_chunks = (file_size + config.CHUNK_SIZE - 1) // config.CHUNK_SIZE
                if num_chunks > config.MAX_CHUNKS:
                    os.remove(input_path)
                    return jsonify({
                        'error': f'File "{filename}" is too large. Would require {num_chunks} chunks (max {config.MAX_CHUNKS}). Increase MAX_CHUNKS in config.py.'
                    }), 400
            
            # Get individual password if applicable
            file_password = None
            if use_individual_passwords:
                file_password = request.form.get(f'password_{idx}', '').strip() or None
            elif password:
                file_password = password
            
            # Handle chunked encryption for large files
            if needs_chunking:
                # Split file into chunks
                chunks = ColorCrypt.split_file_into_chunks(input_path, config.CHUNK_SIZE)
                chunk_results = []
                
                for chunk in chunks:
                    chunk_filename = f"{Path(filename).stem}_chunk{chunk['number']:04d}_encrypted.png"
                    chunk_output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{idx}_{chunk_filename}")
                    
                    # Encrypt chunk
                    ColorCrypt.encrypt_file_to_image(chunk['path'], chunk_output_path, file_password)
                    
                    chunk_size = os.path.getsize(chunk_output_path)
                    chunk_results.append({
                        'filename': chunk_filename,
                        'size': chunk_size,
                        'download_url': f'/download/{Path(chunk_output_path).name}',
                        'chunk_number': chunk['number']
                    })
                    
                    # Clean up chunk temp file
                    os.remove(chunk['path'])
                
                # Clean up input file
                os.remove(input_path)
                
                # Return chunked result
                results.append({
                    'original_name': filename,
                    'is_chunked': True,
                    'total_chunks': len(chunks),
                    'original_size': file_size,
                    'chunks': chunk_results,
                    'protected': file_password is not None
                })
                continue
            
            # Regular encryption for small files
            # Generate output filename
            output_filename = f"{Path(filename).stem}_encrypted.png"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{idx}_{output_filename}")
            
            # Encrypt
            ColorCrypt.encrypt_file_to_image(input_path, output_path, file_password)
            
            # Get file size
            output_file_size = os.path.getsize(output_path)
            
            # Clean up input file
            os.remove(input_path)
            
            results.append({
                'original_name': filename,
                'filename': output_filename,
                'size': output_file_size,
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
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ Encryption error: {str(e)}")
        print(error_details)
        return jsonify({'error': str(e)}), 500


def decrypt_chunks(files, password):
    """Decrypt multiple chunk files and reassemble."""
    try:
        # Validate all files are PNGs
        for file in files:
            if not allowed_file(file.filename, {'png'}):
                return jsonify({'error': f'File {file.filename} is not a PNG'}), 400
        
        decrypted_chunks = []
        
        # Decrypt each chunk
        for idx, file in enumerate(files):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"chunk_{idx}_{filename}")
            file.save(input_path)
            
            try:
                output_path = ColorCrypt.decrypt_image_to_file(input_path, app.config['OUTPUT_FOLDER'], password)
                decrypted_chunks.append(output_path)
                os.remove(input_path)
            except ValueError as e:
                # Clean up
                os.remove(input_path)
                for chunk in decrypted_chunks:
                    if os.path.exists(chunk):
                        os.remove(chunk)
                
                error_msg = str(e)
                if "password protected" in error_msg.lower():
                    return jsonify({'error': error_msg, 'requires_password': True}), 400
                return jsonify({'error': error_msg}), 400
        
        # Reassemble chunks
        # Extract original filename from first chunk (remove _chunk0000 suffix)
        first_chunk_name = Path(decrypted_chunks[0]).name
        original_name = first_chunk_name.replace('_chunk0000', '').replace('_chunk000', '').replace('_chunk00', '').replace('_chunk0', '')
        if '_chunk' in original_name:
            original_name = original_name.split('_chunk')[0] + Path(first_chunk_name).suffix
        
        reassembled_path = os.path.join(app.config['OUTPUT_FOLDER'], f"reassembled_{original_name}")
        ColorCrypt.reassemble_chunks(decrypted_chunks, reassembled_path)
        
        # Clean up chunk files
        for chunk in decrypted_chunks:
            if os.path.exists(chunk):
                os.remove(chunk)
        
        file_size = os.path.getsize(reassembled_path)
        output_filename = Path(reassembled_path).name
        
        return jsonify({
            'success': True,
            'filename': output_filename,
            'size': file_size,
            'download_url': f'/download/{output_filename}',
            'was_chunked': True,
            'chunks_count': len(files)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/decrypt', methods=['POST'])
def decrypt():
    """Decrypt a PNG image (or multiple chunks) back to the original file."""
    try:
        # Check if this is multi-chunk decryption
        files = request.files.getlist('files') if 'files' in request.files else []
        single_file = request.files.get('file')
        
        if not files and not single_file:
            return jsonify({'error': 'No file provided'}), 400
        
        # Handle multi-chunk decryption
        if files and len(files) > 1:
            return decrypt_chunks(files, request.form.get('password', '').strip() or None)
        
        # Handle single file decryption
        file = files[0] if files else single_file
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
    return jsonify({'error': f'File too large. Maximum upload size is {config.format_size(config.MAX_CONTENT_LENGTH)}'}), 413


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
