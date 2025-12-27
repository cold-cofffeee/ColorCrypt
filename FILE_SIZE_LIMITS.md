# ColorCrypt - Automatic File Chunking System

## 🚀 Quick Start

**Want to encrypt a 5GB file?** Just do it! ColorCrypt handles everything automatically.

1. **Select your file** (any size - 100MB, 1GB, 5GB, even larger!)
2. **Click Encrypt** - ColorCrypt auto-splits it into chunks
3. **Download all chunks** - Get multiple PNG files  
4. **To decrypt:** Select all PNG chunks → Upload → Get original file back!

That's it! No manual splitting, no configuration needed.

---

## 🎯 Overview

ColorCrypt now features **automatic file chunking** to handle files of any size! Large files are automatically split into manageable chunks during encryption, and seamlessly reassembled during decryption.

### How It Works

**Encryption:**
- Files larger than 500MB are automatically split into chunks
- Each chunk is encrypted separately into a PNG image
- You receive multiple PNG files (e.g., `file_chunk0000.png`, `file_chunk0001.png`, etc.)

**Decryption:**
- Select all chunk PNGs when decrypting
- ColorCrypt automatically reassembles them into the original file
- You get back your complete original file

### Example: Encrypting a 5GB File

```
Original File: movie.mp4 (5GB)
                ↓
        Automatic Splitting
                ↓
    10 chunks × 500MB each
                ↓
    Encrypt Each Chunk
                ↓
Output: movie_chunk0000.png ... movie_chunk0009.png
```

**To Decrypt:**
1. Select all 10 PNG chunks
2. Upload them together
3. Get back: movie.mp4 (5GB original file)

## ⚙️ Configuration

All settings are in `config.py`:

```python
# Automatic Chunking - USER CONFIGURABLE!
ENABLE_AUTO_CHUNKING = True               # Enable/disable auto-chunking
CHUNK_SIZE = 500 * 1024 * 1024            # 500 MB per chunk (CHANGE THIS!)
MAX_CHUNKS = 1000                         # Max 1000 chunks (500GB with 500MB chunks)

# NO FILE SIZE LIMIT!
# File size only limited by: CHUNK_SIZE × MAX_CHUNKS
# Default: 500MB × 1000 = 500GB maximum
# Want bigger? Increase MAX_CHUNKS!
```

### Key Settings Explained

**ENABLE_AUTO_CHUNKING** (Default: `True`)
- When `True`: Large files automatically split into chunks - **NO SIZE LIMIT!**
- When `False`: Files processed as single PNG (not recommended for large files)

**CHUNK_SIZE** (Default: 500MB) ⭐ **USER CONFIGURABLE**
- Size of each chunk - **SET YOUR PREFERRED SIZE HERE!**
- 500MB default works for most use cases
- Want smaller chunks? Set to 100MB or 250MB
- Want larger chunks? Set to 1GB or 2GB
- Adjust based on your needs and system capabilities

**MAX_CHUNKS** (Default: 1000)
- Maximum chunks per file
- This is your only "limit": `Max File Size = CHUNK_SIZE × MAX_CHUNKS`
- Default: 500MB × 1000 = **500GB max**
- Want to encrypt 1TB files? Set `MAX_CHUNKS = 2000`
- Want unlimited? Set `MAX_CHUNKS = 10000` (5TB with 500MB chunks!)

**MAX_CHUNKS** (Default: 100)
- Maximum chunks per file (prevents abuse)
- 100 chunks × 45MB = ~4.5GB max file size
- Increase for larger files

### Adjusting for Different Use Cases

#### Default Configuration (Recommended for Most Users)
```python
ENABLE_AUTO_CHUNKING = True
CHUNK_SIZE = 500 * 1024 * 1024  # 500 MB - good balance
MAX_CHUNKS = 100                # Up to 50GB files
```
**Best for:** General use, videos, large documents

#### Smaller Chunks (More manageable files)
```python
ENABLE_AUTO_CHUNKING = True
CHUNK_SIZE = 250 * 1024 * 1024  # 250 MB chunks
MAX_CHUNKS = 100                # Up to 25GB files
```
**Best for:** Limited bandwidth, easier chunk management

