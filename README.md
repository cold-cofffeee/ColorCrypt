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

- 🎨 **Dark/Light Theme Toggle**: 
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

### 🔑 Using Password Protection

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
