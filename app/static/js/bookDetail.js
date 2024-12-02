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
    data = {
        "comment": commentForm.value,
        'bookId': parseInt(CURRENT_URL.searchParams.get('bookId')),
        "starCount": starCount
    }
    postComment(data, 'comment').then(res => {
        if (res['status'] === 200) {
            alert("ok")
        }
    })
})
const buttonCloseFormComment = document.querySelectorAll('.close-form')
buttonCloseFormComment.forEach(
    el => el.addEventListener('click', () => {
        modal.style = "display:none"
        commentForm.value = ''
        renderStar(-1)
    }))

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
const groupComment = document.querySelector('.group-comment')
const commentList = document.querySelectorAll('.comment-item')
commentList.forEach(el => {
    const buttonReply = el.querySelector('.btn-comment-reply')
    const buttonShowMore = el.querySelector('.btn-comment-more')
    const groupButton = el.querySelector('.comment-controll-group-btn')
    const buttonSend = el.querySelector('.icon-send')
    const subComment = el.querySelector(".sub-comment")
    toggle = false
    buttonReply.addEventListener('click', () => {
        if (!toggle)
            el.querySelector('.input-text').style = 'display:block'
        else {
            el.querySelector('.input-text').style = 'display:none'
            el.querySelector("#review_field").value = ''
        }
        toggle = !toggle
    })
    buttonSend.addEventListener('click', () => {
        data = {
            "parentId": parseInt(el.id),
            'comment': el.querySelector("#review_field").value
        }
        postComment(data, "reply").then(res => {
            if (res['status'] === 200) {

            }
        })
    })
})