#### Larger Chunks (Fewer files to manage)
```python
ENABLE_AUTO_CHUNKING = True
CHUNK_SIZE = 1024 * 1024 * 1024  # 1 GB chunks
MAX_CHUNKS = 100                 # Up to 100GB files
```
**Best for:** High-speed systems, very large files

#### Maximum Capacity (Handle massive files)
```python
ENABLE_AUTO_CHUNKING = True
CHUNK_SIZE = 2048 * 1024 * 1024  # 2 GB chunks
MAX_CHUNKS = 200                 # Up to 400GB files!
```
**Best for:** Enterprise use, backup systems, data archival

#### Conservative/Public Server
```python
ENABLE_AUTO_CHUNKING = True
CHUNK_SIZE = 100 * 1024 * 1024  # 100 MB chunks
MAX_CHUNKS = 50                 # Max 5GB files
```
**Best for:** Shared hosting, limited resources

#### Disable Chunking (Simple mode)
```python
ENABLE_AUTO_CHUNKING = False
MAX_INPUT_FILE_SIZE = 100 * 1024 * 1024  # Just increase single file limit
```
**Best for:** Small files only, testing

## 📊 File Size Capabilities

| Chunk Size | Max Chunks | Maximum File Size |
|-----------|-----------|------------------|
| **500 MB (Default)** | **1000** | **~500 GB** |
| 500 MB | 2000 | ~1 TB |
| 250 MB | 1000 | ~250 GB |
| 1 GB | 1000 | ~1 TB |
| 1 GB | 5000 | ~5 TB |
| 2 GB | 1000 | ~2 TB |

**Formula:** `Max File Size = CHUNK_SIZE × MAX_CHUNKS`

**No Hard Limits!** Just increase `MAX_CHUNKS` to handle larger files. Want to encrypt 10TB? No problem - just set it up!

**Recommendation:** The default 500MB × 1000 chunks = 500GB max is suitable for most use cases.

## 🚀 How to Use

### Encrypting Large Files

**Single File (Automatic Chunking):**
1. Select your large file (e.g., 5GB video)
2. Click "Encrypt"
3. System automatically detects file is large
4. Splits into chunks (e.g., 10 chunks of 500MB each)
5. Encrypts each chunk
6. You get 10 PNG files

**Download Options:**
- Download each chunk individually
- Or click "Download All Chunks" to get all at once

### Decrypting Chunked Files

**Multi-Chunk Upload:**
1. Select ALL chunk PNGs together (Ctrl+Click or Shift+Click)
2. Upload all chunks at once
3. System automatically:
   - Detects you're uploading chunks
   - Decrypts each chunk
   - Reassembles into original file
4. Download your complete original file!

**Important:** You must upload ALL chunks together for successful decryption.

## 🎨 User Interface

### Encryption Tab
- Shows chunking info: "Large files auto-split into 500MB chunks" (or your configured size)
- When file is chunked, you'll see:
  - Original filename
  - Number of chunks created
  - Individual download buttons for each chunk
  - "Download All Chunks" button

### Decryption Tab
- Updated to accept multiple files
- Hint text: "For chunked files, select all chunks"
- After decryption: Shows "Reassembled from X chunks"

## 💡 Why Chunking?

### The Problem
Encryption doesn't compress - it adds overhead:
- 5GB file → 5.5GB encrypted (not smaller!)
- Single large PNG files:
  - Consume massive memory
  - Slow to process
  - Can crash browsers/servers

### The Solution
Chunking provides:
- ✅ **Unlimited file sizes** - Handle files of any size
- ✅ **Memory efficient** - Process only 45MB at a time
- ✅ **No crashes** - Stable operation
- ✅ **Parallel processing** - Can encrypt chunks in parallel (future)
- ✅ **Resume capability** - Re-encrypt failed chunks only (future)
- ✅ **Better control** - Manageable file sizes

## 🔧 Technical Details

### Chunking Process

