document.addEventListener("DOMContentLoaded", function() {
    const navbarContainer = document.querySelector('.dashboard-navbar-container');
    const navLinks = document.querySelector('.nav-links');
    const menuToggle = document.createElement('div');

    // Create a toggle button for the mobile menu
    menuToggle.classList.add('menu-toggle');
    menuToggle.innerHTML = '<span>&#9776;</span>'; // Hamburger icon

    // Insert the toggle button into the navbar container
    navbarContainer.insertBefore(menuToggle, navLinks);

    // Toggle navbar links visibility on click
    menuToggle.addEventListener('click', function() {
        console.log("Toggle button clicked"); // Debugging log
        navLinks.classList.toggle('nav-open');
    });

    // Adjust layout based on window size
    function adjustLayout() {
        if (window.innerWidth < 768) {
            console.log("Mobile view detected"); // Debugging log
            navLinks.style.display = 'none';
        } else {
            console.log("Desktop view detected"); // Debugging log
            navLinks.style.display = 'flex';
            navLinks.classList.remove('nav-open'); // Remove any leftover classes
        }
    }

    // Run on page load and window resize
    adjustLayout();
    window.addEventListener('resize', adjustLayout);
});
document.addEventListener("DOMContentLoaded", function() {
    const tabs = document.querySelectorAll('.status-tab');
    const sections = document.querySelectorAll('.status-section');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and sections
            tabs.forEach(t => t.classList.remove('active'));
            sections.forEach(section => section.classList.remove('active'));

            // Add active class to the clicked tab and corresponding section
            tab.classList.add('active');
            document.getElementById(tab.getAttribute('data-status')).classList.add('active');
        });
    });
});
