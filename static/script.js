// ColorCrypt - Client-side JavaScript with bulk upload and password support

let selectedFiles = [];
let downloadUrls = {};
let fileSizeLimits = {
    max_input_size: 50 * 1024 * 1024,
    max_output_size: 100 * 1024 * 1024,
    max_files_per_batch: 10,
    max_bulk_total_size: 200 * 1024 * 1024
};

document.addEventListener('DOMContentLoaded', function() {
    // Fetch file size limits from server
    fetchFileSizeLimits();
    
    // Theme toggle
    setupThemeToggle();
    
    // Tab switching
    setupTabs();
    
    // Password visibility toggles
    setupPasswordToggles();
    
    // Encrypt functionality
    setupEncryptTab();
    
    // Decrypt functionality
    setupDecryptTab();
});

async function fetchFileSizeLimits() {
    try {
        const response = await fetch('/api/limits');
        if (response.ok) {
            fileSizeLimits = await response.json();
            updateLimitsDisplay();
        }
    } catch (error) {
        console.error('Failed to fetch file size limits:', error);
    }
}

function updateLimitsDisplay() {
    const limitsInfo = document.getElementById('encrypt-limits-info');
    if (limitsInfo) {
        if (fileSizeLimits.enable_auto_chunking) {
            const maxSize = (fileSizeLimits.chunk_size * fileSizeLimits.max_chunks) / (1024 * 1024 * 1024);
            limitsInfo.innerHTML = `Files auto-split into ${fileSizeLimits.chunk_size_formatted} chunks • No file size limit (up to ${maxSize.toFixed(0)}GB)`;
        } else {
            limitsInfo.innerHTML = `Chunking disabled • Max ${fileSizeLimits.max_files_per_batch} files per batch`;
        }
    }
}

function setupThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    const savedTheme = localStorage.getItem('theme') || 'dark';
    
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
        themeToggle.querySelector('i').classList.replace('fa-sun', 'fa-moon');
    }
    
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('light-theme');
        const isLight = document.body.classList.contains('light-theme');
        const icon = themeToggle.querySelector('i');
        
        if (isLight) {
            icon.classList.replace('fa-sun', 'fa-moon');
            localStorage.setItem('theme', 'light');
        } else {
            icon.classList.replace('fa-moon', 'fa-sun');
            localStorage.setItem('theme', 'dark');
        }
    });
}

function setupTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');
            
            resetTab(tabName);
        });
    });
}

function setupPasswordToggles() {
    document.querySelectorAll('.toggle-password').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.dataset.target;
            const input = document.getElementById(targetId);
            const icon = btn.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.replace('fa-eye', 'fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.replace('fa-eye-slash', 'fa-eye');
            }
        });
    });
}