**Encryption Flow:**
```python
1. Check file size > CHUNK_SIZE?
2. If yes:
   - Split file into chunks
   - Name: filename_chunk0000.png, filename_chunk0001.png, etc.
   - Encrypt each chunk separately
   - Return array of chunk info
3. If no:
   - Encrypt normally as single PNG
```

**Decryption Flow:**
```python
1. Check number of files uploaded
2. If multiple files:
   - Assume chunked encryption
   - Decrypt each chunk
   - Sort chunks by name
   - Reassemble in correct order
   - Return complete file
3. If single file:
   - Decrypt normally
```

### Chunk Naming Convention
```
original_name.ext → original_name_chunk0000_encrypted.png
                 → original_name_chunk0001_encrypted.png
                 → original_name_chunk0002_encrypted.png
```

Chunks are zero-padded (0000, 0001, etc.) for proper sorting.

### Memory Usage

**Without Chunking:**
- 5GB file needs ~10GB RAM (input + output + overhead)

**With Chunking (500MB chunks):**
- Uses ~1.1GB RAM per chunk
- Processes one 500MB chunk at a time
- Total RAM needed: ~1.1GB (constant regardless of total file size)

## 🛡️ Security Notes

1. **Password Protection:** All chunks use the same password
2. **Chunk Order:** Chunks must be reassembled in correct order
3. **Missing Chunks:** If any chunk is lost, file cannot be fully recovered
4. **Chunk Integrity:** Each chunk has its own SHA1 hash verification

## ⚠️ Limitations & Considerations

### Current Limitations

1. **Sequential Processing:** Chunks encrypted one at a time (parallelization coming soon)
2. **All Chunks Required:** Missing even one chunk = file corruption
3. **Chunk Management:** User must keep track of all chunks
4. **No Automatic Compression:** Files not compressed before chunking

### Best Practices

**DO:**
- ✅ Keep all chunks together in same folder
- ✅ Use descriptive filenames before encryption
- ✅ Backup chunks separately
- ✅ Test decryption immediately after encryption

**DON'T:**
- ❌ Delete or lose individual chunks
- ❌ Rename chunks manually
- ❌ Mix chunks from different files
- ❌ Upload partial chunk sets for decryption

## 📈 Performance Guidelines

### Recommended Settings by System

**Low-End System (4GB RAM):**
```python
CHUNK_SIZE = 25 * 1024 * 1024  # 25 MB
MAX_CHUNKS = 40                # Max 1GB files
```

**Mid-Range System (8GB RAM):**
```python
CHUNK_SIZE = 45 * 1024 * 1024  # 45 MB
MAX_CHUNKS = 100               # Max 4.5GB files
```

**High-End System (16GB+ RAM):**
```python
CHUNK_SIZE = 90 * 1024 * 1024  # 90 MB
MAX_CHUNKS = 500               # Max 45GB files
```

### Processing Times (Approximate)

| File Size | Chunks (500MB) | Encryption Time | Decryption Time |
|-----------|--------|----------------|------------------|
| 500 MB | 1 | ~30 seconds | ~20 seconds |
| 1 GB | 2 | ~60 seconds | ~40 seconds |
| 5 GB | 10 | ~5 minutes | ~3 minutes |
| 10 GB | 20 | ~10 minutes | ~6 minutes |
| 50 GB | 100 | ~50 minutes | ~30 minutes |

*Times vary based on system performance and chunk size configuration*

## 🔮 Future Enhancements

### Planned Features

1. **Parallel Chunk Processing**
   - Encrypt multiple chunks simultaneously
   - 3-5x faster for large files

2. **Automatic Compression**
   - Compress before chunking for compressible files
   - Reduce total chunks needed

3. **Resume Support**
   - Resume interrupted encryptions
   - Re-encrypt only failed chunks

4. **Chunk Archives**
   - Auto-zip all chunks into single archive
   - Easier management

5. **Progress Tracking**
   - Real-time progress bar
   - "Chunk X of Y encrypting..."

6. **Smart Chunk Size**
   - Auto-adjust chunk size based on file type
   - Smaller chunks for text, larger for video

## 🐛 Troubleshooting

**Q: File too large error despite chunking enabled**
A: Increase `MAX_CHUNKS` in config.py to allow more chunks.

