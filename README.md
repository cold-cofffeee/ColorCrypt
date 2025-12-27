# 🌈 ColorCrypt

**Turn any file into an image, and back again.**  
A beautiful Python web application for steganography - hide files inside PNG images.

---

## ✨ What is ColorCrypt?

Have you ever wanted to:

- 📧 Send a file by email that the provider does not allow?  
- ☁️ Store restricted file types on cloud services that only accept images?  
- 🕵️ Add an extra layer of privacy when sharing files publicly?  
- ✒ Are you a journalist in a totalitarian state and need to release a file?
- 🔒 Exfiltrate data into systems that monitor suspicious files? 

With ColorCrypt, you can **convert any file into an image** and later **recover the original file**.  
The output looks like a normal PNG, but it actually carries your data inside its pixels.

### 🎨 Beautiful Web Interface

ColorCrypt features a modern, gradient-based web UI with drag-and-drop functionality, making file encryption and decryption as simple as possible!

---

## 🚀 Features

- 🌐 **Beautiful Web Interface**: Modern "Encrypted Spectrum" theme with drag-and-drop functionality
- 🔄 **Two-way conversion**:  
  - **Encrypt**: Transform any file into a PNG image  
  - **Decrypt**: Restore the original file from the PNG  

- 🔐 **Password Protection**: Optional AES-256-CBC encryption with PBKDF2 key derivation
  - Auto-detection of password-protected files
  - Strong cryptographic security (100,000 PBKDF2 iterations)
  - Individual or shared passwords for bulk operations

- 📦 **Bulk Upload Support**: 
  - Encrypt multiple files at once
  - Set individual passwords or use one for all
  - Batch download with individual buttons

- � **Automatic File Chunking**: Handle files of ANY size!
  - Files larger than 500MB automatically split into chunks
  - No file size limits (default max: 500GB, configurable to unlimited!)
  - Seamless reassembly during decryption
  - Progress tracking with timer and ETA

- ⏱️ **Real-Time Progress Tracking**:
  - Live progress bar with percentage
  - Elapsed time and estimated time remaining (ETA)
  - Detailed status messages (e.g., "Splitting file into chunks", "Encrypting chunk 5 of 10")
  - Automatic speed-based estimation

- �🎨 **Dark/Light Theme Toggle**: 
  - Beautiful dark theme ("Encrypted Spectrum" - default)
  - Clean light theme for better readability
  - Theme preference saved automatically

- 📝 **Embedded metadata**:  
  - Signature validation ("ER" for plain, "EC" for encrypted)
  - Original file size and filename
  - SHA1 hash for integrity verification
  - Salt and IV for encrypted files

- 🖼️ **Cross-platform**: Built with Python and Pillow. Works on Windows, Linux, macOS  
- ✅ **Integrity check**: SHA1 verification ensures files aren't corrupted or tampered with
- 📱 **Responsive design**: Works beautifully on desktop and mobile devices  

---

## 📦 Installation & Usage

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ColorCrypt.git
cd ColorCrypt
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Web Application

```bash
python app.py
```

Then open your browser to: **http://127.0.0.1:5000**

🎉 That's it! Use the beautiful web interface to encrypt and decrypt files.

---

## 🎯 Automatic File Chunking

ColorCrypt automatically handles files of **any size**! Large files are split into manageable chunks during encryption and seamlessly reassembled during decryption.

### 🚀 Quick Start

**Encrypting a 5GB file?** Just do it!

1. **Select your file** (100MB, 1GB, 5GB, even 20GB!)
2. **Click Encrypt** - ColorCrypt auto-splits into 500MB chunks
3. **Download all chunks** - Multiple PNG files created
4. **To decrypt:** Select all PNG chunks → Upload → Get original file back!

### How It Works

**Encryption:**
```
Original File: movie.mp4 (5GB)
        ↓
 Auto-Split into chunks
        ↓
 10 chunks × 500MB each
        ↓
 Encrypt each chunk
        ↓
Output: movie_chunk0000.png ... movie_chunk0009.png
```

**Decryption:**
1. Select all 10 PNG chunks (Ctrl+Click)
2. Upload them together
3. ColorCrypt automatically reassembles
4. Download complete original file!

### ⚙️ Configuration

All settings in `config.py`:

```python
# USER CONFIGURABLE!
ENABLE_AUTO_CHUNKING = True               # Enable auto-chunking
CHUNK_SIZE = 500 * 1024 * 1024           # 500MB per chunk (CHANGE THIS!)
MAX_CHUNKS = 1000                        # Max chunks (500GB default)
MAX_CONTENT_LENGTH = 20 * 1024 * 1024 * 1024  # 20GB upload limit
```

**Key Settings:**

- **CHUNK_SIZE** (Default: 500MB) - Size of each chunk
  - Smaller (250MB): More files, easier to manage
  - Larger (1GB-2GB): Fewer files, faster processing
  
- **MAX_CHUNKS** (Default: 1000) - Maximum chunks per file
  - Max file size = `CHUNK_SIZE × MAX_CHUNKS`
  - Default: 500MB × 1000 = **500GB max**
  - Want 1TB? Set `MAX_CHUNKS = 2000`
  - Want unlimited? Set `MAX_CHUNKS = 10000` (5TB+)

