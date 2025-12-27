// ColorCrypt - Client-side JavaScript with bulk upload and password support

let selectedFiles = [];
let downloadUrls = {};

document.addEventListener('DOMContentLoaded', function() {
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
    .then(response => response.json())
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
        showError('encrypt', 'An error occurred. Please try again.');
        filesList.classList.remove('hidden');
    });
}

function showEncryptResult(data) {
    const resultArea = document.getElementById('encrypt-result');
    const resultContent = document.getElementById('encrypt-result-content');
    
    if (data.bulk) {
        // Multiple files
        resultContent.innerHTML = data.files.map(file => `
            <div class="result-file">
                <div class="result-file-name">📄 ${file.filename}</div>
                <div class="result-file-size">📦 Size: ${formatFileSize(file.size)}</div>
                ${file.protected ? '<div class="result-file-protected"><i class="fas fa-lock"></i> Password Protected</div>' : ''}
                <button class="btn btn-primary btn-sm" onclick="downloadFile('${file.download_url}', '${file.filename}')">
                    <i class="fas fa-download"></i> Download
                </button>
            </div>
        `).join('');
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
            handleDecryption(e.dataTransfer.files[0]);
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleDecryption(e.target.files[0]);
        }
    });
    
    resetBtn.addEventListener('click', () => resetTab('decrypt'));
    
    downloadBtn.addEventListener('click', () => {
        if (downloadUrls.decrypt) {
            window.location.href = downloadUrls.decrypt;
        }
    });
}

function handleDecryption(file) {
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
    formData.append('file', file);
    
    const password = document.getElementById('decrypt-password').value.trim();
    if (password) {
        formData.append('password', password);
    }
    
    fetch('/decrypt', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
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
        showError('decrypt', 'An error occurred. Please try again.');
        uploadArea.classList.remove('hidden');
    });
}

function showDecryptResult(data) {
    const resultArea = document.getElementById('decrypt-result');
    
    resultArea.querySelector('.result-filename').textContent = `📄 ${data.filename}`;
    resultArea.querySelector('.result-size').textContent = `📦 Size: ${formatFileSize(data.size)}`;
    
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

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}
