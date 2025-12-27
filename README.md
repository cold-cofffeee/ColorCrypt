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

- 🌐 **Beautiful Web Interface**: Modern, gradient-based UI with drag-and-drop functionality
- 🔄 **Two-way conversion**:  
  - **Encrypt**: Transform any file into a PNG image  
  - **Decrypt**: Restore the original file from the PNG  

- 📝 **Embedded metadata**:  
  - Signature `"ER"` for file validation
  - Original file size  
  - Original filename  
  - SHA1 hash for integrity check  

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
## 🛠️ Technical Details

### How It Works

1. **Encryption Process:**
   - Reads the input file as binary data
   - Creates a header with metadata (signature, size, filename, SHA1 hash)
   - Combines header + file data
   - Maps data to RGBA pixels (4 bytes per pixel)
   - Saves as a standard PNG image

2. **Decryption Process:**
   - Loads the PNG image
   - Extracts RGBA values from all pixels
   - Parses the header to get metadata
   - Verifies SHA1 hash for integrity
   - Reconstructs the original file

### File Structure

```
ColorCrypt/
├── app.py                 # Flask web application
├── colorcrypt.py         # Core encryption/decryption module
├── requirements.txt      # Python dependencies
├── templates/
│   ├── index.html        # Main web interface
│   └── 404.html          # Error page
├── static/
│   ├── style.css         # Beautiful gradient styling
│   └── script.js         # Client-side functionality
└── README.md
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
