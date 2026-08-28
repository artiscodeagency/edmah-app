/**
 * EDMAH Framework JS — comportements maison (modales, FAQ, menu mobile)
 * Remplace bootstrap.bundle.js.
 */

function openEdmahModal(id, trigger) {
    const backdrop = document.getElementById(id);
    if (!backdrop) return;
    backdrop.classList.add('active');
    backdrop.dispatchEvent(new CustomEvent('edmah-modal-open', { detail: { trigger } }));
    document.body.style.overflow = 'hidden';
}

function closeEdmahModal(id) {
    const backdrop = typeof id === 'string' ? document.getElementById(id) : id;
    if (!backdrop) return;
    backdrop.classList.remove('active');
    backdrop.dispatchEvent(new CustomEvent('edmah-modal-close'));
    document.body.style.overflow = '';
}

document.addEventListener('DOMContentLoaded', () => {
    // Open triggers: [data-modal-open="modalId"]
    document.querySelectorAll('[data-modal-open]').forEach(trigger => {
        trigger.addEventListener('click', () => {
            openEdmahModal(trigger.getAttribute('data-modal-open'), trigger);
        });
    });

    // Close triggers: [data-modal-close] inside a .edmah-modal-backdrop
    document.querySelectorAll('.edmah-modal-backdrop').forEach(backdrop => {
        backdrop.querySelectorAll('[data-modal-close]').forEach(btn => {
            btn.addEventListener('click', () => closeEdmahModal(backdrop));
        });
        backdrop.addEventListener('click', (e) => {
            if (e.target === backdrop) closeEdmahModal(backdrop);
        });
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.edmah-modal-backdrop.active').forEach(closeEdmahModal);
        }
    });

    // Generic FAQ / accordion toggle: [data-accordion-trigger]
    document.querySelectorAll('[data-accordion-trigger]').forEach(trigger => {
        trigger.addEventListener('click', () => {
            trigger.closest('.accordion-item, .faq-item')?.classList.toggle('is-open');
            trigger.closest('.faq-item')?.classList.toggle('active');
        });
    });
});
