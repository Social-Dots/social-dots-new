/**
 * Portfolio Animations and Effects
 * This file contains all the animations and interactive elements for the portfolio page
*/

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Portfolio animations initialized');
    
    // Initialize all animations
    initParticleBackground();
    initParallaxEffects();
    initGradientText();
    init3DCardEffects();
    initMagneticHover();
    initMicroInteractions();
    initScrollProgress();
    initScrollAnimations();
    initLazyLoading();
    initSvgAnimations();
    initVideoPreview();
    initMobileOptimizations();
    initBackgroundEffects();
    initFloatingActionButton();
    initPortfolioFilters(); // Initialize portfolio filtering and search
});

/**
 * Initialize particle.js background in the hero section
 */
function initParticleBackground() {
    const heroSection = document.querySelector('#portfolio-hero');
    if (!heroSection) return;
    
    // Configure particles.js
    if (window.particlesJS) {
        particlesJS('particles-js', {
            particles: {
                number: { value: 80, density: { enable: true, value_area: 800 } },
                color: { value: ['#0B32A4', '#0E42CE', '#FFA300'] },
                shape: {
                    type: ['circle', 'triangle', 'polygon'],
                    stroke: { width: 0, color: '#000000' },
                    polygon: { nb_sides: 5 }
                },
                opacity: {
                    value: 0.5,
                    random: true,
                    anim: { enable: true, speed: 1, opacity_min: 0.1, sync: false }
                },
                size: {
                    value: 5,
                    random: true,
                    anim: { enable: true, speed: 2, size_min: 0.1, sync: false }
                },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: '#0B32A4',
                    opacity: 0.2,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 1,
                    direction: 'none',
                    random: true,
                    straight: false,
                    out_mode: 'out',
                    bounce: false,
                    attract: { enable: true, rotateX: 600, rotateY: 1200 }
                }
            },
            interactivity: {
                detect_on: 'canvas',
                events: {
                    onhover: { enable: true, mode: 'grab' },
                    onclick: { enable: true, mode: 'push' },
                    resize: true
                },
                modes: {
                    grab: { distance: 140, line_linked: { opacity: 0.5 } },
                    bubble: { distance: 400, size: 40, duration: 2, opacity: 0.8, speed: 3 },
                    repulse: { distance: 200, duration: 0.4 },
                    push: { particles_nb: 4 },
                    remove: { particles_nb: 2 }
                }
            },
            retina_detect: true
        });
    }
}

/**
 * Initialize parallax effects on the hero section
 * Modified to prevent floating background issues
 */
function initParallaxEffects() {
    // Simple parallax effect on scroll - only for decorative elements, not backgrounds
    const parallaxElements = document.querySelectorAll('.parallax');
    
    if (parallaxElements.length > 0) {
        window.addEventListener('scroll', function() {
            const scrollY = window.scrollY;
            
            parallaxElements.forEach(element => {
                // Skip background elements to prevent floating issues
                if (element.classList.contains('bg-element')) return;
                
                const speed = element.getAttribute('data-parallax-speed') || 0.2;
                const yPos = -(scrollY * speed);
                // Use a more subtle transform with a max limit to prevent excessive movement
                const limitedYPos = Math.max(Math.min(yPos, 50), -50); // Limit to ±50px
                element.style.transform = `translate3d(0, ${limitedYPos}px, 0)`;
            });
        });
    }
}

/**
 * Initialize gradient text animation on the main headline
 */
function initGradientText() {
    // Animated gradient text effect using GSAP if available
    const gradientTexts = document.querySelectorAll('.gradient-text');
    
    if (gradientTexts.length > 0 && window.gsap) {
        gradientTexts.forEach(text => {
            gsap.to(text, {
                backgroundPosition: '200% center',
                duration: 10,
                ease: 'none',
                repeat: -1
            });
        });
    }
}

/**
 * Initialize enhanced 3D card effects on portfolio items
 */
