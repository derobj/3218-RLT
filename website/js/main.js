/* ============================================================
   Road Less Traveled — main.js
   ============================================================ */

// All 94 photos in numeric order
const allPhotos = [
    1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
    21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,
    41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,
    61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,
    81,82,83,84,85,86,87,88,89,90,91,92,93,94
].map(n => `Photos/jbp-web-ROADLESSTRAVELED-${n}.jpg`);

// Featured gallery photos (12, matching the HTML order)
const featuredPhotos = [
    'Photos/jbp-web-ROADLESSTRAVELED-80.jpg',
    'Photos/jbp-web-ROADLESSTRAVELED-85.jpg',
    'Photos/jbp-web-ROADLESSTRAVELED-3.jpg',
    'Photos/jbp-web-ROADLESSTRAVELED-10.jpg',
    'Photos/jbp-web-ROADLESSTRAVELED-30.jpg',
    'Photos/jbp-web-ROADLESSTRAVELED-15.jpg',
    'Photos/jbp-web-ROADLESSTRAVELED-20.jpg',
    'Photos/jbp-web-ROADLESSTRAVELED-25.jpg',
    'Photos/jbp-web-ROADLESSTRAVELED-40.jpg',
    'Photos/jbp-web-ROADLESSTRAVELED-5.jpg',
    'Photos/jbp-web-ROADLESSTRAVELED-55.jpg',
    'Photos/jbp-web-ROADLESSTRAVELED-90.jpg',
];

let currentPhotos = featuredPhotos;
let currentIndex  = 0;

// ── Navbar scroll behaviour ──────────────────────────────────
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 60) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
}, { passive: true });

// ── Hamburger menu ───────────────────────────────────────────
const hamburger  = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobile-menu');

hamburger.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
});

// Close mobile menu when a link is clicked
mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => mobileMenu.classList.remove('open'));
});

// ── Lightbox ─────────────────────────────────────────────────
const lightbox     = document.getElementById('lightbox');
const lightboxImg  = document.getElementById('lightbox-img');
const lightboxCounter = document.getElementById('lightbox-counter');
const btnClose     = document.getElementById('lightbox-close');
const btnPrev      = document.getElementById('lightbox-prev');
const btnNext      = document.getElementById('lightbox-next');

function openLightbox(photos, index) {
    currentPhotos = photos;
    currentIndex  = index;
    showPhoto();
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
}

function showPhoto() {
    lightboxImg.src = currentPhotos[currentIndex];
    lightboxImg.alt = `Road Less Traveled — photo ${currentIndex + 1}`;
    lightboxCounter.textContent = `${currentIndex + 1} / ${currentPhotos.length}`;
}

function prevPhoto() {
    currentIndex = (currentIndex - 1 + currentPhotos.length) % currentPhotos.length;
    showPhoto();
}

function nextPhoto() {
    currentIndex = (currentIndex + 1) % currentPhotos.length;
    showPhoto();
}

btnClose.addEventListener('click', closeLightbox);
btnPrev.addEventListener('click', prevPhoto);
btnNext.addEventListener('click', nextPhoto);

lightbox.addEventListener('click', e => {
    if (e.target === lightbox) closeLightbox();
});

document.addEventListener('keydown', e => {
    if (!lightbox.classList.contains('active')) return;
    if (e.key === 'Escape')     closeLightbox();
    if (e.key === 'ArrowLeft')  prevPhoto();
    if (e.key === 'ArrowRight') nextPhoto();
});

// Attach lightbox to featured gallery items
document.querySelectorAll('#gallery-grid .gallery-item').forEach((item, i) => {
    item.addEventListener('click', () => openLightbox(featuredPhotos, i));
});

// ── Full gallery modal ───────────────────────────────────────
const viewAllBtn      = document.getElementById('view-all-btn');
const fullGallery     = document.getElementById('full-gallery');
const fullGalleryGrid = document.getElementById('full-gallery-grid');
const fullGalleryClose = document.getElementById('full-gallery-close');

function buildFullGallery() {
    if (fullGalleryGrid.children.length > 0) return; // already built
    allPhotos.forEach((src, i) => {
        const item = document.createElement('div');
        item.className = 'gallery-item';
        item.dataset.index = i;

        const img = document.createElement('img');
        img.src     = src;
        img.alt     = `Road Less Traveled — photo ${i + 1}`;
        img.loading = 'lazy';

        const overlay = document.createElement('div');
        overlay.className = 'gallery-overlay';
        overlay.innerHTML = '<span>View</span>';

        item.appendChild(img);
        item.appendChild(overlay);
        item.addEventListener('click', () => openLightbox(allPhotos, i));
        fullGalleryGrid.appendChild(item);
    });
}

viewAllBtn.addEventListener('click', () => {
    buildFullGallery();
    fullGallery.classList.add('active');
    document.body.style.overflow = 'hidden';
});

fullGalleryClose.addEventListener('click', () => {
    fullGallery.classList.remove('active');
    document.body.style.overflow = '';
});

document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && fullGallery.classList.contains('active')) {
        fullGallery.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// ── Smooth scroll offset for fixed nav ───────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
        const target = document.querySelector(anchor.getAttribute('href'));
        if (!target) return;
        e.preventDefault();
        const offset = navbar.offsetHeight + 8;
        const top    = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
    });
});
