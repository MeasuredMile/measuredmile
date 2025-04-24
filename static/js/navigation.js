document.addEventListener('DOMContentLoaded', function() {
  // Mobile menu toggle
  const mobileToggle = document.querySelector('.mobile-toggle');
  const menu = document.querySelector('.horizontal-menu');
  
  if (mobileToggle && menu) {
    mobileToggle.addEventListener('click', function() {
      menu.classList.toggle('active');
    });
  }
  
  // Mobile dropdown toggle
  const dropdowns = document.querySelectorAll('.dropdown');
  
  dropdowns.forEach(function(dropdown) {
    const button = dropdown.querySelector('.dropdown-button');
    
    if (button) {
      button.addEventListener('click', function(e) {
        // Only for mobile
        if (window.innerWidth <= 768) {
          e.preventDefault();
          dropdown.classList.toggle('active');
          
          // Close other dropdowns
          dropdowns.forEach(function(other) {
            if (other !== dropdown) {
              other.classList.remove('active');
            }
          });
        }
      });
    }
  });
  
  // Set active class for current page
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(function(link) {
    const href = link.getAttribute('href');
    if (href === currentPath || 
        (href !== '/' && currentPath.startsWith(href))) {
      link.classList.add('active');
    }
  });
  
  // Close menu when clicking outside
  document.addEventListener('click', function(e) {
    if (window.innerWidth <= 768) {
      const nav = document.querySelector('.main-navigation');
      if (nav && !nav.contains(e.target)) {
        menu.classList.remove('active');
        
        // Close all dropdowns
        dropdowns.forEach(function(dropdown) {
          dropdown.classList.remove('active');
        });
      }
    }
  });
  
  // Reset on window resize
  window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
      // Remove any active classes added for mobile
      menu.classList.remove('active');
      
      dropdowns.forEach(function(dropdown) {
        dropdown.classList.remove('active');
      });
    }
  });
});