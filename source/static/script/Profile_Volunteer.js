document.getElementById("volunteerProfileForm").addEventListener("submit", function(event) {
    event.preventDefault();
    alert("Volunteer profile has been saved successfully!");
});


function validateForm(event) {
    event.preventDefault(); // Prevent form submission

    const contactNumber = document.getElementById("contactNumber").value;

    // Check if the contact number is a valid 10-digit number
    const contactRegex = /^\d{10}$/;
    if (!contactRegex.test(contactNumber)) {
        alert("Please enter a valid 10-digit contact number.");
        return;
    }

    // Submit form if all validations pass
    alert("Profile saved successfully!");
    document.getElementById("volunteerProfileForm").submit();
}
