document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("navbar").innerHTML = `
        <header class="navbar">
            <div class="navbar-container">
                <div class="logo">
                    <img src="logo.png" alt="Logo">
                    <span class="org-name">Crisis Management</span>
                </div>
                <nav class="nav-links">
                    <a href="#">Home</a>
                    <a href="#">Login</a>
                    <a href="#">Incidents</a>
                    <a href="#">About Us</a>
                    <a href="#">Contact Us</a>
                    <a href="#" class="donate-btn">Donate</a>
                </nav>
            </div>
        </header>
    `;
});
