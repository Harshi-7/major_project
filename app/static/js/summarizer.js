// summarizer.js - Summarization functionality

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const inputText = document.getElementById('inputText');
    const charCount = document.getElementById('charCount');
    const summarizeBtn = document.getElementById('summarizeBtn');
    const outputArea = document.getElementById('outputArea');
    const summaryOutput = document.getElementById('summaryOutput');
    const errorArea = document.getElementById('errorArea');
    const errorMessage = document.getElementById('errorMessage');
    const clearBtn = document.getElementById('clearBtn');
    const sampleBtn = document.getElementById('sampleBtn');
    const copyBtn = document.getElementById('copyBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const compressionRatio = document.getElementById('compressionRatio');
    const processingTime = document.getElementById('processingTime');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');
    const modelSelect = document.getElementById('modelSelect');

    // Sample legal text
    const SAMPLE_TEXT = `The plaintiff, John Doe, hereby files this complaint against the defendant, XYZ Corporation, for breach of contract and negligence. The plaintiff alleges that on or about January 15, 2023, the defendant entered into a written agreement with the plaintiff to provide consulting services. The defendant failed to perform their obligations under said agreement, causing damages in the amount of $500,000. The plaintiff seeks compensatory damages, legal fees, and any other relief the court deems proper.`;

    // Character count update
    if (inputText) {
        inputText.addEventListener('input', function() {
            const count = this.value.length;
            charCount.textContent = count;
        });
    }

    // Tab switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tab = this.dataset.tab;
            
            tabBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === tab + '-tab') {
                    content.classList.add('active');
                }
            });
        });
    });

    // Clear button
    if (clearBtn && inputText) {
        clearBtn.addEventListener('click', function() {
            inputText.value = '';
            charCount.textContent = '0';
            outputArea.style.display = 'none';
            errorArea.style.display = 'none';
        });
    }

    // Sample button
    if (sampleBtn && inputText) {
        sampleBtn.addEventListener('click', function() {
            inputText.value = SAMPLE_TEXT;
            charCount.textContent = SAMPLE_TEXT.length;
            outputArea.style.display = 'none';
            errorArea.style.display = 'none';
            
            // Switch to paste tab
            document.querySelector('[data-tab="paste"]').click();
        });
    }

    // File upload handling
    if (dropArea && fileInput) {
        dropArea.addEventListener('click', () => {
            fileInput.click();
        });

        dropArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropArea.style.borderColor = 'var(--primary-500)';
            dropArea.style.background = 'linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(59, 130, 246, 0.1))';
        });

        dropArea.addEventListener('dragleave', () => {
            dropArea.style.borderColor = 'var(--border-color)';
            dropArea.style.background = 'var(--bg-primary)';
        });

        dropArea.addEventListener('drop', (e) => {
            e.preventDefault();
            dropArea.style.borderColor = 'var(--border-color)';
            dropArea.style.background = 'var(--bg-primary)';
            
            const file = e.dataTransfer.files[0];
            handleFileUpload(file);
        });

        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            handleFileUpload(file);
        });
    }

    function handleFileUpload(file) {
        if (!file) return;
        
        const reader = new FileReader();
        reader.onload = function(e) {
            if (inputText) {
                inputText.value = e.target.result;
                charCount.textContent = e.target.result.length;
                document.querySelector('[data-tab="paste"]').click();
            }
        };
        reader.readAsText(file);
    }

    // Summarize button
    if (summarizeBtn) {
        summarizeBtn.addEventListener('click', async function() {
            const text = inputText ? inputText.value.trim() : '';
            
            if (!text) {
                showError('Please enter some text to summarize.');
                return;
            }
            
            if (text.length < 100) {
                showError('Text must be at least 100 characters long.');
                return;
            }

            showLoading(summarizeBtn);
            outputArea.style.display = 'none';
            errorArea.style.display = 'none';

            const startTime = Date.now();

            try {
                const response = await fetch('/summarize', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        text: text,
                        model: modelSelect ? modelSelect.value : 'bart'
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    const endTime = Date.now();
                    const timeInSeconds = ((endTime - startTime) / 1000).toFixed(1);
                    
                    const originalLength = text.length;
                    const summaryLength = data.summary.length;
                    const ratio = ((1 - summaryLength / originalLength) * 100).toFixed(1);
                    
                    summaryOutput.innerHTML = data.summary;
                    compressionRatio.textContent = ratio + '%';
                    processingTime.textContent = timeInSeconds + 's';
                    outputArea.style.display = 'block';
                } else {
                    showError(data.error || 'An error occurred while generating summary.');
                }
            } catch (error) {
                showError('Network error. Please check your connection.');
            } finally {
                hideLoading(summarizeBtn);
            }
        });
    }

    // Copy button
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            const summary = summaryOutput.innerText;
            navigator.clipboard.writeText(summary).then(() => {
                const originalHTML = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    this.innerHTML = originalHTML;
                }, 2000);
            });
        });
    }

    // Download button
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            const summary = summaryOutput.innerText;
            const blob = new Blob([summary], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'summary.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        });
    }

    function showError(message) {
        if (errorArea && errorMessage) {
            errorMessage.textContent = message;
            errorArea.style.display = 'flex';
            outputArea.style.display = 'none';
        }
    }

    // Keyboard shortcut (Ctrl+Enter)
    if (inputText) {
        inputText.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                summarizeBtn.click();
            }
        });
    }

    // Auto-resize textarea
    if (inputText) {
        inputText.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }
});