function setupEncryptTab() {
    const uploadArea = document.getElementById('encrypt-upload');
    const fileInput = document.getElementById('encrypt-file-input');
    const usePasswordCheckbox = document.getElementById('encrypt-use-password');
    const passwordGroup = document.getElementById('encrypt-password-group');
    const bulkOption = document.getElementById('encrypt-bulk-option');
    const filesList = document.getElementById('encrypt-files-list');
    const resetBtn = document.getElementById('encrypt-reset-btn');
    
    // Password checkbox toggle
    usePasswordCheckbox.addEventListener('change', () => {
        if (usePasswordCheckbox.checked) {
            passwordGroup.classList.remove('hidden');
            if (selectedFiles.length > 1) {
                bulkOption.classList.remove('hidden');
            }
        } else {
            passwordGroup.classList.add('hidden');
            bulkOption.classList.add('hidden');
        }
    });
    
    // Click to upload
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        handleFileSelection(e.dataTransfer.files);
    });
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        handleFileSelection(e.target.files);
    });
    
    // Reset button
    resetBtn.addEventListener('click', () => {
        resetTab('encrypt');
    });
    
    function handleFileSelection(files) {
        selectedFiles = Array.from(files);
        
        if (selectedFiles.length === 0) return;
        
        // Validate number of files
        if (selectedFiles.length > fileSizeLimits.max_files_per_batch) {
            showError('encrypt', `Too many files selected. Maximum ${fileSizeLimits.max_files_per_batch} files per batch.`);            selectedFiles = [];
            return;
        }
        
        // If auto-chunking is enabled, skip size validation (will be handled server-side)
        if (!fileSizeLimits.enable_auto_chunking) {
            // Validate individual file sizes
            const oversizedFiles = selectedFiles.filter(file => file.size > fileSizeLimits.max_input_size);
            if (oversizedFiles.length > 0) {
                const fileNames = oversizedFiles.map(f => f.name).join(', ');
                showError('encrypt', `File(s) too large: ${fileNames}. Maximum input file size is ${fileSizeLimits.max_input_size_formatted}.`);
                selectedFiles = [];
                return;
            }
            
            // Validate total size for bulk uploads
            const totalSize = selectedFiles.reduce((sum, file) => sum + file.size, 0);
            if (selectedFiles.length > 1 && totalSize > fileSizeLimits.max_bulk_total_size) {
                showError('encrypt', `Total file size exceeds limit. Maximum ${fileSizeLimits.max_bulk_total_size_formatted} for bulk upload.`);
                selectedFiles = [];
                return;
            }
        }
        
        // Show files list
        displayFilesList();
        
        // Show bulk option if multiple files and password enabled
        if (selectedFiles.length > 1 && usePasswordCheckbox.checked) {
            bulkOption.classList.remove('hidden');
        }
        
        // Show process button
        createProcessButton();
    }
    
    function displayFilesList() {
        const filesList = document.getElementById('encrypt-files-list');
        const useIndividual = document.querySelector('input[name="password-mode"]:checked')?.value === 'individual';
        const usePassword = usePasswordCheckbox.checked;
        
        filesList.innerHTML = selectedFiles.map((file, idx) => `
            <div class="file-item" data-idx="${idx}">
                <div class="file-info">
                    <i class="fas fa-file"></i>
                    <span class="file-name">${file.name} (${formatFileSize(file.size)})</span>
                </div>
                ${usePassword && useIndividual ? 
                    `<input type="password" class="file-password-input" placeholder="Password" data-idx="${idx}">` : 
                    ''}
                <button class="file-remove" onclick="removeFile(${idx})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `).join('');
        
        filesList.classList.remove('hidden');
        document.getElementById('encrypt-upload').classList.add('hidden');
    }
    
    function createProcessButton() {
        const existing = document.getElementById('process-btn');
        if (existing) existing.remove();
        
        const btn = document.createElement('button');
        btn.id = 'process-btn';
        btn.className = 'btn btn-primary process-files-btn';
        btn.innerHTML = `<i class="fas fa-lock"></i> Encrypt ${selectedFiles.length} File${selectedFiles.length > 1 ? 's' : ''}`;
        btn.onclick = processEncryption;
        
        document.getElementById('encrypt-files-list').appendChild(btn);
    }
    
    // Radio button change listener
    document.querySelectorAll('input[name="password-mode"]').forEach(radio => {
        radio.addEventListener('change', () => {
            if (selectedFiles.length > 0) {
                displayFilesList();
            }
        });
    });
}

window.removeFile = function(idx) {
    selectedFiles.splice(idx, 1);
    
    if (selectedFiles.length === 0) {
        resetTab('encrypt');
    } else {
        const filesList = document.getElementById('encrypt-files-list');
        const useIndividual = document.querySelector('input[name="password-mode"]:checked')?.value === 'individual';
        const usePassword = document.getElementById('encrypt-use-password').checked;
        
        filesList.innerHTML = selectedFiles.map((file, newIdx) => `
            <div class="file-item" data-idx="${newIdx}">
                <div class="file-info">
                    <i class="fas fa-file"></i>
                    <span class="file-name">${file.name} (${formatFileSize(file.size)})</span>
                </div>
                ${usePassword && useIndividual ? 
                    `<input type="password" class="file-password-input" placeholder="Password" data-idx="${newIdx}">` : 
                    ''}
                <button class="file-remove" onclick="removeFile(${newIdx})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `).join('');
        
        const btn = document.createElement('button');
        btn.id = 'process-btn';
        btn.className = 'btn btn-primary process-files-btn';
        btn.innerHTML = `<i class="fas fa-lock"></i> Encrypt ${selectedFiles.length} File${selectedFiles.length > 1 ? 's' : ''}`;
        btn.onclick = processEncryption;
        filesList.appendChild(btn);
        
        // Hide bulk option if only one file left
        if (selectedFiles.length === 1) {
            document.getElementById('encrypt-bulk-option').classList.add('hidden');
        }
    }
};

