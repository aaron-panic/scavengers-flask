document.addEventListener('DOMContentLoaded', () => {
    // Modal Triggers
    const modalTriggers = document.querySelectorAll('[data-modal-target]');
    
    modalTriggers.forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.getAttribute('data-modal-target');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.showModal();
            }
        });
    });
});