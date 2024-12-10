const searhButton = document.querySelector('.icon-search')
searhButton.addEventListener('click', (e) => {
    e.preventDefault()
    const keyword = document.querySelector('input[name="keyword"]').value
    window.location.href = `http://127.0.0.1:5000/search?keyword=${keyword}`
})
const cartLink = document.querySelector('.cart-link')
cartLink.addEventListener('click', (e) => {
    window.location.href = `http://127.0.0.1:5000/cart`
})
const searchInput = document.getElementById("search-desktop")
// console.log(searchInput)
// searchInput.addEventListener('keydown', (e) => {
//     if (e.key === "Enter") {
//         const keyword = document.querySelector('input[name="keyword"]').value
//         window.location.href = `http://127.0.0.1:5000/search?keyword=${keyword}`
//     }
// })

document.addEventListener('DOMContentLoaded', function () {
    // Xử lý chỉnh sửa email và số điện thoại
    function handleEditButton(inputId, buttonClass) {
        document.querySelector(buttonClass).addEventListener('click', function (event) {
            event.preventDefault(); // Ngăn chặn hành vi mặc định của nút

            const inputElement = document.getElementById(inputId);
            if (inputElement.disabled) {
                inputElement.disabled = false;
                inputElement.focus();
                this.textContent = 'Xác nhận';
                this.classList.remove('btn-primary');
                this.classList.add('btn-success');
            } else {
                const newValue = inputElement.value.trim();
                if (!newValue) {
                    alert(`${inputId === 'email' ? 'Email' : 'Số điện thoại'} không được để trống!`);
                    inputElement.focus();
                    return;
                }

                console.log(`${inputId === 'email' ? 'Email mới' : 'Số điện thoại mới'}:`, newValue);
                inputElement.disabled = true;
                this.textContent = 'Sửa';
                this.classList.remove('btn-success');
                this.classList.add('btn-primary');
            }
        });
    }

    handleEditButton('phone', '.edit-btn-phone');
    handleEditButton('email', '.edit-btn-email');

    // Xử lý lưu thông tin người dùng
    const saveButton = document.querySelector('.btn-save');
    saveButton.addEventListener('click', function () {
        const updatedData = {};

        // Thu thập dữ liệu từ các trường input
        updatedData.first_name = document.querySelector('#first_name').value;
        updatedData.last_name = document.querySelector('#last_name').value;
        updatedData.email = document.querySelector('#email').value;
        updatedData.phone_number = document.querySelector('#phone').value;

        const gender = document.querySelector('input[name="gender"]:checked').value;
        updatedData.sex = gender === 'Nam' ? 1 : gender === 'Nữ' ? 0 : null;

        updatedData.date_of_birth = `${document.querySelector('#year').value}-${document.querySelector('#month').value}-${document.querySelector('#day').value}`;

        const avatarInput = document.querySelector('#fileUpload');
        updatedData.avt_url = avatarInput && avatarInput.files.length > 0
            ? URL.createObjectURL(avatarInput.files[0])
            : document.querySelector('#profileImage').src;

        // Gửi dữ liệu tới server
        fetch('/update-profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedData)
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Cập nhật thành công!');
                    document.querySelector('#profileImage').src = updatedData.avt_url;
                } else {
                    alert('Cập nhật thất bại: ' + (data.message || 'Lỗi không xác định'));
                }
            })
            .catch(error => {
                console.error('Error updating profile:', error);
                alert('Đã xảy ra lỗi trong quá trình cập nhật.');
            });
    });

    // Xử lý modal Hồ sơ
    const modal = document.getElementById('profileModal');
    const btn = document.getElementById('profileButton');
    const span = document.getElementsByClassName('close')[0];

    btn.onclick = function () {
        modal.style.display = 'block';
    };

    span.onclick = function () {
        modal.style.display = 'none';
    };

    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };
});

// Xử lý ảnh
function previewImage(event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function() {
        const imageElement = document.getElementById('profileImage');
        imageElement.src = reader.result;
    }

    if (file) {
        reader.readAsDataURL(file);
    }
}