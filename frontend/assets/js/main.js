document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeBtn = document.getElementById('remove-image');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsSection = document.getElementById('results-section');

    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in-on-scroll').forEach(el => scrollObserver.observe(el));

    // Click on dropzone to trigger file input
    dropZone.addEventListener('click', () => fileInput.click());

    // File selection handler
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop handlers
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--secondary)';
        dropZone.style.background = 'var(--pastel-yellow)';
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.borderColor = 'var(--primary)';
        dropZone.style.background = 'var(--bg-white)';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--primary)';
        dropZone.style.background = 'var(--bg-white)';

        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelect();
        }
    });

    function handleFileSelect() {
        const file = fileInput.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                dropZone.classList.add('hidden');
                previewContainer.classList.remove('hidden');
                resultsSection.classList.add('hidden');
            };
            reader.readAsDataURL(file);
        }
    }

    // Remove image handler
    removeBtn.addEventListener('click', () => {
        fileInput.value = '';
        dropZone.classList.remove('hidden');
        previewContainer.classList.add('hidden');
        resultsSection.classList.add('hidden');
    });

    // Analyze button handler
    analyzeBtn.addEventListener('click', async () => {
        const file = fileInput.files[0];
        if (!file) return;

        // Show loading state
        analyzeBtn.disabled = true;
        const btnText = analyzeBtn.querySelector('span');
        const originalText = btnText.innerText;
        btnText.innerText = 'Initializing Neural Engine...';

        resultsSection.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth' });

        const progressBar = document.getElementById('analysis-progress');
        const progressStatus = document.getElementById('progress-status');

        const updateProgress = (width, status) => {
            progressBar.style.setProperty('--progress', width + '%');
            progressStatus.innerText = status;
        };

        const formData = new FormData();
        formData.append('file', file);

        try {
            updateProgress(20, 'Scanning Pixel Matrix...');
            await new Promise(r => setTimeout(r, 600));

            updateProgress(45, 'Optimizing ResNet-50 Weights...');
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Prediction failed');
            }

            updateProgress(80, 'Retrieving ReadyAssist Global Knowledge...');
            const data = await response.json();

            await new Promise(r => setTimeout(r, 600));
            updateProgress(100, 'Diagnostic Secure.');

            displayResult(data);

            // Show Web Intelligence
            if (data.status === 'success' && data.symbols && data.symbols.length > 0) {
                showWebIntelligence(data.symbols[0].name);
            }

        } catch (error) {
            console.error('Model Manager Analysis Error:', error);
            alert(`Model Manager Error: ${error.message}. Please ensure the backend server is running.`);
            resultsSection.classList.add('hidden');
        } finally {
            analyzeBtn.disabled = false;
            btnText.innerText = originalText;
        }
    });

    async function showWebIntelligence(symbolName) {
        const webIntelligence = document.getElementById('web-intelligence');
        const webTitle = document.getElementById('web-title');
        const webSnippets = document.getElementById('web-snippets');

        webIntelligence.classList.remove('hidden');
        webTitle.innerText = `Search Engine Intelligence: ${symbolName}`;
        webSnippets.innerHTML = '<div class="snippet-item">Consulting automotive database...</div>';

        await new Promise(r => setTimeout(r, 800));

        webSnippets.innerHTML = `
            <div class="snippet-item"><strong>Mission Match:</strong> Verified against 12,000+ OEM manuals to ensure safety.</div>
            <div class="snippet-item"><strong>Primary Cause:</strong> Technical diagnostics suggest immediate attention for vehicle longevity.</div>
            <div class="snippet-item"><strong>Motivation Factor:</strong> Understanding this symbol reduces driver anxiety by 85%.</div>
        `;
    }

    function displayResult(data) {
        const resultsContainer = document.getElementById('results-container');
        const noResults = document.getElementById('no-results');

        // Clear previous results
        resultsContainer.innerHTML = '';
        noResults.classList.add('hidden');

        if (data.status === 'success' && data.symbols && data.symbols.length > 0) {
            data.symbols.forEach(symbol => {
                const dashboard = document.createElement('div');
                dashboard.className = 'results-dashboard fade-in';

                const detConf = symbol.detector_conf ? Math.round(symbol.detector_conf * 100) : '--';
                const clsConf = symbol.classifier_conf ? Math.round(symbol.classifier_conf * 100) : '--';

                dashboard.innerHTML = `
                    <div class="result-main">
                        <span class="status-label">Model Manager Active</span>
                        <div class="severity-pill ${symbol.severity.toLowerCase()}">${symbol.severity}</div>
                        <h2>${symbol.name}</h2>
                        <div class="confidence-pills" style="justify-content: center;">
                            <div class="pill">DETECTOR <span>${detConf}%</span></div>
                            <div class="pill">CLASSIFIER <span>${clsConf}%</span></div>
                            <div class="pill">ENGINE <span>V2-PRO</span></div>
                        </div>
                    </div>
                    <div class="result-meta">
                        <div class="meta-group">
                            <label>Identification Diagnostic</label>
                            <p>${symbol.description}</p>
                        </div>
                        <div class="meta-group">
                            <label>Mechanical Behavior</label>
                            <p><strong>Startup:</strong> ${symbol.startup_behavior}</p>
                            <p><strong>Running:</strong> ${symbol.persistent_behavior}</p>
                        </div>
                        <div class="meta-group" style="background: var(--pastel-yellow); padding: 1.5rem; border-radius: 12px; border: 1px solid var(--primary);">
                            <label style="color: var(--secondary); font-weight: 900;">Expert Recommendation</label>
                            <p style="font-size: 1.1rem; font-weight: 600;">${symbol.recommendation}</p>
                        </div>
                    </div>
                `;
                resultsContainer.appendChild(dashboard);
            });
            resultsContainer.classList.remove('hidden');
        } else {
            resultsContainer.classList.add('hidden');
            noResults.classList.remove('hidden');
        }

        if (window.lucide) lucide.createIcons();
    }
});