function processEncryption() {
    const filesList = document.getElementById('encrypt-files-list');
    const loadingArea = document.getElementById('encrypt-loading');
    const errorBox = document.getElementById('encrypt-error');
    const resultArea = document.getElementById('encrypt-result');
    
    filesList.classList.add('hidden');
    errorBox.classList.add('hidden');
    resultArea.classList.add('hidden');
    loadingArea.classList.remove('hidden');
    
    const formData = new FormData();
    const usePassword = document.getElementById('encrypt-use-password').checked;
    const useIndividual = document.querySelector('input[name="password-mode"]:checked')?.value === 'individual';
    
    // Add files
    selectedFiles.forEach(file => {
        formData.append('files', file);
    });
    
    // Add password(s)
    if (usePassword) {
        if (useIndividual) {
            formData.append('use_individual_passwords', 'true');
            document.querySelectorAll('.file-password-input').forEach((input, idx) => {
                formData.append(`password_${idx}`, input.value);
            });
        } else {
            const password = document.getElementById('encrypt-password').value;
            formData.append('password', password);
        }
    }
    
    fetch('/encrypt', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        loadingArea.classList.add('hidden');
        
        if (data.error) {
            showError('encrypt', data.error);
            filesList.classList.remove('hidden');
        } else {
            showEncryptResult(data);
        }
    })
    .catch(error => {
        loadingArea.classList.add('hidden');
        console.error('Encryption error:', error);
        showError('encrypt', 'An error occurred: ' + error.message + '. Please check console for details.');
        filesList.classList.remove('hidden');
    });
}

function showEncryptResult(data) {
    const resultArea = document.getElementById('encrypt-result');
    const resultContent = document.getElementById('encrypt-result-content');
    
    if (data.bulk) {
        // Multiple files
        resultContent.innerHTML = data.files.map(file => {
            if (file.is_chunked) {
                // Chunked file
                return `
                    <div class="result-file chunked-file">
                        <div class="result-file-name">📄 ${file.original_name}</div>
                        <div class="result-file-size">📦 Original Size: ${formatFileSize(file.original_size)}</div>
                        <div class="chunk-info"><i class="fas fa-puzzle-piece"></i> Split into ${file.total_chunks} chunks</div>
                        ${file.protected ? '<div class="result-file-protected"><i class="fas fa-lock"></i> Password Protected</div>' : ''}
                        ${file.chunks.map(chunk => `
                            <button class="btn btn-secondary btn-sm chunk-download" onclick="downloadFile('${chunk.download_url}', '${chunk.filename}')">
                                <i class="fas fa-download"></i> Chunk ${chunk.chunk_number + 1}
                            </button>
                        `).join('')}
                        <button class="btn btn-primary btn-sm download-all-chunks" onclick="downloadAllChunks(${JSON.stringify(file.chunks).replace(/"/g, '&quot;')})">
                            <i class="fas fa-download"></i> Download All Chunks
                        </button>
                    </div>
                `;
            } else {
                // Regular file
                return `
                    <div class="result-file">
                        <div class="result-file-name">📄 ${file.filename}</div>
                        <div class="result-file-size">📦 Size: ${formatFileSize(file.size)}</div>
                        ${file.protected ? '<div class="result-file-protected"><i class="fas fa-lock"></i> Password Protected</div>' : ''}
                        <button class="btn btn-primary btn-sm" onclick="downloadFile('${file.download_url}', '${file.filename}')">
                            <i class="fas fa-download"></i> Download
                        </button>
                    </div>
                `;
            }
        }).join('');
    } else if (data.is_chunked) {
        // Single chunked file
        resultContent.innerHTML = `
            <div class="result-file chunked-file">
                <div class="result-file-name">📄 ${data.original_name}</div>
                <div class="result-file-size">📦 Original Size: ${formatFileSize(data.original_size)}</div>
                <div class="chunk-info"><i class="fas fa-puzzle-piece"></i> Split into ${data.total_chunks} chunks</div>
                ${data.protected ? '<div class="result-file-protected"><i class="fas fa-lock"></i> Password Protected</div>' : ''}
                ${data.chunks.map(chunk => `
                    <button class="btn btn-secondary btn-sm chunk-download" onclick="downloadFile('${chunk.download_url}', '${chunk.filename}')">
                        <i class="fas fa-download"></i> Chunk ${chunk.chunk_number + 1}
                    </button>
                `).join('')}
                <button class="btn btn-primary download-all-chunks" onclick="downloadAllChunks(${JSON.stringify(data.chunks).replace(/"/g, '&quot;')})">
                    <i class="fas fa-download"></i> Download All Chunks
                </button>
            </div>
        `;
    } else {
        // Single file
        resultContent.innerHTML = `
            <div class="result-file">
                <div class="result-file-name">📄 ${data.filename}</div>
                <div class="result-file-size">📦 Size: ${formatFileSize(data.size)}</div>
                ${data.protected ? '<div class="result-file-protected"><i class="fas fa-lock"></i> Password Protected</div>' : ''}
                <button class="btn btn-primary" onclick="downloadFile('${data.download_url}', '${data.filename}')">
                    <i class="fas fa-download"></i> Download PNG
                </button>
            </div>
        `;
    }
    
    resultArea.classList.remove('hidden');
}

