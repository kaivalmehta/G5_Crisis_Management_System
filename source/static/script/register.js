function togglePassword(id) {
    const passwordInput = document.getElementById(id);
    const toggleButton = passwordInput.nextElementSibling;
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleButton.textContent = "Hide";
    } else {
        passwordInput.type = "password";
        toggleButton.textContent = "Show";
    }
}

