// Function to assign a volunteer to the current logged-in user's organization
function assignToMyOrganization(volunteerId) {
    // Fetch the current logged-in user's organization
    fetch('/get_current_organization/')
        .then(response => response.json())
        .then(data => {
            if (data.organization) {
                const organizationId = data.organization.id;

                // Send an AJAX request to update the volunteer's organization
                fetch(`/assign_to_my_organization/${volunteerId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') // CSRF token for security
                    },
                    body: JSON.stringify({ organization_id: organizationId })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Volunteer assigned to your organization!');
                        location.reload(); // Reload the page to update the table
                    } else {
                        alert('Failed to assign volunteer. Please try again.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            } else {
                alert('You are not assigned to any organization.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Function to get the CSRF token (for security in AJAX requests)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