function setupDecryptTab() {
    const uploadArea = document.getElementById('decrypt-upload');
    const fileInput = document.getElementById('decrypt-file-input');
    const downloadBtn = document.getElementById('decrypt-download-btn');
    const resetBtn = document.getElementById('decrypt-reset-btn');
    
    uploadArea.addEventListener('click', () => fileInput.click());
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleDecryption(e.dataTransfer.files);
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleDecryption(e.target.files);
        }
    });
    
    resetBtn.addEventListener('click', () => resetTab('decrypt'));
    
    downloadBtn.addEventListener('click', () => {
        if (downloadUrls.decrypt) {
            window.location.href = downloadUrls.decrypt;
        }
    });
}

function handleDecryption(files) {
    const uploadArea = document.getElementById('decrypt-upload');
    const loadingArea = document.getElementById('decrypt-loading');
    const errorBox = document.getElementById('decrypt-error');
    const resultArea = document.getElementById('decrypt-result');
    const passwordGroup = document.getElementById('decrypt-password-group');
    
    uploadArea.classList.add('hidden');
    errorBox.classList.add('hidden');
    resultArea.classList.add('hidden');
    loadingArea.classList.remove('hidden');
    
    const formData = new FormData();
    const filesArray = Array.from(files);
    
    // Check if multiple files (chunks) or single file
    if (filesArray.length > 1) {
        // Multiple chunks
        filesArray.forEach(file => {
            formData.append('files', file);
        });
    } else {
        // Single file
        formData.append('file', filesArray[0]);
    }
    
    const password = document.getElementById('decrypt-password').value.trim();
    if (password) {
        formData.append('password', password);
    }
    
    fetch('/decrypt', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        loadingArea.classList.add('hidden');
        
        if (data.error) {
            if (data.requires_password) {
                showError('decrypt', data.error + ' Please enter the password above and try again.');
                passwordGroup.classList.add('highlight-password');
                setTimeout(() => passwordGroup.classList.remove('highlight-password'), 2000);
            } else {
                showError('decrypt', data.error);
            }
            uploadArea.classList.remove('hidden');
        } else {
            showDecryptResult(data);
        }
    })
    .catch(error => {
        loadingArea.classList.add('hidden');
        console.error('Decryption error:', error);
        showError('decrypt', 'An error occurred: ' + error.message + '. Please check console for details.');
        uploadArea.classList.remove('hidden');
    });
}

function showDecryptResult(data) {
    const resultArea = document.getElementById('decrypt-result');
    
    let filenameText = `📄 ${data.filename}`;
    let sizeText = `📦 Size: ${formatFileSize(data.size)}`;
    
    if (data.was_chunked) {
        filenameText += ` (Reassembled from ${data.chunks_count} chunks)`;
    }
    
    resultArea.querySelector('.result-filename').textContent = filenameText;
    resultArea.querySelector('.result-size').textContent = sizeText;
    
    downloadUrls.decrypt = data.download_url;
    
    resultArea.classList.remove('hidden');
}

function showError(mode, message) {
    const errorBox = document.getElementById(`${mode}-error`);
    errorBox.querySelector('.error-message').textContent = message;
    errorBox.classList.remove('hidden');
}

function resetTab(mode) {
    const uploadArea = document.getElementById(`${mode}-upload`);
    const resultArea = document.getElementById(`${mode}-result`);
    const loadingArea = document.getElementById(`${mode}-loading`);
    const errorBox = document.getElementById(`${mode}-error`);
    const fileInput = document.getElementById(`${mode}-file-input`);
    
    fileInput.value = '';
    
    uploadArea.classList.remove('hidden');
    resultArea.classList.add('hidden');
    loadingArea.classList.add('hidden');
    errorBox.classList.add('hidden');
    
    if (mode === 'encrypt') {
        selectedFiles = [];
        document.getElementById('encrypt-files-list').classList.add('hidden');
        document.getElementById('encrypt-files-list').innerHTML = '';
        document.getElementById('encrypt-password').value = '';
        document.getElementById('encrypt-use-password').checked = false;
        document.getElementById('encrypt-password-group').classList.add('hidden');
        document.getElementById('encrypt-bulk-option').classList.add('hidden');
    } else {
        document.getElementById('decrypt-password').value = '';
    }
    
    downloadUrls[mode] = '';
}

window.downloadFile = function(url, filename) {
    window.location.href = url;
};

window.downloadAllChunks = function(chunks) {
    // Download all chunks sequentially with delay
    chunks.forEach((chunk, index) => {
        setTimeout(() => {
            downloadFile(chunk.download_url, chunk.filename);
        }, index * 500); // 500ms delay between downloads
    });
};

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

