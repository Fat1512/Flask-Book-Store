const SUGGEST_API = '/api/v1/search/suggest'
const searhButton = document.querySelector('.icon-search')
searhButton.addEventListener('click', (e) => {
    e.preventDefault()
    const keyword = document.querySelector('input[name="keyword"]').value
    window.location.href = `http://127.0.0.1:5000/search?keyword=${keyword}`
})

async function fetchSuggestBook(params) {
    try {
        const res = await fetch(`${SUGGEST_API}?${params}`)
        if (!res.ok) throw Error("Failed getting book")
        const data = await res.json()
        return data
    } catch (error) {

    } finally {
    }
}


const debounce = (callback, wait) => {
    let timeoutId = null;
    return (...args) => {
        window.clearTimeout(timeoutId);
        timeoutId = window.setTimeout(() => {
            callback(...args);
        }, wait);
    };
}


const cartLink = document.querySelector('.cart-link')
cartLink.addEventListener('click', (e) => {
    window.location.href = `http://127.0.0.1:5000/cart`
})
const searchInput = document.getElementById("search-desktop")
const suggestList = document.querySelector('.suggestion-list')
const suggestListBook = suggestList.querySelector('.suggestion-list-book')

const handleInputChange = debounce(async e => {
    const {data: books} = await fetchSuggestBook(`keyword=${e.target.value}`)
    if (!books.length) {
        suggestList.style = 'display:none'
        return
    }
    suggestList.style = 'display:flex'
    suggestListBook.innerHTML = books.map(b => `
        <a href="/search/detail?bookId=${b.book_id}" class="p-2 d-flex suggestion-list-book-item ">
            <img class="suggestion-list-book-image"
                 src="${b.book_image.length ? b.book_image[0].image_url : null}"/>
             <div class="ml-1 suggestion-list-book-title"> ${b.title}</div>
        </a>
    `).join('')
}, 500)
searchInput.addEventListener('input', handleInputChange)
document.body.addEventListener('click', (e) => {

    if ((!e.target.contains(suggestList) && e.target !== searchInput) || e.target.value.trim() === '') {
        suggestList.style = 'display:none'
    } else {
        suggestList.style = 'display:flex'
    }
})

//        const avatarInput = document.querySelector('#fileUpload');
//        updatedData.avt_url = avatarInput && avatarInput.files.length > 0
//            ? URL.createObjectURL(avatarInput.files[0])
//            : document.querySelector('#profileImage').src;
//
//        // Gửi dữ liệu tới server
//        fetch('/update-profile', {
//            method: 'POST',
//            headers: { 'Content-Type': 'application/json' },
//            body: JSON.stringify(updatedData)
//        })
//            .then(response => response.json())
//            .then(data => {
//                if (data.success) {
//                    alert('Cập nhật thành công!');
//                    document.querySelector('#profileImage').src = updatedData.avt_url;
//                } else {
//                    alert('Cập nhật thất bại: ' + (data.message || 'Lỗi không xác định'));
//                }
//            })
//            .catch(error => {
//                console.error('Error updating profile:', error);
//                alert('Đã xảy ra lỗi trong quá trình cập nhật.');
//            });
//    });
//
//    // Xử lý modal Hồ sơ
//    const modal = document.getElementById('profileModal');
//    const btn = document.getElementById('profileButton');
//    const span = document.getElementsByClassName('close')[0];
//
//    btn.onclick = function () {
//        modal.style.display = 'block';
//    };
//
//    span.onclick = function () {
//        modal.style.display = 'none';
//    };
//
//    window.onclick = function (event) {
//        if (event.target === modal) {
//            modal.style.display = 'none';
//        }
//    };
//});
//
//// Xử lý ảnh
//function previewImage(event) {
//    const file = event.target.files[0];
//    const reader = new FileReader();
//
//    reader.onload = function() {
//        const imageElement = document.getElementById('profileImage');
//        imageElement.src = reader.result;
//    }
//
//    if (file) {
//        reader.readAsDataURL(file);
//    }
//}