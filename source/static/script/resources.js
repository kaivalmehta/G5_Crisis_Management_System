let resourceIndex = 1; // Changed to resourceIndex
let editingRow = null; // To store the row being edited

// Show Add Resource Modal (used for both Add and Edit)
function showAddVolunteerModal(row = null) {
    if (row) {
        // If editing, populate the fields with existing data
        const cells = row.querySelectorAll('td');
        document.getElementById('volunteerName').value = cells[2].textContent;
        document.getElementById('resourceQuantity').value = cells[3].textContent;

        // Store the row for editing
        editingRow = row;
    } else {
        // Reset the modal if adding a new resource
        document.getElementById('volunteerName').value = '';
        document.getElementById('resourceQuantity').value = '';
        editingRow = null; // Reset the editing row
    }
    document.getElementById('addVolunteerModal').classList.add('show');
    document.querySelector('.modal-content').classList.add('show');
}

// Close Add/Edit Resource Modal
function closeAddVolunteerModal() {
    document.getElementById('addVolunteerModal').classList.remove('show');
    document.querySelector('.modal-content').classList.remove('show');
}

// Add or Edit Resource
function saveResource() {
    const name = document.getElementById('volunteerName').value;
    const quantity = document.getElementById('resourceQuantity').value;
    const tableBody = document.getElementById('volunteerList');
    const currentDate = new Date().toLocaleDateString();

    if (name && quantity && quantity > 0) {
        if (editingRow) {
            // If editing, update the existing row
            const cells = editingRow.querySelectorAll('td');
            cells[2].textContent = name;
            cells[3].textContent = quantity;
            cells[4].textContent = currentDate;
        } else {
            // If adding, create a new row
            const row = `
                <tr>
                    <td><input type="checkbox"></td>
                    <td>${resourceIndex++}</td>
                    <td>${name}</td>
                    <td>${quantity}</td>
                    <td>${currentDate}</td>
                    <td><button class="action-btn edit-btn" onclick="showAddVolunteerModal(this.closest('tr'))">Edit</button></td>
                </tr>
            `;
            tableBody.insertAdjacentHTML('beforeend', row);
        }

        closeAddVolunteerModal(); // Close the modal after saving
    } else {
        alert('Please fill out both fields and enter a valid quantity.');
    }
}

// Delete Selected Resources
function deleteSelectedVolunteers() {
    const checkboxes = document.querySelectorAll('#volunteerList input[type="checkbox"]:checked');
    checkboxes.forEach(checkbox => checkbox.closest('tr').remove());
}

// Toggle Select All Checkboxes
function toggleSelectAll(mainCheckbox) {
    const checkboxes = document.querySelectorAll('#volunteerList input[type="checkbox"]');
    checkboxes.forEach(checkbox => checkbox.checked = mainCheckbox.checked);
}
