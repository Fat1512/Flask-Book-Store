const CART_API = '/api/v1/cart'
const ACCOUNT_API = '/api/v1/account/'
const CURRENT_URL = new URL(window.location);
const buttonAddCart = document.querySelector(".btn-add-cart")
const buttonBuy = document.querySelector('.btn-buy')
let starCount = 0


buttonBuy.addEventListener('click', () => {
    addCartItem(CURRENT_URL.searchParams.get("bookId")).then(res => {
        if (res['status'] === 200)
            window.location.replace("http://127.0.0.1:5000/cart")
    })

})
buttonAddCart.addEventListener('click', () => addCartItem(CURRENT_URL.searchParams.get("bookId")))
const addCartItem = async function (id) {
    try {
        const response = await fetch(`${CART_API}/${id}`, {
            method: 'POST', // HTTP PUT method
            headers: {
                'Content-Type': 'application/json' // Specify JSON content type
            },
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        // Parse JSON response
        return await response.json()
    } catch (error) {
        alert('Failed to add cart.');
    }
}
const postComment = async function (data, url) {
    try {
        const response = await fetch(`${ACCOUNT_API}/${url}`, {
            method: 'POST', // HTTP PUT method
            headers: {
                'Content-Type': 'application/json' // Specify JSON content type
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json()
    } catch (error) {
        alert('Failed to post comment.');
    }
}

const buttonOpenFormComment = document.querySelector('.form-comment-open')
const modal = document.querySelector(".modal")
const commentForm = modal.querySelector('.comment-area')
const buttonModalComment = modal.querySelector('.btn-modal-comment')
buttonOpenFormComment.addEventListener('click', () =>
    modal.style = "display:flex"
)
buttonModalComment.addEventListener('click', () => {
    try {
        if (commentForm.value.trim() === '') throw new Error("Vui lòng nhập bình luận của bạn")
        if (starCount === 0) throw new Error("Vui lòng chọn đánh giá sao")
        data = {
            "comment": commentForm.value,
            'bookId': parseInt(CURRENT_URL.searchParams.get('bookId')),
            "starCount": starCount + 1
        }
        postComment(data, 'comment').then(res => {
            if (res['status'] === 200) {
                renderComment(res['data'])
                handleCloseFormComment()
            }
        })
    } catch (error) {
        Toastify({
            text: error.message,
            duration: 3000,
            newWindow: true,
            close: true,
            gravity: "top", // `top` or `bottom`
            position: "center", // `left`, `center` or `right`
            stopOnFocus: true, // Prevents dismissing of toast on hover
            style: {
                background: "var(--red)",
            }
        }).showToast();
    } finally {
        Toastify({
            text: 'Đánh giá của bạn đã được ghi nhận',
            duration: 3000,
            newWindow: true,
            close: true,
            gravity: "top", // `top` or `bottom`
            position: "center", // `left`, `center` or `right`
            stopOnFocus: true, // Prevents dismissing of toast on hover
            style: {
                background: "#6cbf6c",
            }
        }).showToast();
    }

})
const groupComment = document.querySelector('.group-comment')
const renderComment = function (data) {

    const groupOverview = document.querySelector('.overview')
    const starPercentList = groupOverview.querySelector('.star-percent').children
    let startArr = []
    const totalComment = parseInt(groupOverview.querySelector('.total-comment').getAttribute('length'))
    for (let i = 0; i < starPercentList.length; i++) {
        startArr[starPercentList.length - i - 1] = (Math.round((starPercentList[i].querySelector('.review-star-percent')
            .textContent.trim().split(' ')[0]) / 100 * totalComment))
    }
    startArr[data.star_count - 1] += 1

    const avg = Math.floor(startArr.reduce(
        (acc, currentValue, currentIndex) => acc + (currentValue * (currentIndex + 1)), 0) / (totalComment + 1))
    console.log(data, startArr, totalComment, Math.round(avg))
    const ratingLine = []
    for (let i = startArr.length - 1; i >= 0; i--) {
        ratingLine[i] = `
            <div class="d-flex align-items-center">
                    <p class="p-0 m-0">${i + 1} sao</p>
                    <div class="review-rating">
                        <div style="width: 0%;"></div>
                    </div>           
                        <div class="review-star"
                             style="width: calc(200px * ${startArr[i] / (totalComment + 1)});">
                            <div style="width: 0%;"></div>
                        </div>
               
                    <p class="p-0 m-0"> 
                            ${Math.round(startArr[i] / (totalComment + 1) * 100)}
                        %</p>
                </div>
    `
    }
    const overview = `
        <div>
            <p class="mb-2 text-large"><span class="font-weight-bold">${avg}</span>/5
            </p>
                ${'<i class="text-warning fa-solid fa-star"></i>'.repeat(avg)}
                ${'<i class="text-warning fa-regular fa-star"></i>'.repeat(5 - avg)}
            <p class="text-warning">(${totalComment + 1} đánh giá)</p>
        </div>
        <div class="star-percent position-relative ml-3">
            ${ratingLine.reverse().join('')}
        </div>
    `
    const html = `
     <div class="comment-item d-flex pt-3 pb-3">
        <div class="user-infor">
            <p class="user-infor-name">${data.user_name}</p>
            <p class="user-infor-post text-secondary">${new Date(data.created_at).toLocaleDateString('en-GB')}</p>
        </div>
        <div class="comment">
            <div class="rating">
                   ${'<i class="text-warning fa-solid fa-star"></i>'.repeat(data.star_count)}
                   ${'<i class="text-warning fa-regular fa-star"></i>'.repeat((5 - data.star_count))}
            </div>
            <p class="parent-comment m-0">
                ${data.content}
            </p>
        </div>
     </div>
    `
    groupComment.insertAdjacentHTML('beforebegin', html)
    groupOverview.innerHTML = overview
}
const buttonCloseFormComment = document.querySelectorAll('.close-form')

function handleCloseFormComment() {
    modal.style = "display:none"
    commentForm.value = ''
    renderStar(-1)
}

buttonCloseFormComment.forEach(
    el => el.addEventListener('click', () => handleCloseFormComment()))

const ratingForm = document.querySelector(".rating-form")
const starElements = ratingForm.querySelectorAll(".fa-regular.fa-star")
const moreDetail = document.querySelector(".item-more-detail")
let toggleMoreDetail = false
moreDetail.addEventListener('click', () => {
    if (!toggleMoreDetail) {
        document.querySelector(".block-gradient").style = "display: none"
        document.querySelector(".item-content").style = "overflow:none;max-height:100%"
    } else {
        document.querySelector(".block-gradient").style = "display: block"
        document.querySelector(".item-content").style = "overflow:hidden;max-height:300px"
    }
    toggleMoreDetail = !toggleMoreDetail
})

starElements.forEach((el, index) => {
    el.addEventListener('click', () => renderStar(index))
})
const renderStar = function (index) {
    starCount = index
    let html = []
    for (let i = 0; i < 5; i++) {
        if (i <= index)
            html.push(`<span><i onclick="renderStar(${i})" class="fa-solid fa-star text-medium"></i></span>`)
        else
            html.push(`<span><i onclick="renderStar(${i})" class="fa-regular fa-star text-medium"></i></span>`)

    }
    ratingForm.innerHTML = html.join('')
}