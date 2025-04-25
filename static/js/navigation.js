document.addEventListener('DOMContentLoaded', function() {
  // Mobile menu toggle
  const mobileToggle = document.querySelector('.mobile-toggle');
  const menu = document.querySelector('.horizontal-menu');

  if (mobileToggle && menu) {
    mobileToggle.addEventListener('click', function() {
      // console.log('Hamburger clicked');
      menu.classList.toggle('active');
      // Optional: Close all dropdowns when main menu is toggled
      // dropdowns.forEach(function(dropdown) {
      //   dropdown.classList.remove('active');
      // });
    });
  }

  // Mobile dropdown toggle
  const dropdowns = document.querySelectorAll('.horizontal-menu .dropdown');

  dropdowns.forEach(function(dropdown) {
    // Find the specific trigger element within this dropdown
    // Use :scope to ensure we only get direct children if selecting .nav-link
    const trigger = dropdown.querySelector('.dropdown-button') || dropdown.querySelector(':scope > .nav-link');

    if (trigger) {
      // Attach listener directly to the trigger element
      trigger.addEventListener('click', function(event) { // 'this' now refers to the trigger element (button or link)
        // console.log('Dropdown trigger clicked:', this.textContent);

        // Only apply toggle logic for mobile view
        if (window.innerWidth <= 768) {
          // console.log('Processing click in mobile view');

          // Prevent default link behavior if it's just a trigger
          if (this.classList.contains('dropdown-button') || this.getAttribute('href') === '#') {
             event.preventDefault();
             // console.log('Default action prevented');
          }

          // Find the parent .dropdown element associated with this trigger
          const parentDropdown = this.closest('.dropdown');
          if (!parentDropdown) {
             // console.error('Could not find parent dropdown for trigger:', this);
             return; // Exit if we can't find the parent
          }

          // Check state before toggle
          // const isActiveBefore = parentDropdown.classList.contains('active');
          // console.log('Dropdown active state BEFORE toggle:', isActiveBefore);

          // Toggle the 'active' class on the PARENT .dropdown element
          parentDropdown.classList.toggle('active');

          // Check state after toggle
          // const isActiveAfter = parentDropdown.classList.contains('active');
          // console.log('Dropdown active state AFTER toggle:', isActiveAfter);


          // Close other dropdowns *only* if this one was just opened (is now active)
          if (parentDropdown.classList.contains('active')) {
             // console.log('Closing other active dropdowns...');
             dropdowns.forEach(function(otherDropdown) {
                // Check it's not the current dropdown and that it IS active
                if (otherDropdown !== parentDropdown && otherDropdown.classList.contains('active')) {
                   // console.log('Closing dropdown:', otherDropdown);
                   otherDropdown.classList.remove('active');
                }
             });
          }
        } else {
           // console.log('Click ignored in desktop view');
        }
      });
    } else {
       // console.log('No trigger found for dropdown:', dropdown);
    }
  });

  // Set active class for current page
  const currentPath = window.location.pathname;
  // Ensure trailing slashes are handled consistently for comparison
  const normalizedPath = currentPath.endsWith('/') ? currentPath : currentPath + '/';
  const navLinks = document.querySelectorAll('.nav-link');

  navLinks.forEach(function(link) {
    let href = link.getAttribute('href');
    // Normalize href similarly, assuming relative paths might lack trailing slash
    if (href && !href.startsWith('http') && !href.startsWith('#')) { // Avoid normalizing external links or # links
        href = href.endsWith('/') ? href : href + '/';
        // Special case for root index.html comparison
        if ((normalizedPath === '/' || normalizedPath === '/index.html/') && (href === './' || href === '/index.html/')) {
             link.classList.add('active');
        } else if (href !== './' && href !== '/index.html/' && normalizedPath.startsWith(href)) {
             link.classList.add('active');
             // Make parent dropdown active if child is active
             const parentDropdown = link.closest('.dropdown');
             if(parentDropdown) {
                const parentLink = parentDropdown.querySelector('.nav-link');
                if(parentLink) parentLink.classList.add('active');
             }
        }
    } else if (href === currentPath) { // Fallback for exact match if normalization fails
        link.classList.add('active');
    }
  });


  // Close menu when clicking outside
  document.addEventListener('click', function(e) {
    if (window.innerWidth <= 768) {
      // Check if the click is outside the main navigation AND outside the toggle button
      const navContainer = document.querySelector('.main-navigation'); // More specific container
      const isClickInsideNav = navContainer && navContainer.contains(e.target);
      const isClickOnToggle = mobileToggle && mobileToggle.contains(e.target);

      // Check if the menu itself exists and is active
      if (menu && menu.classList.contains('active') && !isClickInsideNav && !isClickOnToggle) {
        // console.log('Click outside nav detected, closing menu.');
        menu.classList.remove('active');

        // Also close any open dropdowns when clicking outside
        dropdowns.forEach(function(dropdown) {
          dropdown.classList.remove('active');
        });
      }
    }
  });

  // Reset on window resize
  window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
      // console.log('Resized to desktop, resetting mobile states.');
      // Remove any active classes added for mobile when resizing to desktop
      if (menu) {
        menu.classList.remove('active');
      }
      dropdowns.forEach(function(dropdown) {
        dropdown.classList.remove('active');
      });
    }
  });
});
