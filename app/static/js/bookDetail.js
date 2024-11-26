const CART_API = '/api/v1/cart'
const CURRENT_URL = new URL(window.location);
const buttonAddCart = document.querySelector(".btn-add-cart")
buttonAddCart.addEventListener('click',() => addCartItem(CURRENT_URL.searchParams.get("bookId")))
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
        const result = await response.json(); // Parse JSON response
        alert(result.message);
    } catch (error) {
        alert('Failed to add cart.');
    }
}

const buttonOpenFormComment = document.querySelector('.form-comment-open')
const modal = document.querySelector(".modal")
buttonOpenFormComment.addEventListener('click', () =>
    modal.style = "display:flex"
)
const buttonCloseFormComment = document.querySelectorAll('.close-form')
buttonCloseFormComment.forEach(
    el => el.addEventListener('click', () => modal.style = "display:none"))

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
starElements.forEach(el => {
    let start = 0
    el.addEventListener('mouseenter', () => {
        start += 1
        renderStar(starElements, start)
    })
    el.addEventListener("mouseleave", () => {
        start -= 1
        renderStar(starElements, start)
    })
})

const renderStar = function (el, index) {
    let html = []
    for (let i = 0; i < el.length; i++) {
        if (i < index)
            html.push(`<span><i class="fa-solid fa-star text-medium"></i></span>`)
        else
            html.push(`<span><i class="fa-regular fa-star text-medium"></i></span>`)

    }
    ratingForm.innerHTML = html
}