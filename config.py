"""
ColorCrypt Configuration
Centralized configuration for file size limits and application settings

=== QUICK START: CONFIGURE YOUR CHUNK SIZE ===
NO FILE SIZE LIMITS - Encrypt files of ANY size!

Want to change how files are split? 
Edit CHUNK_SIZE below (default: 500 MB per chunk)

Examples:
- Smaller chunks (more files):   CHUNK_SIZE = 250 * 1024 * 1024   # 250 MB
- Larger chunks (fewer files):   CHUNK_SIZE = 1024 * 1024 * 1024  # 1 GB  
- Very large chunks:             CHUNK_SIZE = 2048 * 1024 * 1024  # 2 GB

Your 5GB file will be split into:
- 500 MB chunks = 10 files
- 250 MB chunks = 20 files  
- 1 GB chunks = 5 files

Maximum file size = CHUNK_SIZE × MAX_CHUNKS
Default: 500MB × 1000 = 500GB (increase MAX_CHUNKS for bigger files!)

==============================================
"""

# Automatic file chunking - CONFIGURE YOUR CHUNK SIZE HERE
ENABLE_AUTO_CHUNKING = True  # Automatically split large files into chunks
CHUNK_SIZE = 500 * 1024 * 1024  # 500 MB per chunk (USER CONFIGURABLE - set your preferred size!)
MAX_CHUNKS = 1000  # Maximum number of chunks per file (1000 chunks × 500MB = 500GB max)

# Upload Limits (per HTTP request)
# Set high enough to allow large files before server-side chunking
# Flask streams files to disk, so this doesn't consume RAM
MAX_CONTENT_LENGTH = 20 * 1024 * 1024 * 1024  # 20GB - allows files up to 20GB before chunking

# Bulk upload limits
MAX_FILES_PER_BATCH = 10  # Maximum number of files in a single bulk upload
MAX_BULK_TOTAL_SIZE = 200 * 1024 * 1024  # 200 MB total for all files in bulk upload


def format_size(size_bytes):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def get_limits_info():
    """Get formatted information about current limits."""
    return {
        'max_files_per_batch': MAX_FILES_PER_BATCH,
        'max_bulk_total_size': MAX_BULK_TOTAL_SIZE,
        'max_bulk_total_size_formatted': format_size(MAX_BULK_TOTAL_SIZE),
        'enable_auto_chunking': ENABLE_AUTO_CHUNKING,
        'chunk_size': CHUNK_SIZE,
        'chunk_size_formatted': format_size(CHUNK_SIZE),
        'max_chunks': MAX_CHUNKS
    }
