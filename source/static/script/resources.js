function deleteResource(resourceID) {
    if (confirm("Are you sure you want to delete this resource?")) {
        fetch(`/delete_resource/${resourceID}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json",
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    // Remove the deleted resource row from the table
                    const row = document.querySelector(`tr[data-id='${resourceID}']`);
                    if (row) {
                        row.remove();
                    }
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error("Error:", error));
    }
}

// Helper function to get the CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
    fetch("/", {
        method: "GET",
    });
});
