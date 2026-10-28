/**
 * NotesApp - Interactive Client Utilities
 * - Theme Switcher (Dark / Light) with localStorage persistence
 * - Real-time Note Search & Filtering
 * - One-click Copy Note Content
 * - Character & Word Counter
 * - Password Show/Hide Toggle
 * - Safe Delete Confirmation
 */

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initPasswordToggle();
    initCharCounters();
    initNoteSearch();
    initCopyButtons();
    initDeleteConfirmations();
});

/* --- 1. Theme Management --- */
function initTheme() {
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeToggleIcon');
    const htmlElement = document.documentElement;

    // Check saved preference or default to dark
    const savedTheme = localStorage.getItem('notesapp-theme') || 'dark';
    setTheme(savedTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-theme') || 'dark';
            const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(nextTheme);
        });
    }

    function setTheme(theme) {
        htmlElement.setAttribute('data-theme', theme);
        localStorage.setItem('notesapp-theme', theme);
        if (themeIcon) {
            if (theme === 'light') {
                themeIcon.className = 'fa-solid fa-moon';
                if (themeToggleBtn) themeToggleBtn.setAttribute('title', 'Switch to Dark Mode');
            } else {
                themeIcon.className = 'fa-solid fa-sun';
                if (themeToggleBtn) themeToggleBtn.setAttribute('title', 'Switch to Light Mode');
            }
        }
    }
}

/* --- 2. Password Visibility Toggle --- */
function initPasswordToggle() {
    const toggleBtns = document.querySelectorAll('.toggle-pwd-btn');
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const input = document.getElementById(targetId);
            if (!input) return;

            const isPassword = input.type === 'password';
            input.type = isPassword ? 'text' : 'password';
            
            const icon = btn.querySelector('i');
            if (icon) {
                icon.className = isPassword ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye';
            }
        });
    });
}

/* --- 3. Dynamic Character & Word Counters --- */
function initCharCounters() {
    const textareas = document.querySelectorAll('[data-counter-target]');
    textareas.forEach(textarea => {
        const counterEl = document.getElementById(textarea.getAttribute('data-counter-target'));
        if (!counterEl) return;

        const updateCount = () => {
            const count = textarea.value.trim().length;
            const words = textarea.value.trim() ? textarea.value.trim().split(/\s+/).length : 0;
            counterEl.textContent = `${count} characters • ${words} words`;
        };

        textarea.addEventListener('input', updateCount);
        updateCount(); // Initial run
    });
}

/* --- 4. Live Notes Filtering / Search --- */
function initNoteSearch() {
    const searchInput = document.getElementById('noteSearchInput');
    const noteCards = document.querySelectorAll('.note-card');
    const notesGrid = document.getElementById('notesGrid');
    const notesCountBadge = document.getElementById('notesCountBadge');
    const noSearchResults = document.getElementById('noSearchResults');

    if (!searchInput || !noteCards.length) return;

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        let visibleCount = 0;

        noteCards.forEach(card => {
            const content = card.getAttribute('data-content') || card.innerText;
            if (content.toLowerCase().includes(query)) {
                card.style.display = 'flex';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Update count badge
        if (notesCountBadge) {
            notesCountBadge.textContent = `${visibleCount} of ${noteCards.length} notes`;
        }

        // Show/hide no results message
        if (noSearchResults) {
            noSearchResults.style.display = (visibleCount === 0) ? 'block' : 'none';
        }
    });
}

/* --- 5. Quick Copy Note to Clipboard --- */
function initCopyButtons() {
    const copyBtns = document.querySelectorAll('.btn-copy-note');
    copyBtns.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const textToCopy = btn.getAttribute('data-copy-text');
            if (!textToCopy) return;

            try {
                await navigator.clipboard.writeText(textToCopy);
                const originalHtml = btn.innerHTML;
                btn.innerHTML = '<i class="fa-solid fa-check" style="color: var(--success);"></i>';
                btn.setAttribute('title', 'Copied to clipboard!');
                setTimeout(() => {
                    btn.innerHTML = originalHtml;
                    btn.setAttribute('title', 'Copy Note');
                }, 1800);
            } catch (err) {
                console.error('Failed to copy', err);
            }
        });
    });
}

/* --- 6. Delete Confirmation Prompt --- */
function initDeleteConfirmations() {
    const deleteLinks = document.querySelectorAll('.btn-delete-confirm');
    deleteLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const confirmed = confirm('Are you sure you want to permanently delete this note?');
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });
}
