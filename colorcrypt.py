"""
ColorCrypt - Core Module
Converts files to images and back using steganography
"""
import math
import hashlib
import struct
from pathlib import Path
from PIL import Image


class ColorCrypt:
    """Handles encryption and decryption of files into/from PNG images."""
    
    SIGNATURE = b'ER'
    FILENAME_FIELD_LENGTH = 256
    SHA1_LENGTH = 20
    HEADER_LENGTH = 2 + 8 + FILENAME_FIELD_LENGTH + SHA1_LENGTH  # 286 bytes
    
    @classmethod
    def encrypt_file_to_image(cls, input_file_path: str, output_image_path: str) -> None:
        """
        Convert a file into a PNG image.
        
        Args:
            input_file_path: Path to the file to encrypt
            output_image_path: Path where the output PNG will be saved
        """
        # Read the file
        with open(input_file_path, 'rb') as f:
            file_bytes = f.read()
        
        file_name = Path(input_file_path).name
        
        # Create header
        header = cls._create_header(file_bytes, file_name)
        
        # Combine header + file data
        data = header + file_bytes
        
        # Calculate image size (RGBA = 4 bytes per pixel)
        size = math.ceil(math.sqrt(len(data) / 4.0))
        
        # Create image
        img = Image.new('RGBA', (size, size))
        pixels = img.load()
        
        i = 0
        for y in range(size):
            for x in range(size):
                r = data[i] if i < len(data) else 0
                i += 1
                g = data[i] if i < len(data) else 0
                i += 1
                b = data[i] if i < len(data) else 0
                i += 1
                a = data[i] if i < len(data) else 255  # padding alpha
                i += 1
                pixels[x, y] = (r, g, b, a)
        
        # Save as PNG
        img.save(output_image_path, 'PNG')
    
    @classmethod
    def decrypt_image_to_file(cls, input_image_path: str, output_dir: str = '.') -> str:
        """
        Recover the original file from a PNG image.
        
        Args:
            input_image_path: Path to the encrypted PNG image
            output_dir: Directory where the file will be saved (uses embedded filename)
        
        Returns:
            Path to the saved file
        """
        # Load image
        img = Image.open(input_image_path)
        img = img.convert('RGBA')
        
        # Extract all bytes from RGBA channels
        pixels = img.load()
        width, height = img.size
        all_bytes = bytearray()
        
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                all_bytes.extend([r, g, b, a])
        
        # Parse header
        if len(all_bytes) < cls.HEADER_LENGTH:
            raise ValueError("Insufficient data for header")
        
        signature = bytes(all_bytes[0:2])
        if signature != cls.SIGNATURE:
            raise ValueError("Invalid signature: not a ColorCrypt image")
        
        file_size = struct.unpack('<Q', bytes(all_bytes[2:10]))[0]  # little-endian uint64
        
        if file_size < 0:
            raise ValueError("Invalid file size in header")
        
        # Extract filename (UTF-8, null-terminated)
        filename_bytes = bytes(all_bytes[10:10 + cls.FILENAME_FIELD_LENGTH])
        embedded_name = filename_bytes.rstrip(b'\x00').decode('utf-8')
        
        # Extract stored SHA1
        sha1_stored = bytes(all_bytes[10 + cls.FILENAME_FIELD_LENGTH:10 + cls.FILENAME_FIELD_LENGTH + cls.SHA1_LENGTH])
        
        data_offset = cls.HEADER_LENGTH
        
        if data_offset + file_size > len(all_bytes):
            raise ValueError("Image doesn't contain all declared data")
        
        # Extract file data
        file_data = bytes(all_bytes[data_offset:data_offset + file_size])
        
        # Verify SHA1
        sha1_calc = hashlib.sha1(file_data).digest()
        if sha1_stored != sha1_calc:
            raise ValueError("SHA1 mismatch: data is corrupted or altered")
        
        # Determine output path
        output_path = Path(output_dir) / embedded_name
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(output_path, 'wb') as f:
            f.write(file_data)
        
        return str(output_path)
    
    @classmethod
    def _create_header(cls, file_bytes: bytes, file_name: str) -> bytes:
        """Create the header for the encrypted image."""
        # Calculate SHA1
        sha1_hash = hashlib.sha1(file_bytes).digest()
        
        # Encode filename (UTF-8)
        name_bytes = file_name.encode('utf-8')
        if len(name_bytes) > cls.FILENAME_FIELD_LENGTH:
            raise ValueError(f"Filename too long (max {cls.FILENAME_FIELD_LENGTH} bytes UTF-8)")
        
        # Build header
        header = bytearray(cls.HEADER_LENGTH)
        
        # Signature "ER"
        header[0:2] = cls.SIGNATURE
        
        # File size (8 bytes, little-endian)
        header[2:10] = struct.pack('<Q', len(file_bytes))
        
        # Filename (padded with zeros)
        header[10:10 + len(name_bytes)] = name_bytes
        
        # SHA1 hash (20 bytes)
        header[10 + cls.FILENAME_FIELD_LENGTH:10 + cls.FILENAME_FIELD_LENGTH + cls.SHA1_LENGTH] = sha1_hash
        
        return bytes(header)


def main():
    """Command-line interface for ColorCrypt."""
    import sys
    import os
    
    def print_help():
        print("ColorCrypt - Hide files inside PNG images")
        print()
        print("Usage:")
        print("  python colorcrypt.py -crypt <inputFile> <outputImage.png>")
        print("  python colorcrypt.py -decrypt <inputImage.png>")
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    try:
        if command == '-crypt':
            if len(sys.argv) < 4:
                print_help()
                return
            input_file = sys.argv[2]
            output_image = sys.argv[3]
            ColorCrypt.encrypt_file_to_image(input_file, output_image)
            print(f"✓ OK: '{input_file}' -> '{output_image}'")
        
        elif command == '-decrypt':
            if len(sys.argv) < 3:
                print_help()
                return
            input_image = sys.argv[2]
            saved_as = ColorCrypt.decrypt_image_to_file(input_image, os.getcwd())
            print(f"✓ OK: '{input_image}' -> '{saved_as}'")
        
        else:
            print(f"Unknown command: {command}")
            print_help()
    
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
