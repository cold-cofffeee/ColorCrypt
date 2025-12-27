"""
ColorCrypt - Core Module
Converts files to images and back using steganography with optional password protection
"""
import math
import hashlib
import struct
from pathlib import Path
from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os


class ColorCrypt:
    """Handles encryption and decryption of files into/from PNG images."""
    
    SIGNATURE = b'ER'
    SIGNATURE_ENCRYPTED = b'EC'  # Encrypted ColorCrypt
    FILENAME_FIELD_LENGTH = 256
    SHA1_LENGTH = 20
    SALT_LENGTH = 32
    IV_LENGTH = 16
    HEADER_LENGTH = 2 + 8 + FILENAME_FIELD_LENGTH + SHA1_LENGTH  # 286 bytes
    ENCRYPTED_HEADER_LENGTH = 2 + 8 + FILENAME_FIELD_LENGTH + SHA1_LENGTH + SALT_LENGTH + IV_LENGTH  # 334 bytes
    
    @classmethod
    def split_file_into_chunks(cls, file_path: str, chunk_size: int) -> list:
        """Split a file into chunks and return chunk file paths."""
        import tempfile
        chunks = []
        file_name = Path(file_path).stem
        file_ext = Path(file_path).suffix
        
        with open(file_path, 'rb') as f:
            chunk_num = 0
            while True:
                chunk_data = f.read(chunk_size)
                if not chunk_data:
                    break
                
                # Create temporary chunk file
                chunk_path = tempfile.mktemp(suffix=f'_chunk{chunk_num:04d}{file_ext}')
                with open(chunk_path, 'wb') as chunk_file:
                    chunk_file.write(chunk_data)
                
                chunks.append({
                    'path': chunk_path,
                    'number': chunk_num,
                    'size': len(chunk_data)
                })
                chunk_num += 1
        
        return chunks
    
    @classmethod
    def reassemble_chunks(cls, chunk_paths: list, output_path: str) -> None:
        """Reassemble chunks into original file."""
        with open(output_path, 'wb') as output_file:
            for chunk_path in sorted(chunk_paths):
                with open(chunk_path, 'rb') as chunk_file:
                    output_file.write(chunk_file.read())
    
    @classmethod
    def calculate_output_size(cls, input_file_size: int, is_encrypted: bool = False) -> int:
        """
        Calculate the expected output PNG file size for a given input file.
        
        Args:
            input_file_size: Size of the input file in bytes
            is_encrypted: Whether the file will be password-protected
        
        Returns:
            Estimated size of the output PNG file in bytes
        """
        # Calculate data size (header + file data)
        if is_encrypted:
            # Encrypted data is padded to 16-byte blocks (AES block size)
            encrypted_size = input_file_size
            # Add padding for AES block alignment
            if encrypted_size % 16 != 0:
                encrypted_size += (16 - encrypted_size % 16)
            data_size = cls.ENCRYPTED_HEADER_LENGTH + encrypted_size
        else:
            data_size = cls.HEADER_LENGTH + input_file_size
        
        # Calculate image dimensions (RGBA = 4 bytes per pixel)
        pixels_needed = math.ceil(data_size / 4.0)
        image_size = math.ceil(math.sqrt(pixels_needed))
        
        # Estimate PNG file size (actual size varies due to compression)
        # PNG overhead: header (~8 bytes) + IHDR chunk (~25 bytes) + IDAT chunk header (~12 bytes per chunk)
        # + IEND chunk (~12 bytes) + uncompressed RGBA data
        # Compression typically reduces size by 10-30%, but we use worst case (no compression)
        uncompressed_data = image_size * image_size * 4  # RGBA
        png_overhead = 8 + 25 + 12 + 12  # Basic PNG structure
        chunk_overhead = (uncompressed_data // 8192 + 1) * 12  # Multiple IDAT chunks
        
        estimated_size = png_overhead + chunk_overhead + uncompressed_data
        
        # Add 10% safety margin
        return int(estimated_size * 1.1)
    
    @classmethod
    def encrypt_file_to_image(cls, input_file_path: str, output_image_path: str, password: str = None) -> None:
        """
        Convert a file into a PNG image with optional password protection.
        
        Args:
            input_file_path: Path to the file to encrypt
            output_image_path: Path where the output PNG will be saved
            password: Optional password for AES encryption
        """
        # Read the file
        with open(input_file_path, 'rb') as f:
            file_bytes = f.read()
        
        file_name = Path(input_file_path).name
        
        # Encrypt data if password provided
        if password:
            salt = os.urandom(cls.SALT_LENGTH)
            iv = os.urandom(cls.IV_LENGTH)
            encrypted_data = cls._encrypt_data(file_bytes, password, salt, iv)
            header = cls._create_encrypted_header(encrypted_data, file_name, salt, iv)
            data = header + encrypted_data
        else:
            header = cls._create_header(file_bytes, file_name)
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
    def decrypt_image_to_file(cls, input_image_path: str, output_dir: str = '.', password: str = None) -> str:
        """
        Recover the original file from a PNG image.
        
        Args:
            input_image_path: Path to the encrypted PNG image
            output_dir: Directory where the file will be saved (uses embedded filename)
            password: Optional password if file is encrypted
        
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
        
        # Check signature to determine if encrypted
        signature = bytes(all_bytes[0:2])
        
        if signature == cls.SIGNATURE_ENCRYPTED:
            # Encrypted file - requires password
            if not password:
                raise ValueError("This file is password protected. Please provide a password.")
            return cls._decrypt_encrypted_file(all_bytes, output_dir, password)
        elif signature == cls.SIGNATURE:
            # Non-encrypted file
            return cls._decrypt_plain_file(all_bytes, output_dir)
        else:
            raise ValueError("Invalid signature: not a ColorCrypt image")
    
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
    
    @classmethod
    def _create_encrypted_header(cls, encrypted_data: bytes, file_name: str, salt: bytes, iv: bytes) -> bytes:
        """Create the header for password-protected encrypted image."""
        # Calculate SHA1 of encrypted data
        sha1_hash = hashlib.sha1(encrypted_data).digest()
        
        # Encode filename (UTF-8)
        name_bytes = file_name.encode('utf-8')
        if len(name_bytes) > cls.FILENAME_FIELD_LENGTH:
            raise ValueError(f"Filename too long (max {cls.FILENAME_FIELD_LENGTH} bytes UTF-8)")
        
        # Build header
        header = bytearray(cls.ENCRYPTED_HEADER_LENGTH)
        
        # Signature "EC" (Encrypted ColorCrypt)
        header[0:2] = cls.SIGNATURE_ENCRYPTED
        
        # File size (8 bytes, little-endian)
        header[2:10] = struct.pack('<Q', len(encrypted_data))
        
        # Filename (padded with zeros)
        header[10:10 + len(name_bytes)] = name_bytes
        
        # SHA1 hash (20 bytes)
        offset = 10 + cls.FILENAME_FIELD_LENGTH
        header[offset:offset + cls.SHA1_LENGTH] = sha1_hash
        
        # Salt (32 bytes)
        offset += cls.SHA1_LENGTH
        header[offset:offset + cls.SALT_LENGTH] = salt
        
        # IV (16 bytes)
        offset += cls.SALT_LENGTH
        header[offset:offset + cls.IV_LENGTH] = iv
        
        return bytes(header)
    
    @classmethod
    def _encrypt_data(cls, data: bytes, password: str, salt: bytes, iv: bytes) -> bytes:
        """Encrypt data using AES-256-CBC with PBKDF2 key derivation."""
        # Derive key from password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode('utf-8'))
        
        # Pad data to AES block size (16 bytes)
        padding_length = 16 - (len(data) % 16)
        padded_data = data + bytes([padding_length] * padding_length)
        
        # Encrypt
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        
        return encrypted
    
    @classmethod
    def _decrypt_data(cls, encrypted_data: bytes, password: str, salt: bytes, iv: bytes) -> bytes:
        """Decrypt data using AES-256-CBC with PBKDF2 key derivation."""
        # Derive key from password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode('utf-8'))
        
        # Decrypt
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Remove padding
        padding_length = decrypted[-1]
        return decrypted[:-padding_length]
    
    @classmethod
    def _decrypt_plain_file(cls, all_bytes: bytearray, output_dir: str) -> str:
        """Decrypt a non-password-protected file."""
        if len(all_bytes) < cls.HEADER_LENGTH:
            raise ValueError("Insufficient data for header")
        
        file_size = struct.unpack('<Q', bytes(all_bytes[2:10]))[0]
        
        if file_size < 0:
            raise ValueError("Invalid file size in header")
        
        # Extract filename
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
    def _decrypt_encrypted_file(cls, all_bytes: bytearray, output_dir: str, password: str) -> str:
        """Decrypt a password-protected file."""
        if len(all_bytes) < cls.ENCRYPTED_HEADER_LENGTH:
            raise ValueError("Insufficient data for encrypted header")
        
        file_size = struct.unpack('<Q', bytes(all_bytes[2:10]))[0]
        
        if file_size < 0:
            raise ValueError("Invalid file size in header")
        
        # Extract filename
        filename_bytes = bytes(all_bytes[10:10 + cls.FILENAME_FIELD_LENGTH])
        embedded_name = filename_bytes.rstrip(b'\x00').decode('utf-8')
        
        # Extract stored SHA1
        offset = 10 + cls.FILENAME_FIELD_LENGTH
        sha1_stored = bytes(all_bytes[offset:offset + cls.SHA1_LENGTH])
        
        # Extract salt
        offset += cls.SHA1_LENGTH
        salt = bytes(all_bytes[offset:offset + cls.SALT_LENGTH])
        
        # Extract IV
        offset += cls.SALT_LENGTH
        iv = bytes(all_bytes[offset:offset + cls.IV_LENGTH])
        
        data_offset = cls.ENCRYPTED_HEADER_LENGTH
        
        if data_offset + file_size > len(all_bytes):
            raise ValueError("Image doesn't contain all declared data")
        
        # Extract encrypted data
        encrypted_data = bytes(all_bytes[data_offset:data_offset + file_size])
        
        # Verify SHA1 of encrypted data
        sha1_calc = hashlib.sha1(encrypted_data).digest()
        if sha1_stored != sha1_calc:
            raise ValueError("SHA1 mismatch: data is corrupted or altered")
        
        # Decrypt data
        try:
            file_data = cls._decrypt_data(encrypted_data, password, salt, iv)
        except Exception:
            raise ValueError("Invalid password or corrupted data")
        
        # Determine output path
        output_path = Path(output_dir) / embedded_name
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(output_path, 'wb') as f:
            f.write(file_data)
        
        return str(output_path)


def main():
    """Command-line interface for ColorCrypt."""
    import sys
    import os
    import getpass
    
    def print_help():
        print("ColorCrypt - Hide files inside PNG images")
        print()
        print("Usage:")
        print("  python colorcrypt.py -crypt <inputFile> <outputImage.png> [--password]")
        print("  python colorcrypt.py -decrypt <inputImage.png> [--password]")
    
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
            password = None
            if len(sys.argv) > 4 and sys.argv[4] == '--password':
                password = getpass.getpass("Enter password: ")
            ColorCrypt.encrypt_file_to_image(input_file, output_image, password)
            print(f"✓ OK: '{input_file}' -> '{output_image}'")
        
        elif command == '-decrypt':
            if len(sys.argv) < 3:
                print_help()
                return
            input_image = sys.argv[2]
            password = None
            if len(sys.argv) > 3 and sys.argv[3] == '--password':
                password = getpass.getpass("Enter password: ")
            saved_as = ColorCrypt.decrypt_image_to_file(input_image, os.getcwd(), password)
            print(f"✓ OK: '{input_image}' -> '{saved_as}'")
        
        else:
            print(f"Unknown command: {command}")
            print_help()
    
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
