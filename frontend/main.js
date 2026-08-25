/**
 * EDMAH - Main JavaScript File
 * Gestion des fonctionnalités communes et des appels AJAX
 */

// Configuration API
const API_CONFIG = {
    baseURL: '/api', // À remplacer par votre URL de backend
    endpoints: {
        newsletter: '/newsletter',
        contact: '/contact',
        register: '/register',
        formations: '/formations',
        events: '/events',
        blog: '/blog'
    }
};

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Affiche un message d'alerte
 */
function showAlert(message, type = 'success', duration = 5000) {
    const alertContainer = document.getElementById('alertContainer') || createAlertContainer();
    
    const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
    const icon = type === 'success' ? 'check-circle' : 'exclamation-circle';
    
    const alertHTML = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <i class="fas fa-${icon} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertContainer.innerHTML = alertHTML;
    
    if (duration > 0) {
        setTimeout(() => {
            alertContainer.innerHTML = '';
        }, duration);
    }
}

/**
 * Crée un conteneur d'alertes si nécessaire
 */
function createAlertContainer() {
    const container = document.createElement('div');
    container.id = 'alertContainer';
    container.style.cssText = 'position: fixed; top: 100px; right: 20px; z-index: 9999; max-width: 400px;';
    document.body.appendChild(container);
    return container;
}

/**
 * Valide une adresse email
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Formate la taille d'un fichier
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Valide un fichier uploadé
 */
function validateFile(file, maxSize, allowedTypes) {
    if (file.size > maxSize) {
        return {
            valid: false,
            error: `Le fichier ${file.name} dépasse la taille maximale de ${formatFileSize(maxSize)}`
        };
    }
    
    if (allowedTypes && !allowedTypes.includes(file.type)) {
        return {
            valid: false,
            error: `Le type de fichier ${file.name} n'est pas autorisé`
        };
    }
    
    return { valid: true };
}

/**
 * Smooth scroll vers un élément
 */
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// ============================================
// AJAX FUNCTIONS
// ============================================

/**
 * Newsletter Subscription
 */
async function subscribeNewsletter(email) {
    if (!validateEmail(email)) {
        throw new Error('Adresse email invalide');
    }
    
    const response = await fetch(`${API_CONFIG.baseURL}${API_CONFIG.endpoints.newsletter}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email })
    });
    
    if (!response.ok) {
        throw new Error('Erreur lors de l\'inscription à la newsletter');
    }
    
    return await response.json();
}

/**
 * Contact Form Submission
 */
async function submitContactForm(formData) {
    // Validation
    if (!formData.name || !formData.email || !formData.subject || !formData.message) {
        throw new Error('Tous les champs obligatoires doivent être remplis');
    }
    
    if (!validateEmail(formData.email)) {
        throw new Error('Adresse email invalide');
    }
    
    const response = await fetch(`${API_CONFIG.baseURL}${API_CONFIG.endpoints.contact}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    });
    
    if (!response.ok) {
        throw new Error('Erreur lors de l\'envoi du message');
    }
    
    return await response.json();
}

/**
 * Student Registration with File Upload
 */
async function submitRegistration(formData) {
    // FormData already contains all fields including files
    
    const response = await fetch(`${API_CONFIG.baseURL}${API_CONFIG.endpoints.register}`, {
        method: 'POST',
        body: formData // Don't set Content-Type, browser will set it with boundary
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Erreur lors de l\'inscription');
    }
    
    return await response.json();
}

/**
 * Load Formations List (AJAX)
 */