**Q: Decryption fails with "missing chunks"**
A: Ensure you've selected ALL chunk files. Check file names for sequence.

**Q: Chunks won't upload**
A: Check browser file upload limits. Try uploading in smaller batches.

**Q: How do I know how many chunks were created?**
A: After encryption, the UI shows "Split into X chunks".

**Q: Can I encrypt chunks with different passwords?**
A: Currently no. All chunks use the same password from the original file.

**Q: What if I lose one chunk?**
A: File cannot be fully recovered. All chunks are required.

**Q: Can I manually merge chunks?**
A: No, use ColorCrypt's decryption feature which handles reassembly automatically.

## 📝 Summary

**File Size Limits:**
```
Small Files (< 500MB)   → Encrypted as single PNG
Large Files (> 500MB)   → Auto-split into 500MB chunks (default)
Maximum File Size       → CHUNK_SIZE × MAX_CHUNKS (default 500GB)
Chunk Size             → USER CONFIGURABLE in config.py
NO HARD LIMITS         → Just increase MAX_CHUNKS for bigger files!
```

**Key Benefits:**
- ✅ **NO FILE SIZE LIMIT** - handle files of ANY size!
- ✅ **User configurable chunk size** - set your preferred size!
- ✅ Default supports up to 500GB files
- ✅ Want 1TB? 5TB? 10TB? Just increase MAX_CHUNKS!
- ✅ No server crashes or memory issues  
- ✅ Automatic - user doesn't need to think about it
- ✅ Seamless decryption - just select all chunks

**Configuration:**
- Edit `config.py`
- Set `CHUNK_SIZE` to your preferred size (default: 500MB)
- Set `MAX_CHUNKS` for your max file size (default: 1000 = 500GB max)
- Restart server
- Done!

**Example Configurations:**
```python
# For very large files (up to 1TB)
CHUNK_SIZE = 500 * 1024 * 1024  # 500 MB chunks
MAX_CHUNKS = 2000               # 2000 × 500MB = 1TB

# For huge files (up to 5TB!)
CHUNK_SIZE = 1024 * 1024 * 1024  # 1 GB chunks
MAX_CHUNKS = 5000                # 5000 × 1GB = 5TB

# Virtually unlimited (10TB+)
CHUNK_SIZE = 2048 * 1024 * 1024  # 2 GB chunks
MAX_CHUNKS = 5000                # 5000 × 2GB = 10TB!
```

---

**ColorCrypt with Auto-Chunking = Unlimited Possibilities! 🎨🔒**

```python
# Maximum size for the input file before encryption
MAX_INPUT_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

# Maximum size for the encrypted output PNG image
MAX_OUTPUT_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

# Maximum total upload size for web requests
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB

# Maximum number of files in a single bulk upload
MAX_FILES_PER_BATCH = 10

# Maximum total size for all files in bulk upload
MAX_BULK_TOTAL_SIZE = 200 * 1024 * 1024  # 200 MB
```

### How to Change Limits

1. Open `config.py`
2. Modify the desired limit values (in bytes)
3. Save the file
4. Restart the ColorCrypt application

**Example:** To increase the maximum input file size to 100 MB:
```python
MAX_INPUT_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
```

## Validation Stages

### 1. Client-Side Validation (JavaScript)
- Validates file size immediately upon selection
- Checks individual file sizes against `MAX_INPUT_FILE_SIZE`
- Validates total size for bulk uploads against `MAX_BULK_TOTAL_SIZE`
- Checks number of files against `MAX_FILES_PER_BATCH`
- Provides instant feedback without server roundtrip

### 2. Server-Side Pre-Encryption Validation (Python)
- Double-checks all client-side validations
- Validates actual file size after upload
- Calculates expected encrypted output size
- Rejects files that would exceed `MAX_OUTPUT_FILE_SIZE`

### 3. Output Size Estimation
The system calculates the expected PNG file size before encryption:
- Considers header size (standard vs encrypted)
- Accounts for AES encryption padding (16-byte blocks)
- Calculates image dimensions needed (RGBA pixels)
- Estimates PNG overhead and compression
- Adds 10% safety margin

