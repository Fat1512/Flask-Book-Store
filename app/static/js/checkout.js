document.querySelectorAll('input[name="address"]').forEach((radio) => {
    radio.addEventListener('change', (e) => {
        const prev = document.querySelector(".active")
        prev.classList.remove("active")
        const activeAddress = document.getElementById(e.target.value)
        activeAddress.classList.add("active")
    });
})
const listAddress = document.querySelector('.list-address')
const addressArea = document.querySelector('.select-address')
const inputAddress = document.querySelector(".input-address")
listAddress.querySelectorAll(".address-item").forEach(el =>
    el.addEventListener("click", () => {
        prev = document.querySelector(".address-item.active-address")
        if (prev)
            prev.classList.remove("active-address")
        el.classList.add('active-address')
        inputAddress.value = el.textContent
        listAddress.style = 'display:none; opacity:0'
    })
)
addressArea.addEventListener("click", (e) => {
    function handleClickOutSide(e) {
        if (e.target === listAddress || e.target === inputAddress) {
            return false
        }
        listAddress.style = 'display:none; opacity:0'
        inputAddress.value = ''
        return true
    }

    document.body.addEventListener("click", (e) => {
        handleClickOutSide(e) && document.body.removeEventListener('click', handleClickOutSide)
    })
    if (e.target === inputAddress) {
        listAddress.style = 'display:block; opacity:1'
    }
})
