/**
 * Rüya Tabiri Sözlüğü - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {

    // ═══════════════════════════════════════════════════════════════════════════
    // Search Index
    // ═══════════════════════════════════════════════════════════════════════════
    let searchIndex = null;

    async function loadSearchIndex() {
        if (searchIndex) return searchIndex;
        try {
            const response = await fetch('/index.json');
            searchIndex = await response.json();
            return searchIndex;
        } catch (error) {
            console.error('Search index yüklenemedi:', error);
            return [];
        }
    }

    // Turkish character normalization
    function normalizeText(text) {
        if (!text) return '';
        return text
            .toLowerCase()
            .replace(/ı/g, 'i')
            .replace(/ğ/g, 'g')
            .replace(/ü/g, 'u')
            .replace(/ş/g, 's')
            .replace(/ö/g, 'o')
            .replace(/ç/g, 'c')
            .replace(/İ/g, 'i')
            .replace(/Ğ/g, 'g')
            .replace(/Ü/g, 'u')
            .replace(/Ş/g, 's')
            .replace(/Ö/g, 'o')
            .replace(/Ç/g, 'c');
    }

    function searchContent(query, maxResults = 8) {
        if (!searchIndex || !query || query.length < 2) return [];

        const normalizedQuery = normalizeText(query);
        const results = [];

        for (const item of searchIndex) {
            const normalizedTitle = normalizeText(item.title);
            const normalizedDesc = normalizeText(item.description);

            // Check if query matches title or description
            if (normalizedTitle.includes(normalizedQuery) || normalizedDesc.includes(normalizedQuery)) {
                // Prioritize exact title matches
                const priority = normalizedTitle.includes(normalizedQuery) ? 1 : 2;
                results.push({ ...item, priority });
            }

            if (results.length >= maxResults * 2) break;
        }

        // Sort by priority and limit results
        return results
            .sort((a, b) => a.priority - b.priority)
            .slice(0, maxResults);
    }

    function renderSearchResults(results, container) {
        if (!container) return;

        if (results.length === 0) {
            container.innerHTML = '<div class="search-no-results">Sonuç bulunamadı</div>';
            container.classList.add('active');
            return;
        }

        const html = results.map(item => `
            <a href="${item.url}" class="search-result-item">
                <span class="search-result-title">${item.title}</span>
                <span class="search-result-category">${item.kategori || 'genel'}</span>
            </a>
        `).join('');

        container.innerHTML = html;
        container.classList.add('active');
    }

    function hideSearchResults(container) {
        if (container) {
            container.classList.remove('active');
            container.innerHTML = '';
        }
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Search Functionality
    // ═══════════════════════════════════════════════════════════════════════════
    const searchInputs = [
        { input: document.getElementById('search-input'), results: document.getElementById('nav-search-results') },
        { input: document.getElementById('hero-search-input'), results: document.getElementById('hero-search-results') }
    ];

    let searchTimeout = null;

    searchInputs.forEach(({ input, results }) => {
        if (!input) return;

        // Input event for live search
        input.addEventListener('input', async function() {
            const query = this.value.trim();

            clearTimeout(searchTimeout);

            if (query.length < 2) {
                hideSearchResults(results);
                return;
            }

            // Load index if not loaded
            await loadSearchIndex();

            // Debounce search
            searchTimeout = setTimeout(() => {
                const searchResults = searchContent(query);
                renderSearchResults(searchResults, results);
            }, 150);
        });

        // Enter key to go to first result or search page
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const query = this.value.trim();
                if (query) {
                    const firstResult = results?.querySelector('.search-result-item');
                    if (firstResult) {
                        window.location.href = firstResult.href;
                    } else {
                        window.location.href = '/ruya/?q=' + encodeURIComponent(query);
                    }
                }
            }
        });

        // Focus event
        input.addEventListener('focus', async function() {
            const query = this.value.trim();
            if (query.length >= 2) {
                await loadSearchIndex();
                const searchResults = searchContent(query);
                renderSearchResults(searchResults, results);
            }
        });
    });

    // Close search results when clicking outside
    document.addEventListener('click', function(e) {
        searchInputs.forEach(({ input, results }) => {
            if (input && results && !input.contains(e.target) && !results.contains(e.target)) {
                hideSearchResults(results);
            }
        });
    });

    // ═══════════════════════════════════════════════════════════════════════════
    // Mobile Menu Toggle
    // ═══════════════════════════════════════════════════════════════════════════
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const navLinks = document.getElementById('nav-links');
    const header = document.getElementById('header');

    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            navLinks.classList.toggle('active');
            this.classList.toggle('active');

            // Toggle icon
            const icon = this.querySelector('svg path');
            if (navLinks.classList.contains('active')) {
                icon.setAttribute('d', 'M18 6L6 18M6 6l12 12');
            } else {
                icon.setAttribute('d', 'M3 12h18M3 6h18M3 18h18');
            }
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!mobileMenuBtn.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
                const icon = mobileMenuBtn.querySelector('svg path');
                if (icon) icon.setAttribute('d', 'M3 12h18M3 6h18M3 18h18');
            }
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function() {
                navLinks.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
                const icon = mobileMenuBtn.querySelector('svg path');
                if (icon) icon.setAttribute('d', 'M3 12h18M3 6h18M3 18h18');
            });
        });
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Header Scroll Effect
    // ═══════════════════════════════════════════════════════════════════════════
    if (header) {
        let lastScroll = 0;

        window.addEventListener('scroll', function() {
            const currentScroll = window.pageYOffset;

            if (currentScroll > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }

            lastScroll = currentScroll;
        }, { passive: true });
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Back to Top Button
    // ═══════════════════════════════════════════════════════════════════════════
    const backToTop = document.getElementById('back-to-top');

    if (backToTop) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        }, { passive: true });

        backToTop.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Reading Progress Bar (Article Pages)
    // ═══════════════════════════════════════════════════════════════════════════
    const article = document.querySelector('.article-content');

    if (article) {
        const progressBar = document.createElement('div');
        progressBar.className = 'reading-progress';
        document.body.prepend(progressBar);

        window.addEventListener('scroll', function() {
            const rect = article.getBoundingClientRect();
            const articleTop = rect.top + window.pageYOffset;
            const articleHeight = rect.height;
            const windowHeight = window.innerHeight;
            const scrolled = window.pageYOffset;

            const progress = Math.min(100, Math.max(0,
                ((scrolled - articleTop + windowHeight * 0.3) / (articleHeight)) * 100
            ));

            progressBar.style.width = progress + '%';
        }, { passive: true });
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // Smooth Scroll for Anchor Links
    // ═══════════════════════════════════════════════════════════════════════════
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // ═══════════════════════════════════════════════════════════════════════════
    // Lazy Loading Images
    // ═══════════════════════════════════════════════════════════════════════════
    const lazyImages = document.querySelectorAll('img[data-src]');

    if ('IntersectionObserver' in window && lazyImages.length > 0) {
        const imageObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });

        lazyImages.forEach(function(img) {
            imageObserver.observe(img);
        });
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // External Links - Open in New Tab
    // ═══════════════════════════════════════════════════════════════════════════
    document.querySelectorAll('a[href^="http"]').forEach(function(link) {
        if (!link.href.includes(window.location.hostname)) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });

    // ═══════════════════════════════════════════════════════════════════════════
    // Preload search index on idle
    // ═══════════════════════════════════════════════════════════════════════════
    if ('requestIdleCallback' in window) {
        requestIdleCallback(() => loadSearchIndex());
    } else {
        setTimeout(() => loadSearchIndex(), 2000);
    }

});
