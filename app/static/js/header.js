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

