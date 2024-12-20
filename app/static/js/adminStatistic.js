document.addEventListener('DOMContentLoaded', function () {
    // Đảm bảo rằng sự kiện click được đăng ký sau khi DOM đã sẵn sàng
    const exportButton = document.getElementById('exportPDF');
    if (exportButton) {
        exportButton.addEventListener('click', function () {
            const element = document.getElementById('statistic-table-pdf');

            if (!element) {
                alert("Không tìm thấy phần tử cần in PDF");
                return;
            }

//            element.style.display = 'block';

            // Cấu hình html2pdf
            const options = {
                margin: [20, 10, 10, 10], // Lề: Trên, trái, dưới, phải
                filename: 'ThongKe.pdf',
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 2, logging: true, useCORS: true },
                jsPDF: { unit: 'mm', format: 'a4', orientation: 'landscape' }, // PDF ngang
            };

            // Chuyển đổi HTML sang PDF
            html2pdf()
                .set(options)
                .from(element)
                .toPdf()
                .get('pdf')
                .then(function (pdf) {
                    // Lưu PDF mà không thêm logo và tiêu đề
                    pdf.save();
                })
                .catch((err) => {
                    console.error("Xuất PDF thất bại:", err);
                    alert("Xuất PDF thất bại. Vui lòng thử lại.");
                });
        });
    }
});


const gerneList = document.getElementById("gerneList");
const gerneSearch = document.getElementById("gerneSearch");
const newGerneContainer = document.getElementById("newGerneContainer");
const newGerneInput = document.getElementById("newGerne");

// Fetch genres from backend and populate dropdown list
async function fetchGernes() {
    try {
        const response = await fetch('/admin/api/gernes'); // Gọi API backend
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
            window.location.href = `/admin/statistic-frequency?gerne_id=${gerne.id}`;
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
    const response = await fetch('/admin/api/gernes'); // Fetch lại gernes
    const gernes = await response.json();
    populateGerneList(gernes, gerneSearch.value); // Filter theo input
});

// Ẩn dropdown khi click ra ngoài
document.addEventListener("click", (event) => {
    if (!event.target.closest(".dropdown-container")) {
        gerneList.style.display = "none";
    }
});

//// Form submission handler
//document.getElementById("bookForm").addEventListener("submit", function(event) {
//    event.preventDefault();
//
//    let selectedGerne = gerneSearch.value;
//    if (selectedGerne === "" && newGerneInput.value.trim() !== "") {
//        selectedGerne = newGerneInput.value.trim();
//        // Optionally, gửi thể loại mới lên server qua API POST (nếu cần)
//        console.log("New Gerne Added:", selectedGerne);
//    }
//
//    alert("Book added successfully!");
//    // Thêm logic xử lý form tại đây
//});