### 4. Post-Encryption Validation
- Verifies actual output file size
- Final safety check before delivery
- Cleans up files if limit exceeded

## Error Messages

Users will see clear, informative error messages when limits are exceeded:

- **"File too large"** - Individual file exceeds `MAX_INPUT_FILE_SIZE`
- **"Total file size exceeds limit"** - Bulk upload exceeds `MAX_BULK_TOTAL_SIZE`
- **"Too many files"** - Exceeds `MAX_FILES_PER_BATCH`
- **"Would produce an image that is too large"** - Encrypted output would exceed `MAX_OUTPUT_FILE_SIZE`

## User Interface

The file size limits are displayed in the UI for user awareness:
- Shown in the info box at the top of the Encrypt tab
- Dynamically loaded from the server
- Updates automatically if limits change

## API Endpoint

A new API endpoint provides limit information:

```
GET /api/limits
```

Returns JSON with current limits:
```json
{
    "max_input_size": 52428800,
    "max_output_size": 104857600,
    "max_input_size_formatted": "50.00 MB",
    "max_output_size_formatted": "100.00 MB",
    "max_files_per_batch": 10,
    "max_bulk_total_size": 209715200,
    "max_bulk_total_size_formatted": "200.00 MB"
}
```

## Technical Details

### Output Size Calculation Formula

```python
def calculate_output_size(input_file_size, is_encrypted):
    if is_encrypted:
        # Add AES padding (16-byte blocks)
        encrypted_size = ceil_to_16_bytes(input_file_size)
        data_size = ENCRYPTED_HEADER_LENGTH + encrypted_size
    else:
        data_size = HEADER_LENGTH + input_file_size
    
    # Calculate image dimensions (4 bytes per RGBA pixel)
    pixels_needed = ceil(data_size / 4.0)
    image_size = ceil(sqrt(pixels_needed))
    
    # Estimate PNG size with overhead and 10% safety margin
    uncompressed_data = image_size * image_size * 4
    png_overhead = 8 + 25 + 12 + 12  # Header + chunks
    chunk_overhead = (uncompressed_data // 8192 + 1) * 12
    
    estimated_size = (png_overhead + chunk_overhead + uncompressed_data) * 1.1
    return estimated_size
```

### Header Sizes
- **Standard Header**: 286 bytes (signature + file size + filename + SHA1)
- **Encrypted Header**: 334 bytes (standard + salt + IV)

## Benefits

1. **Prevents Server Overload** - Stops oversized uploads before processing
2. **Better User Experience** - Immediate feedback on file size issues
3. **Resource Management** - Predictable memory and storage usage
4. **Easy Configuration** - Central config file for all limits
5. **Transparent** - Users see limits clearly in the UI

## Recommendations

### For Personal Use (Default)
```python
MAX_INPUT_FILE_SIZE = 50 * 1024 * 1024   # 50 MB
MAX_OUTPUT_FILE_SIZE = 100 * 1024 * 1024 # 100 MB
MAX_FILES_PER_BATCH = 10
```
**Use case:** Documents, photos, small videos, personal files

### For Production/Server Deployment (Conservative)
```python
MAX_INPUT_FILE_SIZE = 25 * 1024 * 1024   # 25 MB
MAX_OUTPUT_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
MAX_FILES_PER_BATCH = 5
```
**Use case:** Public servers, shared hosting, limited resources

### For High-Performance Systems (Generous)
```python
MAX_INPUT_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
MAX_OUTPUT_FILE_SIZE = 200 * 1024 * 1024 # 200 MB
MAX_FILES_PER_BATCH = 20
```
**Use case:** Powerful dedicated servers, internal tools

### ⚠️ For Very Large Files (Advanced Users Only)
```python
MAX_INPUT_FILE_SIZE = 500 * 1024 * 1024   # 500 MB
MAX_OUTPUT_FILE_SIZE = 1024 * 1024 * 1024 # 1 GB
MAX_FILES_PER_BATCH = 5
```
**Warning:** Requires significant RAM (2GB+ available), fast CPU, and SSD storage. Not recommended for web deployment.

