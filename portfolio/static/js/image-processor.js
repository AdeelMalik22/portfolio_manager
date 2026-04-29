/**
 * Portfolio Image Processor - JavaScript Client Library
 * Handles image upload, processing, and preview
 * Usage: Include this script and call PortfolioImageProcessor.processImage()
 */

class PortfolioImageProcessor {
    constructor(options = {}) {
        this.apiUrl = options.apiUrl || '/api/my-portfolio/process-image/';
        this.token = options.token || localStorage.getItem('access_token');
        this.onProgress = options.onProgress || (() => {});
        this.onSuccess = options.onSuccess || (() => {});
        this.onError = options.onError || (() => {});
    }

    /**
     * Process an image file
     * @param {File} imageFile - The image file to process
     * @param {string} templateSlug - Template slug (optional)
     * @returns {Promise}
     */
    async processImage(imageFile, templateSlug = 'modern_corporate') {
        if (!imageFile) {
            this.onError('No image file provided');
            throw new Error('No image file provided');
        }

        if (!imageFile.type.startsWith('image/')) {
            this.onError('Please select a valid image file');
            throw new Error('Invalid file type');
        }

        this.onProgress({ status: 'uploading', percent: 10 });

        try {
            const formData = new FormData();
            formData.append('image', imageFile);
            formData.append('template_slug', templateSlug);

            const response = await this._makeRequest(formData);

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Processing failed');
            }

            const data = await response.json();
            this.onProgress({ status: 'complete', percent: 100 });
            this.onSuccess(data);
            return data;
        } catch (error) {
            this.onError(error.message);
            throw error;
        }
    }

    /**
     * Process image from URL
     * @param {string} imageUrl - URL of image to process
     * @param {string} templateSlug - Template slug (optional)
     * @returns {Promise}
     */
    async processImageFromUrl(imageUrl, templateSlug = 'modern_corporate') {
        try {
            this.onProgress({ status: 'downloading', percent: 5 });

            const response = await fetch(imageUrl);
            const blob = await response.blob();
            const filename = imageUrl.split('/').pop() || 'image.jpg';
            const file = new File([blob], filename, { type: blob.type });

            return await this.processImage(file, templateSlug);
        } catch (error) {
            this.onError(`Failed to download image: ${error.message}`);
            throw error;
        }
    }

    /**
     * Make HTTP request
     * @private
     */
    async _makeRequest(formData) {
        const headers = {};

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        // CSRF token from meta tag if available
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content ||
                         document.querySelector('[name="csrfmiddlewaretoken"]')?.value;

        if (csrfToken) {
            headers['X-CSRFToken'] = csrfToken;
        }

        return fetch(this.apiUrl, {
            method: 'POST',
            headers: headers,
            body: formData
        });
    }

    /**
     * Get available templates
     * @returns {Promise<Array>}
     */
    static async getAvailableTemplates() {
        try {
            const response = await fetch('/api/templates/');
            if (!response.ok) throw new Error('Failed to fetch templates');
            const data = await response.json();
            return data.results || [];
        } catch (error) {
            console.error('Error fetching templates:', error);
            return [];
        }
    }

    /**
     * Preview image before processing
     * @param {File} imageFile
     * @param {HTMLImageElement} imgElement
     */
    static previewImage(imageFile, imgElement) {
        if (!imageFile) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            imgElement.src = e.target.result;
            imgElement.style.display = 'block';
        };
        reader.readAsDataURL(imageFile);
    }

    /**
     * Create a processing UI helper
     * @param {HTMLElement} container - Container element
     * @returns {Object} UI helper object
     */
    static createUI(container) {
        return {
            showLoading: () => {
                container.innerHTML = '<div class="loading-spinner"></div> Processing...';
            },
            showSuccess: (message) => {
                container.innerHTML = `<div class="alert alert-success">✓ ${message}</div>`;
            },
            showError: (message) => {
                container.innerHTML = `<div class="alert alert-error">✗ ${message}</div>`;
            },
            showProgress: (percent) => {
                container.innerHTML = `<div style="width: 100%; background: #e5e7eb; border-radius: 4px;">
                    <div style="width: ${percent}%; height: 4px; background: #10b981; transition: width 0.3s;"></div>
                </div>`;
            }
        };
    }
}

// Auto-initialize if data attributes are present
document.addEventListener('DOMContentLoaded', () => {
    const processorElements = document.querySelectorAll('[data-image-processor]');

    processorElements.forEach(element => {
        const apiUrl = element.getAttribute('data-api-url') || '/api/my-portfolio/process-image/';
        const inputSelector = element.getAttribute('data-input-selector');
        const templateSelector = element.getAttribute('data-template-selector');
        const previewSelector = element.getAttribute('data-preview-selector');

        if (!inputSelector) return;

        const processor = new PortfolioImageProcessor({ apiUrl });
        const inputEl = document.querySelector(inputSelector);

        if (inputEl) {
            inputEl.addEventListener('change', async (e) => {
                const file = e.target.files[0];
                if (!file) return;

                // Show preview
                if (previewSelector) {
                    const previewEl = document.querySelector(previewSelector);
                    PortfolioImageProcessor.previewImage(file, previewEl);
                }

                // Process button
                const processBtn = element.querySelector('.process-btn');
                if (processBtn) {
                    processBtn.addEventListener('click', async () => {
                        const templateSlug = templateSelector ?
                            document.querySelector(templateSelector).value :
                            'modern_corporate';

                        try {
                            await processor.processImage(file, templateSlug);
                        } catch (error) {
                            console.error('Processing error:', error);
                        }
                    });
                }
            });
        }
    });
});

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PortfolioImageProcessor;
}