async function loadFormations(filters = {}) {
    const params = new URLSearchParams(filters);
    
    const response = await fetch(`${API_CONFIG.baseURL}${API_CONFIG.endpoints.formations}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    
    if (!response.ok) {
        throw new Error('Erreur lors du chargement des formations');
    }
    
    return await response.json();
}

/**
 * Load Events List (AJAX)
 */
async function loadEvents(filters = {}) {
    const params = new URLSearchParams(filters);
    
    const response = await fetch(`${API_CONFIG.baseURL}${API_CONFIG.endpoints.events}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    
    if (!response.ok) {
        throw new Error('Erreur lors du chargement des événements');
    }
    
    return await response.json();
}

/**
 * Load Blog Articles (AJAX with pagination)
 */
async function loadBlogArticles(page = 1, limit = 6) {
    const params = new URLSearchParams({ page, limit });
    
    const response = await fetch(`${API_CONFIG.baseURL}${API_CONFIG.endpoints.blog}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    
    if (!response.ok) {
        throw new Error('Erreur lors du chargement des articles');
    }
    
    return await response.json();
}

// ============================================
// DOM READY FUNCTIONS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar-custom');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
    
    // Scroll to top button
    const scrollTopBtn = document.getElementById('scrollTop');
    if (scrollTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                scrollTopBtn.classList.add('show');
            } else {
                scrollTopBtn.classList.remove('show');
            }
        });
        
        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Newsletter forms (multiple instances possible)
    document.querySelectorAll('[data-newsletter-form]').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const emailInput = form.querySelector('input[type="email"]');
            const submitBtn = form.querySelector('button[type="submit"]');
            const messageDiv = form.querySelector('[data-newsletter-message]');
            
            if (!emailInput || !submitBtn) return;
            
            const email = emailInput.value.trim();
            
            // Disable button
            submitBtn.disabled = true;
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            
            try {
                // For demo purposes, simulate API call
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                // In production, use:
                // await subscribeNewsletter(email);
                
                if (messageDiv) {
                    messageDiv.style.display = 'block';
                    messageDiv.className = 'alert alert-success mt-3';
                    messageDiv.innerHTML = '<i class="fas fa-check-circle me-2"></i> Merci ! Vous êtes maintenant inscrit à notre newsletter.';
                }
                
                form.reset();
                
                setTimeout(() => {
                    if (messageDiv) messageDiv.style.display = 'none';
                }, 5000);
                
            } catch (error) {
                if (messageDiv) {
                    messageDiv.style.display = 'block';
                    messageDiv.className = 'alert alert-danger mt-3';
                    messageDiv.innerHTML = '<i class="fas fa-exclamation-circle me-2"></i> ' + error.message;
                }
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        });
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '#!') {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // Lazy loading images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Active nav link on scroll (for single-page sections)
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    if (sections.length > 0 && navLinks.length > 0) {
        window.addEventListener('scroll', () => {
            let current = '';
            
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                if (scrollY >= (sectionTop - 200)) {
                    current = section.getAttribute('id');
                }
            });
            
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${current}`) {
                    link.classList.add('active');
                }
            });
        });
    }
    
    // Form validation enhancement
    document.querySelectorAll('input[required], textarea[required], select[required]').forEach(field => {
        field.addEventListener('invalid', (e) => {
            e.preventDefault();
            field.classList.add('is-invalid');
        });
        
        field.addEventListener('input', () => {
            if (field.validity.valid) {
                field.classList.remove('is-invalid');
                field.classList.add('is-valid');
            }
        });
    });
});

// ============================================
// ANIMATION UTILITIES
// ============================================

/**
 * Counter animation for statistics
 */
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const updateCounter = () => {
        current += increment;
        if (current < target) {
            element.textContent = Math.ceil(current);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    };
    
    updateCounter();
}

/**
 * Observe elements and trigger animations
 */
function observeElements(selector, callback, options = {}) {
    const defaultOptions = {
        threshold: 0.5,
        rootMargin: '0px'
    };
    
    const observerOptions = { ...defaultOptions, ...options };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                callback(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll(selector).forEach(element => {
        observer.observe(element);
    });
}

// ============================================
// EXPORT FOR MODULE USAGE (if needed)
// ============================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        subscribeNewsletter,
        submitContactForm,
        submitRegistration,
        loadFormations,
        loadEvents,
        loadBlogArticles,
        validateEmail,
        validateFile,
        formatFileSize,
        showAlert,
        smoothScrollTo,
        animateCounter,
        observeElements
    };
}

// Global exposure for direct HTML usage
window.EDMAHApp = {
    subscribeNewsletter,
    submitContactForm,
    submitRegistration,
    loadFormations,
    loadEvents,
    loadBlogArticles,
    validateEmail,
    validateFile,
    formatFileSize,
    showAlert,
    smoothScrollTo,
    animateCounter,
    observeElements
};