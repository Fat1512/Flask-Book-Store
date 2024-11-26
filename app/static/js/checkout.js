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
document.body.addEventListener('click', e => handleClickOutSide(e))

function handleClickOutSide(e) {
    if (addressArea && addressArea.contains(e.target)) {
        return
    }
    listAddress.style = 'display:none; opacity:0'
    if (!document.querySelector(".address-item.active-address"))
        inputAddress.value = ''

}

addressArea.addEventListener("click", (e) =>
    listAddress.style = 'display:block; opacity:1'
)
const paymentArea = document.querySelector(".select-payment")
paymentArea.addEventListener('click', () => {
    document.querySelector('.modal').style = 'display:flex'
})
const closeModalButton = document.querySelector(".close-form")
closeModalButton.addEventListener('click', () => {
    document.querySelector('.modal').style = 'display:none'
})
const confirmButton = document.querySelector('.payment-confirm')
confirmButton.addEventListener('click', () => {
    const paymentIcon = document.querySelector('.payment-icon')
    const paymentText = document.querySelector('.payment-text')
    const method = document.querySelector('.payment-method-item-active')

    paymentIcon.innerHTML = method.querySelector('.payment-method-item-icon img').outerHTML
    paymentText.innerHTML = method.querySelector('.payment-method-item-text').textContent

    document.querySelector('.modal').style = 'display:none'
})
const methodList = document.querySelectorAll('.payment-method-item')
methodList.forEach(el => {
    el.addEventListener('click', () => {
        const prev = document.querySelector('.payment-method-item-active')
        if (prev) {
            prev.classList.remove('payment-method-item-active')
            prev.querySelector('.payment-item-tick').style = 'display:none'
        }
        el.classList.add('payment-method-item-active')
        el.querySelector('.payment-item-tick').style = 'display:block'
    })
})
const addressUserList = document.querySelectorAll('.address-user')

addressUserList.forEach(addressUser => {
    addressUser.addEventListener('click', (e) => {
        e.preventDefault()
        let prev = document.querySelector('input[name="address-item"]:checked')
        if (prev) {
            prev.checked = false
        }
        console.log(e.target)
        addressUser.querySelector('input[name="address-item"]').checked = true
    })
})