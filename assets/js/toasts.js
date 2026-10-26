// Toast notification system
(function() {
  const container = document.getElementById('toast-container');
  if (!container) return;

  window.showToast = function(message, type = 'info', duration = 5000) {
    const toast = document.createElement('div');
    toast.className = 'pointer-events-auto flex items-center gap-3 rounded-xl border bg-white px-4 py-3 shadow-lg text-sm transition-all duration-300 transform translate-x-full opacity-0';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'polite');
    
    const colors = {
      info: 'border-indigo-200 text-indigo-800',
      success: 'border-emerald-200 text-emerald-800',
      warning: 'border-amber-200 text-amber-800',
      error: 'border-rose-200 text-rose-800'
    };
    
    const icons = {
      info: '<svg class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
      success: '<svg class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
      warning: '<svg class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zM12 15.75h.007v.008H12v-.008z"/></svg>',
      error: '<svg class="h-5 w-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
    };
    
    toast.classList.add(...colors[type].split(' '));
    toast.innerHTML = icons[type] + '<span class="flex-1">' + message + '</span>' + 
      '<button type="button" class="flex-shrink-0 p-1 rounded hover:bg-gray-100" aria-label="Dismiss"><svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button>';
    
    container.appendChild(toast);
    
    // Animate in
    requestAnimationFrame(() => {
      toast.classList.remove('translate-x-full', 'opacity-0');
    });
    
    // Auto dismiss
    const dismissTimer = setTimeout(() => dismissToast(toast), duration);
    
    // Manual dismiss
    toast.querySelector('button').addEventListener('click', () => {
      clearTimeout(dismissTimer);
      dismissToast(toast);
    });
    
    function dismissToast(el) {
      el.classList.add('translate-x-full', 'opacity-0');
      setTimeout(() => el.remove(), 300);
    }
  };
})();