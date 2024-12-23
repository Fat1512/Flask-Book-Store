// DOM Elements
const roleList = document.getElementById("roleList");
const roleSearch = document.getElementById("roleSearch");
const statsContainer = document.getElementById("statsContainer"); // Element hiển thị kết quả

// Mảng ánh xạ giữa tên vai trò và ID vai trò
const roleMap = {
    "admin": 1,
    "customer": 2,
    "employee_sale": 4,
    "employee_manager_warehouse": 5,
    "employee_manager": 6
};

// Fetch user roles from backend and populate dropdown list
async function fetchUserRoles() {
    try {
        const response = await fetch('/api/user_roles');
        if (!response.ok) throw new Error('Failed to fetch user roles');

        const userRoles = await response.json();
        populateRoleList(userRoles); // Populate dropdown
    } catch (error) {
        console.error('Error fetching user roles:', error);
    }
}

// Populate role dropdown list
function populateRoleList(userRoles, filter = "") {
    roleList.innerHTML = ""; // Clear dropdown
    const filteredRoles = userRoles.filter(role =>
        role.user_role.toLowerCase().includes(filter.toLowerCase()) // Filter roles based on search input
    );

    filteredRoles.forEach(role => {
        const item = document.createElement("div");
        item.classList.add("dropdown-item");
        item.textContent = role.user_role;
        item.addEventListener("click", () => {
            roleSearch.value = role.user_role;
            roleList.style.display = "none";

            // Redirect to the same page but with updated user_role in URL
            const roleId = roleMap[role.user_role.toLowerCase()]; // Get the role ID from map
            window.location.href = `/admin/account-manager?user_role=${roleId}`; // Navigate with new URL
        });
        roleList.appendChild(item);
    });
}

// Fetch user data based on selected role (from URL)
async function filterUsersByRole(selectedRoleId) {
    const response = await fetch(`/api/account-manager?user_role=${selectedRoleId}`);
    if (response.ok) {
        const data = await response.json();
        renderUserStats(data); // Render the filtered user stats
    } else {
        console.error('Failed to fetch filtered user data');
    }
}

// Render user stats in the table
function renderUserStats(data) {
    statsContainer.innerHTML = ""; // Clear previous stats
    if (data.stats) {
        data.stats.forEach(stat => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${stat.user_id}</td>
                <td>${stat.first_name}</td>
                <td>${stat.last_name}</td>
                <td>${stat.username}</td>
                <td>${stat.email}</td>
                <td>${stat.user_role}</td>
            `;
            statsContainer.appendChild(row);
        });
    }
}

// Show dropdown list on focus
roleSearch.addEventListener("focus", () => {
    fetchUserRoles(); // Fetch user roles from backend
    roleList.style.display = "block"; // Show dropdown
});

// Event listener for search input
roleSearch.addEventListener("input", async () => {
    const response = await fetch('/api/user_roles');
    const userRoles = await response.json();
    populateRoleList(userRoles, roleSearch.value); // Filter roles based on search input
});

// Hide dropdown when clicking outside
document.addEventListener("click", (event) => {
    if (!event.target.closest(".dropdown-container")) {
        roleList.style.display = "none";
    }
});

// Check URL on page load to auto-load filtered users if URL contains 'user_role'
function checkAndFilterUsersByRole() {
    const urlParams = new URLSearchParams(window.location.search);
    const userRole = urlParams.get('user_role');
    if (userRole) {
        filterUsersByRole(userRole); // Filter users based on the selected role when page loads
    }
}

// Check URL on page load
window.addEventListener("DOMContentLoaded", checkAndFilterUsersByRole);

// Cập nhật lại dữ liệu khi URL thay đổi (khi người dùng điều hướng trang)
window.addEventListener('popstate', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const userRole = urlParams.get('user_role');
    if (userRole) {
        filterUsersByRole(userRole); // Fetch and render filtered users when back/forward button is used
    }
});