// ColorCrypt - Client-side JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            
            // Remove active class from all tabs and contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            btn.classList.add('active');
            document.getElementById(`${tabName}-tab`).classList.add('active');
            
            // Reset the tab content
            resetTab(tabName);
        });
    });
    
    // Encrypt functionality
    setupUploadArea('encrypt');
    
    // Decrypt functionality
    setupUploadArea('decrypt');
});

function setupUploadArea(mode) {
    const uploadArea = document.getElementById(`${mode}-upload`);
    const fileInput = document.getElementById(`${mode}-file-input`);
    const resultArea = document.getElementById(`${mode}-result`);
    const loadingArea = document.getElementById(`${mode}-loading`);
    const errorBox = document.getElementById(`${mode}-error`);
    const downloadBtn = document.getElementById(`${mode}-download-btn`);
    const resetBtn = document.getElementById(`${mode}-reset-btn`);
    
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
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0], mode);
        }
    });
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0], mode);
        }
    });
    
    // Reset button
    resetBtn.addEventListener('click', () => {
        resetTab(mode);
    });
    
    // Download button (will be set dynamically)
    let downloadUrl = '';
    downloadBtn.addEventListener('click', () => {
        if (downloadUrl) {
            window.location.href = downloadUrl;
        }
    });
    
    // Store download URL for access
    window[`${mode}DownloadUrl`] = '';
}

function handleFileUpload(file, mode) {
    const uploadArea = document.getElementById(`${mode}-upload`);
    const resultArea = document.getElementById(`${mode}-result`);
    const loadingArea = document.getElementById(`${mode}-loading`);
    const errorBox = document.getElementById(`${mode}-error`);
    
    // Validate file for decrypt mode
    if (mode === 'decrypt' && !file.name.toLowerCase().endsWith('.png')) {
        showError(mode, 'Please upload a PNG image file.');
        return;
    }
    
    // Hide upload area, show loading
    uploadArea.classList.add('hidden');
    errorBox.classList.add('hidden');
    resultArea.classList.add('hidden');
    loadingArea.classList.remove('hidden');
    
    // Create form data
    const formData = new FormData();
    formData.append('file', file);
    
    // Send to server
    fetch(`/${mode}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loadingArea.classList.add('hidden');
        
        if (data.error) {
            showError(mode, data.error);
            uploadArea.classList.remove('hidden');
        } else {
            showResult(mode, data);
        }
    })
    .catch(error => {
        loadingArea.classList.add('hidden');
        showError(mode, 'An error occurred. Please try again.');
        uploadArea.classList.remove('hidden');
    });
}

function showResult(mode, data) {
    const resultArea = document.getElementById(`${mode}-result`);
    const downloadBtn = document.getElementById(`${mode}-download-btn`);
    
    // Update result info
    resultArea.querySelector('.result-filename').textContent = `📄 ${data.filename}`;
    resultArea.querySelector('.result-size').textContent = `📦 Size: ${formatFileSize(data.size)}`;
    
    // Store download URL
    window[`${mode}DownloadUrl`] = data.download_url;
    
    // Show result
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
    
    // Reset file input
    fileInput.value = '';
    
    // Show upload area, hide others
    uploadArea.classList.remove('hidden');
    resultArea.classList.add('hidden');
    loadingArea.classList.add('hidden');
    errorBox.classList.add('hidden');
    
    // Clear download URL
    window[`${mode}DownloadUrl`] = '';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}