- **MAX_CONTENT_LENGTH** (Default: 20GB) - Server upload limit
  - Files stream to disk (doesn't use RAM)
  - Increase for even larger files

### 📊 File Size Capabilities

| Chunk Size | Max Chunks | Maximum File Size |
|-----------|-----------|------------------|
| **500 MB (Default)** | **1000** | **~500 GB** |
| 500 MB | 2000 | ~1 TB |
| 1 GB | 1000 | ~1 TB |
| 1 GB | 5000 | ~5 TB |
| 2 GB | 1000 | ~2 TB |

**Formula:** `Max File Size = CHUNK_SIZE × MAX_CHUNKS`

### ⏱️ Progress Tracking

Watch your encryption/decryption in real-time:
- **Progress bar** with percentage (0-100%)
- **Timer** showing elapsed time
- **ETA** showing estimated time remaining
- **Status messages**: "Splitting file into chunks", "Encrypting chunk 5 of 10", "Reassembling file"

Example for 1GB file:
```
⏱️ 45s | ETA: 1m 15s
70%
Encrypting chunk 3 of 4...
```

---

## 🔑 Using Password Protection

**Encrypting with password:**
1. Select files to encrypt
2. Check "Use password protection"
3. En(Optional) Encrypts data with AES-256-CBC if password provided
   - Creates a header with metadata (signature, size, filename, SHA1 hash)
   - For encrypted files: adds salt and IV to header
   - Combines header + file data
   - Maps data to RGBA pixels (4 bytes per pixel)
   - Saves as a standard PNG image

2. **Decryption Process:**
   - Loads the PNG image
   - Extracts RGBA values from all pixels
   - Checks signature ("ER" = plain, "EC" = encrypted)
   - Parses the header to get metadata
   - If encrypted: derives key from password using PBKDF2
   - Decrypts data with AES-256-CBC
   - Verifies SHA1 hash for integrity
   - Reconstructs the original file

### Security Implementation

**Encryption Algorithm:** AES-256-CBC  
**Key Derivation:** PBKDF2-HMAC-SHA256 (100,000 iterations)  
**Integrity Check:** SHA1 hash  
**Randomization:** Unique salt and IV for each encrypted file  
**Padding:** PKCS7 padding for AES block alignment
Click the sun/moon icon in the header to switch between dark and light themes. Your preference is saved automatically.

### 📦 Bulk Upload

Drag and drop or select multiple files to encrypt them all at once. You can set individual passwords for each file or use one password for all.
## 🛠️ Technical Details

### How It Works

1. **Encryption Process:**
   - Reads the input file as binary data
   - Creates a header with metadata (signature, size, filename, SHA1 hash)
   - Combines header + file data
   - Maps data to RGBA pixels (4 bytes per pixel)
   - Saves as a standard PNG image
 (AES-256)
├── requirements.txt      # Python dependencies
├── templates/
│   ├── index.html        # Main web interface (bulk upload + theme toggle)
│   └── 404.html          # Error page
├── static/
│   ├── style.css         # Encrypted Spectrum theme (dark/light)
│   └── script.js         # Client-side functionality (password + bulk)
### File Structure

```
ColorCrypt/
├── app.py                 # Flask web application
├── colorcrypt.py         # Core encryption/decryption module
├── requirements.txt      # Python dependencies
├──� Support for additional encryption algorithms (ChaCha20, etc.)
- ℹ️ Info command to display metadata without extracting
- 🎨 Steganographic modes (make output look more natural)
- 💾 Database for tracking encrypted files
- 📊 File statistics and history dashboard
- 📤 Bulk download as ZIP archive
- 🔗 Share encrypted files with expiration links
```

---

## 🔒 Future Improvements

- 🔐 AES encryption layer before embedding
- 🔑 Support for multiple encryption algorithms and user-defined keys
- ℹ️ Info command to display metadata without extracting
- 🎨 Steganographic modes (make output look more natural)
- 💾 Database for tracking encrypted files
- 🌙 Dark mode toggle
- 📊 File statistics and history

---

## ⚠️ Disclaimer

ColorCrypt is a tool for privacy and experimentation.
It is not intended to be used for illegal purposes. Please respect the terms of service of the platforms where you use it.

---

## 🙏 Credits

Originally inspired by **ShadeOfColor** (C# version). Remade as a beautiful Python web application with enhanced features and modern UI.

---

## ❤️ Contribute

Pull requests are welcome! Feel free to contribute to make ColorCrypt even better.f the input file before embedding.

Support for multiple encryption algorithms and user-defined keys.

Command -info to quickly display metadata without extracting the file.

Steganographic modes (make the output image look more “natural”).

---

## ⚠️ Disclaimer

ShadeOfColor is a tool for privacy and experimentation.
It is not intended to be used for illegal purposes. Please respect the terms of service of the platforms where you use it.

---

## ❤️ Contribute

Ideas, issues, and pull requests are welcome!
Help us make ShadeOfColor even more powerful and versatile.

---

## 📜 License

MIT License – feel free to use, modify, and share.
