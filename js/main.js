// Zatoka Cydrowa — lekki JS bez zależności

document.addEventListener('DOMContentLoaded', function () {
  // Mobile nav toggle
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.querySelector('.mobile-menu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var isOpen = menu.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      toggle.textContent = isOpen ? '\u2715' : '\u2630';
    });
    menu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        menu.classList.remove('is-open');
        toggle.textContent = '\u2630';
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Reveal on scroll
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealEls.length) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(function (el) { observer.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  }

  // Footer year
  var yearEl = document.getElementById('year');
  if (yearEl) { yearEl.textContent = new Date().getFullYear(); }

  // Lightbox: zoom on tap/click, swipe to navigate, arrows/keyboard as fallback
  var lightbox = document.getElementById('lightbox');
  if (lightbox) {
    var images = [];
    try { images = JSON.parse(lightbox.getAttribute('data-images') || '[]'); } catch (e) { images = []; }
    var currentIndex = 0;
    var imgEl = document.getElementById('lightbox-img');
    var counterEl = document.getElementById('lightbox-counter');

    function updateLightbox() {
      if (!images.length || !imgEl) return;
      imgEl.classList.remove('is-zoomed');
      imgEl.src = images[currentIndex];
      if (counterEl) { counterEl.textContent = 'Zdjęcie ' + (currentIndex + 1) + ' / ' + images.length; }
    }
    window.openLightbox = function (e, i) {
      if (e) { e.preventDefault(); }
      currentIndex = i;
      updateLightbox();
      lightbox.classList.add('is-open');
      return false;
    };
    window.closeLightbox = function () { lightbox.classList.remove('is-open'); };
    window.nextImage = function () { currentIndex = (currentIndex + 1) % images.length; updateLightbox(); };
    window.prevImage = function () { currentIndex = (currentIndex - 1 + images.length) % images.length; updateLightbox(); };

    document.addEventListener('keydown', function (ev) {
      if (!lightbox.classList.contains('is-open')) { return; }
      if (ev.key === 'Escape') { window.closeLightbox(); }
      if (ev.key === 'ArrowRight') { window.nextImage(); }
      if (ev.key === 'ArrowLeft') { window.prevImage(); }
    });

    // Tap/click the photo to zoom in and out
    if (imgEl) {
      imgEl.addEventListener('click', function (ev) {
        ev.stopPropagation();
        imgEl.classList.toggle('is-zoomed');
      });
    }

    // Swipe left/right to move through the slideshow (like a standard gallery)
    var touchStartX = null;
    var touchStartY = null;
    var stage = lightbox.querySelector('.lightbox__stage');
    if (stage) {
      stage.addEventListener('touchstart', function (ev) {
        if (ev.touches.length !== 1) { return; }
        touchStartX = ev.touches[0].clientX;
        touchStartY = ev.touches[0].clientY;
      }, { passive: true });
      stage.addEventListener('touchend', function (ev) {
        if (touchStartX === null) { return; }
        var dx = ev.changedTouches[0].clientX - touchStartX;
        var dy = ev.changedTouches[0].clientY - touchStartY;
        touchStartX = null;
        if (imgEl && imgEl.classList.contains('is-zoomed')) { return; }
        if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) {
          if (dx < 0) { window.nextImage(); } else { window.prevImage(); }
        }
      }, { passive: true });
    }

    // Clicking the dark backdrop (not the photo itself) closes the lightbox
    lightbox.addEventListener('click', function (ev) {
      if (ev.target === lightbox || ev.target === stage) { window.closeLightbox(); }
    });
  }
});
