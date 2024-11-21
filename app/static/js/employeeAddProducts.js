
    const menuData = {
      "Health": {
        "Văn Học": ["Tiểu Thuyết", "Truyện Ngắn - Tản Văn", "Tác Phẩm Kinh Điển", "Ngôn Tình", "Du Ký", "Hài Hước - Truyện Cười", "Tuổi Teen", "Sách Ảnh", "Truyện Tranh", "Thể Loại Khác"],
        "Kinh Tế": ["Quản Trị - Lãnh Đạo", "Nhân Vật - Bài Học Kinh doanh", "Marketing - Bán Hàng", "Khởi Nghiệp - Làm Giàu", "Phân Tích Kinh Tế", "Chứng Khoán - Bất Động Sản -  Đầu Tư", "Tài Chính - Ngân Hàng", "Nhân Sự - Việc Làm", "Kế Toán - Kiểm Toán - Thuế", "Ngoại Thương"],
        "Tâm Lý - Kỹ Năng Sống": ["Kỹ năng sống", "Tâm lý", "Sách cho tuổi mới lớn", "Chicken Soup - Hạt Giống Tâm Hồn", "Rèn luyện nhân cách"],
        "Nuôi Dạy Con": ["Cẩm Nang Làm Cha Mẹ", "Phát Triển Kỹ Năng - Trí Tuệ Cho Trẻ", "Phương Pháp Giáo Dục Trẻ Các Nước", "Dinh Dưỡng  - Sức Khỏe Cho Trẻ", "Giáo Dục Trẻ Tuổi Teen", "Dành Cho Mẹ Bầu"],
        "Sách Thiếu Nhi": ["Truyện Thiếu Nhi", "Kiến Thức - Kỹ Năng Sống Cho Trẻ", "Kiến thức bách khoa", "Tô màu, luyện chữ", "Từ Điển Thiếu Nhi", "Flashcard  - Thẻ Học Thông Minh", "Sách Nói"],
        "Tiểu Sử - Hồi Ký": ["Câu Chuyện Cuộc Đời", "Lịch Sử", "Nghệ Thuật - Giải Trí", "Chính Trị", "Kinh Tế", "Thể Thao"],
        "Giáo Khoa - Tham Khảo": ["Sách Tham Khảo", "Sách Giáo Khoa", "Mẫu Giáo", "Sách Giáo Viên", "Đại Học"],
        "Sách Học Ngoại Ngữ": ["Tiếng Anh", "Tiếng Hoa", "Tiếng Nhật", "Tiếng Hàn", "Tiếng Việt Cho Người Nước Ngoài", "Tiếng Pháp", "Tiếng Đức", "Ngoại Ngữ Khác"]
      }
    };

    let selectedPath = "";
    let activeColumn1 = null; // Track active item in column 1
    let activeColumn2 = null; // Track active item in column 2
    let activeColumn3 = null; // Track active item in column 3

    function openModal() {
      document.getElementById("modalOverlay").classList.add("active");
    }

    function closeModal() {
      document.getElementById("modalOverlay").classList.remove("active");
    }

    // Ngăn chặn sự kiện click trên nút "Open" hoặc các nút khác
    document.querySelectorAll('button').forEach(button => {
      button.addEventListener('click', (event) => {
        event.preventDefault(); // Ngăn hành vi mặc định, ví dụ: reload trang
      });
    });

    // Đảm bảo modal không tự tắt khi click bên trong nó
    document.getElementById("modalOverlay").addEventListener("click", (event) => {
      if (event.target === document.getElementById("modalOverlay")) {
        closeModal(); // Chỉ đóng khi click bên ngoài modal
      }
    });


    function toggleSubMenu(category, element) {
      const col2 = document.getElementById("col2");
      const col3 = document.getElementById("col3");

      // Reset column 3
      col3.innerHTML = '<p style="color: #aaa;">Chọn mục từ cột 2</p>';
      col3.classList.add("hidden");

      // Check if clicking on the same active item
      if (activeColumn1 === element) {
        col2.classList.add("hidden");
        activeColumn1.classList.remove("active");
        activeColumn1 = null;
        return;
      }

      // Highlight active item
      if (activeColumn1) activeColumn1.classList.remove("active");
      element.classList.add("active");
      activeColumn1 = element;

      // Load submenu for Column 2
      col2.innerHTML = "";
      col2.classList.remove("hidden");

      const subMenu = menuData[category];
      for (const key in subMenu) {
        const item = document.createElement("div");
        item.className = "menu-item";
        item.textContent = key;
        item.onclick = () => toggleFinalMenu(category, key, item);
        col2.appendChild(item);
      }

      selectedPath = category;
      updateSelectedDisplay();
    }

    function toggleFinalMenu(category, subCategory, element) {
      const col3 = document.getElementById("col3");

      // Check if clicking on the same active item
      if (activeColumn2 === element) {
        col3.classList.add("hidden");
        activeColumn2.classList.remove("active");
        activeColumn2 = null;
        return;
      }

      // Highlight active item
      if (activeColumn2) activeColumn2.classList.remove("active");
      element.classList.add("active");
      activeColumn2 = element;

      // Load submenu for Column 3
      col3.innerHTML = "";
      col3.classList.remove("hidden");

      const finalMenu = menuData[category][subCategory];
      finalMenu.forEach(item => {
        const menuItem = document.createElement("div");
        menuItem.className = "menu-item";
        menuItem.textContent = item;
        menuItem.onclick = () => selectFinalItem(category, subCategory, item, menuItem);
        col3.appendChild(menuItem);
      });

      selectedPath = `${category} > ${subCategory}`;
      updateSelectedDisplay();
    }

    function selectFinalItem(category, subCategory, item, menuItem) {
      // Highlight active item in column 3
      if (activeColumn3) activeColumn3.classList.remove("active");
      menuItem.classList.add("active");
      activeColumn3 = menuItem;

      selectedPath = `${category} > ${subCategory} > ${item}`;
      updateSelectedDisplay();
    }

    function updateSelectedDisplay() {
      document.getElementById("selectedPath").textContent = selectedPath;
    }

    function confirmSelection() {
      alert(`Bạn đã chọn: ${selectedPath}`);
      closeModal();
    }

    function filterMenuItems() {
      const searchInput = document.getElementById("searchInput").value.toLowerCase();
      const allMenuItems = document.querySelectorAll(".menu-item");
      allMenuItems.forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(searchInput) ? "block" : "none";
      });
    }

    // Genre list
    const genres = ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", "Biography", "Mystery"];
    const genreList = document.getElementById("genreList");
    const genreSearch = document.getElementById("genreSearch");
    const newGenreContainer = document.getElementById("newGenreContainer");
    const newGenreInput = document.getElementById("newGenre");

    // Populate genre dropdown list
    function populateGenreList(filter = "") {
        genreList.innerHTML = ""; // Clear the list
        const filteredGenres = genres.filter(genre => genre.toLowerCase().includes(filter.toLowerCase()));
        filteredGenres.forEach(genre => {
            const item = document.createElement("div");
            item.classList.add("dropdown-item");
            item.textContent = genre;
            item.addEventListener("click", () => {
                genreSearch.value = genre;
                genreList.style.display = "none";
                newGenreContainer.style.display = "none";
            });
            genreList.appendChild(item);
        });
        // Option to add a new genre
        const addNewOption = document.createElement("div");
        addNewOption.classList.add("dropdown-item");
        addNewOption.textContent = "+ Add New Genre";
        addNewOption.style.color = "#00bcd4";
        addNewOption.addEventListener("click", () => {
            genreSearch.value = "";
            genreList.style.display = "none";
            newGenreContainer.style.display = "flex";
            newGenreInput.focus();
        });
        genreList.appendChild(addNewOption);
        genreList.style.display = "block";
    }

    // Show dropdown list on click
    genreSearch.addEventListener("focus", () => {
        populateGenreList(); // Show full list when focused
        genreList.style.display = "block"; // Show the dropdown list
    });

    // Event listener for searching within the genre list
    genreSearch.addEventListener("input", () => {
        populateGenreList(genreSearch.value); // Filter list as user types
    });

    // Hide dropdown when clicking outside
    document.addEventListener("click", (event) => {
        if (!event.target.closest(".dropdown-container")) {
            genreList.style.display = "none";
        }
    });

    // Form submission handler
    document.getElementById("bookForm").addEventListener("submit", function(event) {
        event.preventDefault();

        let selectedGenre = genreSearch.value;
        if (selectedGenre === "" && newGenreInput.value.trim() !== "") {
            selectedGenre = newGenreInput.value.trim();
            genres.push(selectedGenre); // Add the new genre to the list
            populateGenreList();
        }

        alert("Book added successfully!");
        // Reset form fields if needed, or add form submission logic here
    });