## 🚨 Handling Very Large Files (GB+ sizes)

### The Problem
ColorCrypt's current architecture loads entire files into memory, which becomes problematic for large files:
- **5GB file** = Needs ~10GB RAM (input + output + processing overhead)
- **Memory exhaustion** = Server crashes
- **Processing time** = Minutes to hours
- **PNG limitations** = Single image files become unwieldy

### Strategies for Large Files

#### 1. **Pre-Compression (Recommended for Compressible Data)**
Compress files before encryption to reduce size:

```bash
# Compress first, then encrypt
zip -9 myfile.zip large_file.doc
# Then encrypt myfile.zip (much smaller)
```

**Benefits:**
- Text documents: 70-90% size reduction
- Office files: 60-80% size reduction
- Already compressed (videos, JPEGs): Minimal benefit

**Limitations:**
- Two-step process (compress, encrypt, decrypt, decompress)
- Already compressed files won't benefit

#### 2. **File Splitting (Most Practical for Large Files)**
Split large files into smaller chunks:

```bash
# Split 5GB file into 50MB chunks
split -b 50M large_file.iso large_file_part_

# Encrypt each chunk separately
# Result: large_file_part_aa.png, large_file_part_ab.png, etc.

# Decrypt each chunk
# Reassemble:
cat large_file_part_* > large_file.iso
```

**Benefits:**
- ✅ Works with current ColorCrypt implementation
- ✅ Manageable file sizes
- ✅ Can process chunks in parallel
- ✅ Partial file recovery possible

**Implementation Strategy:**
```python
# Future enhancement: Add to ColorCrypt
def encrypt_large_file_chunked(input_file, output_dir, chunk_size=50MB):
    """Split file into chunks and encrypt each separately"""
    chunks = split_file(input_file, chunk_size)
    encrypted_chunks = []
    
    for i, chunk in enumerate(chunks):
        output = f"{output_dir}/chunk_{i:04d}_encrypted.png"
        ColorCrypt.encrypt_file_to_image(chunk, output, password)
        encrypted_chunks.append(output)
    
    return encrypted_chunks
```

#### 3. **Streaming/Chunked Processing (Advanced)**
Process files in chunks without loading entirely into memory:

**Benefits:**
- ✅ Constant memory usage regardless of file size
- ✅ Can handle multi-GB files
- ✅ More efficient

**Challenges:**
- ⚠️ Requires significant code refactoring
- ⚠️ PNG format isn't designed for streaming
- ⚠️ Need custom file format or multiple images

**Potential Implementation:**
```python
# Conceptual - requires ColorCrypt redesign
def stream_encrypt(input_file, output_file, chunk_size=4MB):
    """Process large files in memory-efficient chunks"""
    with open(input_file, 'rb') as f_in:
        while chunk := f_in.read(chunk_size):
            encrypted_chunk = encrypt_chunk(chunk)
            write_to_image(encrypted_chunk, output_file)
```

#### 4. **Alternative Storage Formats (Future Enhancement)**
Instead of single PNG, use multi-image approach:

**Option A: Image Gallery**
- Split data across multiple PNGs (e.g., 100MB per image)
- Create manifest file listing all images
- Encrypt: `large_file_001.png`, `large_file_002.png`, etc.

**Option B: Custom Container Format**
- Create `.colorcrypt` container
- Contains multiple compressed image chunks
- Metadata for reassembly

#### 5. **Database/Cloud Hybrid (Enterprise)**
For truly massive files:
- Store file chunks in cloud storage (S3, Azure Blob)
- Encrypt chunks individually
- Store manifest in database
- Download/decrypt on demand

### Recommended Approach by File Size

| File Size | Recommended Strategy | Rationale |
|-----------|---------------------|-----------|
| < 50MB | Direct encryption | Works perfectly with default settings |
| 50-200MB | Increase limits or compress | Manageable with adequate RAM |
| 200MB-1GB | Pre-compress + encrypt | Reduces output size significantly |
| 1GB-5GB | File splitting (50-100MB chunks) | Most practical with current architecture |
| 5GB-20GB | Compression + splitting | Combines both strategies |
| > 20GB | Reconsider use case | ColorCrypt not designed for this scale; use specialized tools |