function init3DCardEffects() {
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    const cardElements = document.querySelectorAll('.card-3d');
    
    // Traditional flip effect
    portfolioItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.classList.add('flipped');
        });
        
        item.addEventListener('mouseleave', function() {
            this.classList.remove('flipped');
        });
    });
    
    // Enhanced 3D hover effect for cards
    cardElements.forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            // Calculate mouse position relative to card center
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            // Calculate rotation angles (enhanced for more pronounced 3D effect)
            const rotateY = Math.min(Math.max(x / 15, -8), 8); // Increased range
            const rotateX = Math.min(Math.max(-y / 15, -8), 8); // Increased range
            
            // Apply enhanced 3D transform with more depth
            this.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(20px) scale3d(1.03, 1.03, 1.03)`;
            
            // Enhanced shadow effect based on tilt
            const shadowX = rotateY * 2.5;
            const shadowY = rotateX * 2.5;
            const shadowBlur = Math.abs(rotateX) + Math.abs(rotateY) + 15;
            this.style.boxShadow = `${shadowX}px ${shadowY}px ${shadowBlur}px rgba(0, 0, 0, 0.15), 0 10px 20px rgba(0, 0, 0, 0.1)`;
            
            // Enhanced 3D effects for inner elements
            // Corner accents
            const cornerElements = this.querySelectorAll('[class*="absolute"][class*="w-16"], [class*="absolute"][class*="h-16"]');
            cornerElements.forEach(corner => {
                corner.style.opacity = '1';
                // Apply subtle transform to corners based on mouse position
                const cornerX = x / 40;
                const cornerY = y / 40;
                corner.style.transform = `translate(${cornerX}px, ${cornerY}px)`;
            });
            
            // Content elements - subtle parallax effect
            const contentElements = this.querySelectorAll('.p-6 > .space-y-4, h3, p, .flex');
            contentElements.forEach(element => {
                // Inverse movement for parallax effect
                const parallaxX = -x / 60;
                const parallaxY = -y / 60;
                element.style.transform = `translate(${parallaxX}px, ${parallaxY}px)`;
            });
            
            // Image parallax effect
            const imageContainer = this.querySelector('.relative.h-64');
            if (imageContainer) {
                const imageX = -x / 40;
                const imageY = -y / 40;
                imageContainer.style.transform = `translate(${imageX}px, ${imageY}px)`;
            }
        });
        
        card.addEventListener('mouseleave', function() {
            // Reset all transforms and effects with a smooth transition
            this.style.transform = '';
            this.style.boxShadow = '';
            
            // Reset corner highlights and transforms
            const cornerElements = this.querySelectorAll('[class*="absolute"][class*="w-16"], [class*="absolute"][class*="h-16"]');
            cornerElements.forEach(corner => {
                corner.style.opacity = '';
                corner.style.transform = '';
            });
            
            // Reset content elements
            const contentElements = this.querySelectorAll('.p-6 > .space-y-4, h3, p, .flex');
            contentElements.forEach(element => {
                element.style.transform = '';
            });
            
            // Reset image container
            const imageContainer = this.querySelector('.relative.h-64');
            if (imageContainer) {
                imageContainer.style.transform = '';
            }
        });
    });
}

/**
 * Initialize magnetic hover effect on portfolio cards
 */
function initMagneticHover() {
    const magneticElements = document.querySelectorAll('.magnetic');
    
    magneticElements.forEach(element => {
        element.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            // Calculate distance from center (0,0)
            const distance = Math.sqrt(x * x + y * y);
            const maxDistance = Math.sqrt(Math.pow(rect.width / 2, 2) + Math.pow(rect.height / 2, 2));
            
            // Normalize the distance (0-1)
            const normalizedDistance = Math.min(distance / maxDistance, 1);
            
            // Calculate the magnetic pull (stronger when closer to center)
            const pull = 15 * (1 - normalizedDistance);
            
            // Apply the transform
            this.style.transform = `translate(${x / 10}px, ${y / 10}px)`;
        });
        
        element.addEventListener('mouseleave', function() {
            // Reset the transform when mouse leaves
            this.style.transform = 'translate(0, 0)';
        });
    });
}

/**
 * Initialize micro-interactions for clickable elements
 */
function initMicroInteractions() {
    const interactiveElements = document.querySelectorAll('.btn, .filter-btn, .nav-link, .portfolio-item');
    
    interactiveElements.forEach(element => {
        element.addEventListener('mousedown', function() {
            this.style.transform = 'scale(0.98)';
        });
        
        element.addEventListener('mouseup', function() {
            this.style.transform = '';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
    
    // Enhanced micro-interactions for filter buttons
    const microInteractionButtons = document.querySelectorAll('.micro-interaction');
    microInteractionButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.classList.add('group');
        });
        
        button.addEventListener('mouseleave', function() {
            this.classList.remove('group');
        });
    });
    
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn, .filter-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s linear';
            ripple.style.backgroundColor = 'rgba(255, 255, 255, 0.7)';
            ripple.style.width = '20px';
            ripple.style.height = '20px';
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            ripple.style.pointerEvents = 'none';
            
            // Add the ripple style if it doesn't exist
            if (!document.querySelector('style#ripple-style')) {
                const style = document.createElement('style');
                style.id = 'ripple-style';
                style.textContent = `
                    @keyframes ripple {
                        to {
                            transform: scale(4);
                            opacity: 0;
                        }
                    }
                `;
                document.head.appendChild(style);
            }
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Enhanced micro-interactions for search inputs
    const microInputs = document.querySelectorAll('.micro-input');
    microInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
    
    // Enhanced micro-interactions for select dropdowns
    const microSelects = document.querySelectorAll('.micro-select');
    microSelects.forEach(select => {
        select.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        select.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
}

/**
 * Initialize scroll progress indicator for the portfolio section
 */
function initScrollProgress() {
    const progressBar = document.querySelector('.scroll-progress');
    if (!progressBar) return;
    
    const portfolioSection = document.querySelector('#portfolio-grid');
    if (!portfolioSection) return;
    
    window.addEventListener('scroll', function() {
        const portfolioRect = portfolioSection.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        
        // Calculate how much of the portfolio section has been scrolled
        let progress = 0;
        
        if (portfolioRect.top <= 0) {
            // Section is at or above the top of the viewport
            const totalHeight = portfolioRect.height;
            const scrolledHeight = Math.min(Math.abs(portfolioRect.top), totalHeight);
            progress = (scrolledHeight / totalHeight) * 100;
        }
        
        // Update the progress bar width
        progressBar.style.width = `${progress}%`;
    });
}

/**
 * Initialize GSAP animations for scroll-triggered reveals
 */
function initScrollAnimations() {
    if (!window.gsap || !window.ScrollTrigger) return;
    
    // Fade in animations for portfolio items
    gsap.utils.toArray('.gsap-fade-in').forEach(element => {
        gsap.from(element, {
            opacity: 0,
            y: 50,
            duration: 0.8,
            ease: 'power2.out',
            scrollTrigger: {
                trigger: element,
                start: 'top 80%',
                toggleActions: 'play none none none'
            }
        });
    });
    
    // Stagger animations for grid items
    const gridContainers = document.querySelectorAll('.gsap-stagger-container');
    gridContainers.forEach(container => {
        const items = container.querySelectorAll('.gsap-stagger-item');
        
        gsap.from(items, {
            opacity: 0,
            y: 50,
            stagger: 0.1,
            duration: 0.8,
            ease: 'power2.out',
            scrollTrigger: {
                trigger: container,
                start: 'top 80%',
                toggleActions: 'play none none none'
            }
        });
    });
}

/**
 * Initialize portfolio filtering, search and sorting functionality
 */
function initPortfolioFilters() {
    const portfolioGrid = document.querySelector('.portfolio-grid');
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    const categoryPills = document.querySelectorAll('.category-pill');
    const searchInput = document.querySelector('#portfolio-search');
    const sortSelect = document.querySelector('#portfolio-sort');
    const activeFiltersContainer = document.querySelector('.active-filters');
    
    let activeCategory = 'all';
    let searchTerm = '';
    let currentSort = 'newest';
    
    // Function to update active filters display
    function updateActiveFilters() {
        activeFiltersContainer.innerHTML = '';
        
        // Add category filter if not 'all'
        if (activeCategory !== 'all') {
            const categoryName = Array.from(categoryPills)
                .find(pill => pill.dataset.category === activeCategory)
                .textContent.trim();
                
            const filterTag = document.createElement('div');
            filterTag.className = 'active-filter-tag';
            filterTag.innerHTML = `
                <span>${categoryName}</span>
                <button class="clear-filter" data-filter-type="category">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                </button>
            `;
            activeFiltersContainer.appendChild(filterTag);
        }
        
        // Add search term filter if exists
        if (searchTerm) {
            const filterTag = document.createElement('div');
            filterTag.className = 'active-filter-tag';
            filterTag.innerHTML = `
                <span>"${searchTerm}"</span>
                <button class="clear-filter" data-filter-type="search">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                </button>
            `;
            activeFiltersContainer.appendChild(filterTag);
        }
        
        // Show or hide the active filters section
        if (activeCategory !== 'all' || searchTerm) {
            activeFiltersContainer.classList.remove('hidden');
        } else {
            activeFiltersContainer.classList.add('hidden');
        }
        
        // Add event listeners to clear filter buttons
        document.querySelectorAll('.clear-filter').forEach(btn => {
            btn.addEventListener('click', function() {
                const filterType = this.dataset.filterType;
                
                if (filterType === 'category') {
                    activeCategory = 'all';
                    updateCategoryPills();
                } else if (filterType === 'search') {
                    searchTerm = '';
                    searchInput.value = '';
                }
                
                filterPortfolioItems();
            });
        });
    }
    
    // Function to update category pills active state
    function updateCategoryPills() {
        categoryPills.forEach(pill => {
            if (pill.dataset.category === activeCategory) {
                pill.classList.add('active');
            } else {
                pill.classList.remove('active');
            }
        });
    }
    
    // Function to filter portfolio items
    function filterPortfolioItems() {
        let visibleCount = 0;
        
        portfolioItems.forEach(item => {
            const itemCategory = item.dataset.category;
            const itemTitle = item.querySelector('.project-title').textContent.toLowerCase();
            const itemDescription = item.querySelector('.project-description').textContent.toLowerCase();
            const itemTechnologies = item.querySelector('.project-technologies').textContent.toLowerCase();
            
            // Check if item matches category filter
            const matchesCategory = activeCategory === 'all' || itemCategory === activeCategory;
            
            // Check if item matches search term
            const matchesSearch = !searchTerm || 
                itemTitle.includes(searchTerm.toLowerCase()) || 
                itemDescription.includes(searchTerm.toLowerCase()) ||
                itemTechnologies.includes(searchTerm.toLowerCase());
            
            // Show or hide item based on filters
            if (matchesCategory && matchesSearch) {
                item.style.display = '';
                visibleCount++;
                
                // Add animation class for appearing items
                item.classList.add('filter-fade-in');
                setTimeout(() => {
                    item.classList.remove('filter-fade-in');
                }, 500);
            } else {
                item.style.display = 'none';
            }
        });
        
        // Show no results message if needed
        const noResultsMessage = document.querySelector('.no-results-message');
        if (visibleCount === 0) {
            if (!noResultsMessage) {
                const message = document.createElement('div');
                message.className = 'no-results-message';
                message.innerHTML = `
                    <div class="flex flex-col items-center justify-center py-12 text-center">
                        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search-x mb-4 text-gray-400"><path d="m13.5 8.5-5 5"/><path d="m8.5 8.5 5 5"/><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                        <h3 class="text-xl font-bold mb-2">No projects found</h3>
                        <p class="text-gray-500">Try adjusting your search or filter criteria</p>
                        <button id="reset-filters" class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all">
                            Reset all filters
                        </button>
                    </div>
                `;
                portfolioGrid.appendChild(message);
                
                // Add event listener to reset button
                document.getElementById('reset-filters').addEventListener('click', resetAllFilters);
            }
        } else if (noResultsMessage) {
            noResultsMessage.remove();
        }
        
        // Update active filters display
        updateActiveFilters();
    }
    
    // Function to sort portfolio items
    function sortPortfolioItems() {
        const items = Array.from(portfolioItems);
        
        items.sort((a, b) => {
            if (currentSort === 'newest') {
                // Sort by date (newest first)
                const dateA = new Date(a.dataset.date || '2000-01-01');
                const dateB = new Date(b.dataset.date || '2000-01-01');
                return dateB - dateA;
            } else if (currentSort === 'oldest') {
                // Sort by date (oldest first)
                const dateA = new Date(a.dataset.date || '2000-01-01');
                const dateB = new Date(b.dataset.date || '2000-01-01');
                return dateA - dateB;
            } else if (currentSort === 'name-asc') {
                // Sort alphabetically (A-Z)
                const titleA = a.querySelector('.project-title').textContent;
                const titleB = b.querySelector('.project-title').textContent;
                return titleA.localeCompare(titleB);
            } else if (currentSort === 'name-desc') {
                // Sort alphabetically (Z-A)
                const titleA = a.querySelector('.project-title').textContent;
                const titleB = b.querySelector('.project-title').textContent;
                return titleB.localeCompare(titleA);
            }
            return 0;
        });
        
        // Reorder items in the DOM
        const fragment = document.createDocumentFragment();
        items.forEach(item => {
            fragment.appendChild(item);
        });
        
        portfolioGrid.innerHTML = '';
        portfolioGrid.appendChild(fragment);
        
        // Re-initialize 3D effects for the reordered items
        init3DCardEffects();
    }
    
    // Function to reset all filters
    function resetAllFilters() {
        activeCategory = 'all';
        searchTerm = '';
        currentSort = 'newest';
        
        // Reset UI elements
        searchInput.value = '';
        sortSelect.value = 'newest';
        updateCategoryPills();
        
        // Apply filters and sort
        filterPortfolioItems();
        sortPortfolioItems();
    }
    
    // Event listeners for category pills
    categoryPills.forEach(pill => {
        pill.addEventListener('click', function() {
            activeCategory = this.dataset.category;
            updateCategoryPills();
            filterPortfolioItems();
            
            // Add ripple effect
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Event listener for search input
    let searchTimeout;
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                searchTerm = this.value.trim();
                filterPortfolioItems();
            }, 300); // Debounce search for better performance
        });
    }
    
    // Event listener for sort select
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            currentSort = this.value;
            sortPortfolioItems();
        });
    }
    
    // Initialize filters and sorting
    updateCategoryPills();
    filterPortfolioItems();
    sortPortfolioItems();
}

/**
 * Initialize lazy loading with placeholder animations
 */
function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('.lazy-image');
        
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    const src = img.getAttribute('data-src');
                    
                    if (src) {
                        img.src = src;
                        img.classList.add('loaded');
                        img.classList.remove('loading');
                        observer.unobserve(img);
                    }
                }
            });
        });
        
        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    }
}

/**
 * Initialize SVG path animations
 */
function initSvgAnimations() {
    if (!window.gsap) return;
    
    const svgElements = document.querySelectorAll('.animated-svg');
    
    svgElements.forEach(svg => {
        const paths = svg.querySelectorAll('path');
        
        gsap.fromTo(paths, 
            { strokeDashoffset: 100, strokeDasharray: 100 },
            {
                strokeDashoffset: 0,
                duration: 2,
                ease: 'power2.out',
                stagger: 0.1,
                scrollTrigger: {
                    trigger: svg,
                    start: 'top 80%',
                    toggleActions: 'play none none none'
                }
            }
        );
    });
}

/**
 * Initialize video previews on hover
 */
function initVideoPreview() {
    const videoPreviewItems = document.querySelectorAll('.video-preview');
    
    videoPreviewItems.forEach(item => {
        const videoSrc = item.getAttribute('data-video-src');
        if (!videoSrc) return;
        
        const videoElement = document.createElement('video');
        videoElement.src = videoSrc;
        videoElement.muted = true;
        videoElement.loop = true;
        videoElement.classList.add('absolute', 'inset-0', 'object-cover', 'w-full', 'h-full', 'opacity-0', 'transition-opacity', 'duration-300');
        
        item.appendChild(videoElement);
        
        item.addEventListener('mouseenter', function() {
            videoElement.play();
            videoElement.classList.remove('opacity-0');
            videoElement.classList.add('opacity-100');
        });
        
        item.addEventListener('mouseleave', function() {
            videoElement.pause();
            videoElement.currentTime = 0;
            videoElement.classList.remove('opacity-100');
            videoElement.classList.add('opacity-0');
        });
    });
}

/**
 * Initialize mobile-specific optimizations
 */
function initMobileOptimizations() {
    // Check if device is mobile
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    
    if (isMobile) {
        // Add touch-friendly classes
        document.body.classList.add('touch-device');
        
        // Initialize horizontal scroll for project cards on mobile
        const horizontalScrollContainers = document.querySelectorAll('.horizontal-scroll');
        
        horizontalScrollContainers.forEach(container => {
            // Enable momentum scrolling with CSS
            container.style.webkitOverflowScrolling = 'touch';
            container.style.overflowX = 'auto';
            
            // Add snap scrolling for better experience
            container.style.scrollSnapType = 'x mandatory';
            
            // Make child items snap points
            const items = container.children;
            for (let i = 0; i < items.length; i++) {
                items[i].style.scrollSnapAlign = 'start';
                items[i].style.flexShrink = '0';
            }
        });
    }
}

/**
 * Initialize background effects (noise, gradients)
 */
function initBackgroundEffects() {
    // Add subtle noise texture to sections with the .noise-bg class
    const noiseBgElements = document.querySelectorAll('.noise-bg');
    
    noiseBgElements.forEach(element => {
        // Apply the noise background
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        
        const noiseOverlay = document.createElement('div');
        noiseOverlay.classList.add('noise-overlay');
        noiseOverlay.style.position = 'absolute';
        noiseOverlay.style.inset = '0';
        noiseOverlay.style.opacity = '0.05';
        noiseOverlay.style.pointerEvents = 'none';
        noiseOverlay.style.zIndex = '1';
        
        element.appendChild(noiseOverlay);
    });
    
    // Animated gradient overlays
    const gradientOverlays = document.querySelectorAll('.gradient-overlay');
    
    if (gradientOverlays.length > 0 && window.gsap) {
        gradientOverlays.forEach(overlay => {
            gsap.to(overlay, {
                backgroundPosition: '200% 0',
                duration: 20,
                ease: 'none',
                repeat: -1
            });
        });
    }
}

/**
 * Initialize floating action button
 */
function initFloatingActionButton() {
    const fab = document.querySelector('.floating-action-button');
    if (!fab) return;
    
    // Show/hide FAB based on scroll position
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            fab.classList.add('visible');
        } else {
            fab.classList.remove('visible');
        }
    });
    
    // Add pulse animation
    if (window.gsap) {
        gsap.to(fab, {
            scale: 1.05,
            duration: 1,
            repeat: -1,
            yoyo: true,
            ease: 'power1.inOut'
        });
    }
}
