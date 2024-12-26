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
                this.backgroundColor = '#2dce89';
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
    saveButton.addEventListener('click', async function () {
        const updatedData = {};

        // Thu thập dữ liệu từ các trường input
        updatedData.first_name = document.querySelector('#first_name').value;
        updatedData.last_name = document.querySelector('#last_name').value;
        updatedData.email = document.querySelector('#email').value;
        updatedData.phone_number = document.querySelector('#phone').value;

        const gender = document.querySelector('input[name="gender"]:checked').value;
        updatedData.sex = gender === 'Nam' ? 1 : gender === 'Nữ' ? 0 : 0;

        updatedData.date_of_birth = `${document.querySelector('#year').value}-${document.querySelector('#month').value}-${document.querySelector('#day').value}`;

        updatedData.password = document.querySelector('#password').value;
        updatedData.newpassword = document.querySelector('#newpassword').value;
        updatedData.confirm = document.querySelector('#confirm').value;


        const avatarInput = document.querySelector('#fileUpload');
        updatedData.avt_url = avatarInput && avatarInput.files.length > 0
            ? avt_image
            : null

        const formData = new FormData()
        for (const key in updatedData) {
            if (updatedData.hasOwnProperty(key)) {
                // For all other fields, append as a string or number
                formData.append(key, updatedData[key]);
            }
        }

        // Gửi dữ liệu tới server
        await fetch('/update-profile', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                avt_image = null
                document.querySelector('#passwordError').style.display = 'none';
                document.querySelector('#confirmError').style.display = 'none';
                const changePass = document.getElementById('change-pass');


                if (data.success) {
                    if (changePass.textContent === 'Đóng') {
                        if (!updatedData.password || !updatedData.newpassword || !updatedData.confirm) {
                            alert('Vui lòng nhập đầy đủ thông tin');
                            return;
                        }
                    }

                    alert('Cập nhật thành công!');
                    document.querySelector('#profileImage').src = updatedData.avt_url;

                    const changeInputPass1 = document.querySelector('.change-pass-1');
                    const changeInputPass2 = document.querySelector('.change-pass-2');
                    const changeInputPass3 = document.querySelector('.change-pass-3');

                    changeInputPass1.style.display = 'none';
                    changeInputPass2.style.display = 'none';
                    changeInputPass3.style.display = 'none';

                    changePass.textContent = 'Đổi mật khẩu';
                } else {
                    if (data.message === 'Mật khẩu hiện tại không chính xác') {
                        document.querySelector('#passwordError').style.display = 'block';
                    } else if (data.message === 'Mật khẩu không trùng khớp') {
                        document.querySelector('#confirmError').style.display = 'block';
                    } else {
                        // alert('Cập nhật thất bại: ' + (data.message || 'Lỗi không xác định'));
                    }
                    throw new Error('Cập nhật thất bại')
                }
            })
            .then(() => {
                window.location.reload();
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
let avt_image;

// Xử lý ảnh
function previewImage(event) {
    const file = event.target.files[0];
    avt_image = file
    const reader = new FileReader();

    reader.onload = function () {
        const imageElement = document.getElementById('profileImage');
        imageElement.src = reader.result;
    }

    if (file) {
        reader.readAsDataURL(file);
    }
}