### Practical Example: Encrypting a 5GB File

**Current limitation:** Direct encryption would fail or require ~10GB RAM

**Solution 1: Split and Encrypt**
```bash
# Split into 50MB chunks (creates 100 files)
split -b 50M movie.mp4 movie_chunk_

# Encrypt each chunk with a script
for file in movie_chunk_*; do
    python -c "from colorcrypt import ColorCrypt; ColorCrypt.encrypt_file_to_image('$file', '${file}_encrypted.png', 'password')"
done

# To decrypt and reassemble:
for file in movie_chunk_*_encrypted.png; do
    python -c "from colorcrypt import ColorCrypt; ColorCrypt.decrypt_image_to_file('$file', '.', 'password')"
done
cat movie_chunk_* > movie_restored.mp4
```

**Solution 2: Compress First (for compressible files)**
```bash
# Compress 5GB text/document file (might become 500MB-1GB)
tar -czf documents.tar.gz documents_folder/

# Now encrypt the compressed file (much more manageable)
python -c "from colorcrypt import ColorCrypt; ColorCrypt.encrypt_file_to_image('documents.tar.gz', 'documents_encrypted.png', 'password')"
```

### Why PNG Has Size Limitations

1. **Image Dimensions:** Max practical PNG size is ~65,000 x 65,000 pixels
   - 65,000² pixels × 4 bytes (RGBA) = ~16GB theoretical max
   - But memory constraints make this impractical

2. **Memory Requirements:** 
   - PIL/Pillow loads entire image into RAM
   - Processing overhead doubles memory usage
   - 5GB input → 10GB+ RAM needed

3. **Processing Time:**
   - Creating massive images is CPU-intensive
   - Encoding/decoding PNG is slow for huge files

### Future Enhancements (Roadmap)

**Phase 1: Automatic Chunking (Easiest)**
- Auto-split files over threshold
- Encrypt each chunk
- Create manifest file
- Auto-reassemble on decrypt

**Phase 2: Built-in Compression**
- Compress before encryption
- Transparent to user
- Auto-detect compressible files

**Phase 3: Streaming Architecture**
- Redesign core engine for chunk-based processing
- Constant memory usage
- Support unlimited file sizes

**Phase 4: Progressive Encryption**
- Encrypt while uploading
- Real-time progress tracking
- Cancellable operations

### For Production Use

**If you need to handle large files regularly:**

1. **Increase server resources:**
   - RAM: 8GB+ recommended for files up to 1GB
   - CPU: Multi-core for parallel chunk processing
   - Storage: SSD for better I/O performance

2. **Implement file splitting in your workflow:**
   - Pre-process large files into chunks
   - Encrypt chunks in parallel
   - Store chunks with metadata for reassembly

3. **Set appropriate limits in config.py:**
   ```python
   # Example for server with 16GB RAM
   MAX_INPUT_FILE_SIZE = 200 * 1024 * 1024   # 200 MB
   MAX_OUTPUT_FILE_SIZE = 400 * 1024 * 1024  # 400 MB
   ```

4. **Monitor server resources:**
   - Track memory usage during encryption
   - Implement timeout limits
   - Add queue system for large files

### For High-Performance Systems (Generous)
```python
MAX_INPUT_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
MAX_OUTPUT_FILE_SIZE = 200 * 1024 * 1024 # 200 MB
MAX_FILES_PER_BATCH = 20
```

## Troubleshooting

**Q: Files are rejected even though they're smaller than the limit**
A: The encrypted output might exceed `MAX_OUTPUT_FILE_SIZE`. Try increasing it or compressing your input file.

**Q: Limits don't appear in the UI**
A: Check browser console for errors. Ensure `/api/limits` endpoint is accessible.

**Q: Want different limits for different users**
A: Currently, limits are global. You would need to implement user-specific limits in `app.py`.

**Q: Getting 413 errors**
A: This is Flask's built-in limit. Ensure `MAX_CONTENT_LENGTH` in config.py is set appropriately.
