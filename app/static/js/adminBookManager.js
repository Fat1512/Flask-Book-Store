const gerneList = document.getElementById("gerneList");
const gerneSearch = document.getElementById("gerneSearch");
const newGerneContainer = document.getElementById("newGerneContainer");
const newGerneInput = document.getElementById("newGerne");

// Fetch genres from backend and populate dropdown list
async function fetchGernes() {
    try {
        const response = await fetch('/api/gernes'); // Gọi API backend
        if (!response.ok) throw new Error('Failed to fetch gernes');

        const gernes = await response.json(); // Parse JSON từ API
        populateGerneList(gernes); // Nạp dữ liệu vào dropdown
    } catch (error) {
        console.error('Error fetching gernes:', error);
    }
}

// Populate gerne dropdown list
function populateGerneList(gernes, filter = "") {
    gerneList.innerHTML = ""; // Clear the list
    const filteredGernes = gernes.filter(gerne => gerne.name.toLowerCase().includes(filter.toLowerCase()));
    filteredGernes.forEach(gerne => {
        const item = document.createElement("div");
        item.classList.add("dropdown-item");
        item.textContent = gerne.name; // Hiển thị tên thể loại
        item.addEventListener("click", () => {
            gerneSearch.value = gerne.name;
            gerneList.style.display = "none";

            // Redirect to statistic page with gerne_id
            window.location.href = `/employee/book-manager?gerne_id=${gerne.id}`;
        });
        gerneList.appendChild(item);
    });
}

// Show dropdown list on click
gerneSearch.addEventListener("focus", () => {
    fetchGernes(); // Fetch và hiển thị danh sách đầy đủ
    gerneList.style.display = "block"; // Hiển thị dropdown
});

// Event listener cho tìm kiếm
gerneSearch.addEventListener("input", async () => {
    const response = await fetch('/api/gernes'); // Fetch lại gernes
    const gernes = await response.json();
    populateGerneList(gernes, gerneSearch.value); // Filter theo input
});

// Ẩn dropdown khi click ra ngoài
document.addEventListener("click", (event) => {
    if (!event.target.closest(".dropdown-container")) {
        gerneList.style.display = "none";
    }
});

// Form submission handler
document.addEventListener('DOMContentLoaded', function () {
    const formatList = document.getElementById("formatList");
    const formatSearch = document.getElementById("formatSearch");

    async function fetchFormats() {
        try {
            const response = await fetch('/api/formats'); // Gọi API backend để lấy enum
            if (!response.ok) throw new Error('Failed to fetch formats');

            const formats = await response.json(); // Parse JSON từ API
            populateFormatList(formats);
        } catch (error) {
            console.error('Error fetching formats:', error);
        }
    }

    function populateFormatList(formats, filter = "") {
        formatList.innerHTML = ""; // Clear the list
        const filteredFormats = formats.filter(format =>
        format.name.toLowerCase().includes(filter.toLowerCase())
        );

        filteredFormats.forEach(format => {
            const item = document.createElement("div");
            item.classList.add("dropdown-item");
            item.textContent = format.name;
            item.dataset.value = format.id; // Gắn ID định dạng vào dataset
            item.addEventListener("click", () => {
                formatSearch.value = format.name; // Hiển thị tên trong input
                formatSearch.dataset.value = format.id; // Lưu ID vào dataset
                formatList.style.display = "none";

                console.log(`Selected format: ${format.name} (ID: ${format.id})`);
            });
            formatList.appendChild(item);
        });
    }

    // Show dropdown list on focus
    formatSearch.addEventListener("focus", () => {
        fetchFormats(); // Fetch và hiển thị danh sách đầy đủ
        formatList.style.display = "block"; // Hiển thị dropdown
    });

    // Event listener cho tìm kiếm
    formatSearch.addEventListener("input", async () => {
        const response = await fetch('/api/formats'); // Fetch lại formats
        const formats = await response.json();
        populateFormatList(formats, formatSearch.value); // Filter theo input
    });

    // Ẩn dropdown khi click ra ngoài
    document.addEventListener("click", (event) => {
        if (!event.target.closest(".dropdown-container")) {
            formatList.style.display = "none";
        }
    });

    // Gửi dữ liệu đến backend
    document.querySelector('.update-btn').addEventListener('click', () => {
        const updatedFormatId = formatSearch.dataset.value; // Lấy ID từ dataset

        fetch('/api/update-format', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ format: updatedFormatId })
        })
            .then(response => response.json())
            .then(data => {
            if (data.success) {
                alert('Cập nhật thành công!');
            } else {
                alert(`Cập nhật thất bại: ${data.message || 'Unknown error'}`);
            }
        })
            .catch(error => console.error('Error updating format:', error));
    });
});







