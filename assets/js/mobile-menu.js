// Mobile Menu Toggle (for the checkbox-based CSS-only pattern with JS enhancement)
// This file handles mobile menu open/close and trap focus
(function() {
  const menuOverlay = document.getElementById('menu-overlay');
  const mobileMenu = document.getElementById('mobile-menu');
  const menuTrigger = document.querySelector('[aria-controls="mobile-menu"]');
  const menuClose = document.getElementById('menu-close-button');
  const navToggle = document.getElementById('navtoggle');
  const focusableElements = 'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])';

  function openMenu() {
    if (menuOverlay) {
      menuOverlay.classList.remove('hidden', 'opacity-0');
      menuOverlay.classList.add('opacity-100');
      menuOverlay.setAttribute('aria-hidden', 'false');
    }
    if (mobileMenu) {
      mobileMenu.classList.remove('translate-x-full');
      mobileMenu.setAttribute('aria-hidden', 'false');
      mobileMenu.removeAttribute('inert');
      trapFocus(mobileMenu);
    }
    if (menuTrigger) {
      menuTrigger.setAttribute('aria-expanded', 'true');
    }
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    if (menuOverlay) {
      menuOverlay.classList.add('opacity-0');
      menuOverlay.classList.remove('opacity-100');
      setTimeout(() => menuOverlay.classList.add('hidden'), 300);
      menuOverlay.setAttribute('aria-hidden', 'true');
    }
    if (mobileMenu) {
      mobileMenu.classList.add('translate-x-full');
      mobileMenu.setAttribute('aria-hidden', 'true');
      mobileMenu.setAttribute('inert', '');
    }
    if (menuTrigger) {
      menuTrigger.setAttribute('aria-expanded', 'false');
    }
    document.body.style.overflow = '';
  }

  function trapFocus(element) {
    const focusable = element.querySelectorAll(focusableElements);
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    
    element.addEventListener('keydown', function handleTab(e) {
      if (e.key !== 'Tab') return;
      if (e.shiftKey) {
        if (document.activeElement === first) {
          e.preventDefault();
          last.focus();
        }
      } else {
        if (document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    }, { once: false });
    
    if (first) first.focus();
  }

  // Event listeners
  if (navToggle) {
    navToggle.addEventListener('change', function() {
      if (this.checked) openMenu();
      else closeMenu();
    });
  }

  if (menuOverlay) {
    menuOverlay.addEventListener('click', closeMenu);
  }

  if (menuClose) {
    menuClose.addEventListener('click', closeMenu);
  }

  // Close on Escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && mobileMenu && !mobileMenu.classList.contains('translate-x-full')) {
      closeMenu();
      if (navToggle) navToggle.checked = false;
    }
  });

  // Close on resize to desktop
  window.addEventListener('resize', function() {
    if (window.innerWidth >= 768 && mobileMenu && !mobileMenu.classList.contains('translate-x-full')) {
      closeMenu();
      if (navToggle) navToggle.checked = false;
    }
  });

  // Sync checkbox with CSS peer-checked state on load
  if (navToggle && mobileMenu) {
    const isOpen = mobileMenu.classList.contains('peer-checked:block') || !mobileMenu.classList.contains('translate-x-full');
    navToggle.checked = isOpen;
  }
})();