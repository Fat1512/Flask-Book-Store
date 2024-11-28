const CART_API = '/cart/clear_session'
const ORDER_API = '/api/v1/order'
const PAYMENT_API = '/api/v1/payment'

const VND = new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
});

function extractCurrencyNumber(currencyString) {
    const numericValue = currencyString.replace(/[^\d,]/g, ''); // Keep digits and comma
    return parseFloat(numericValue.replace(',', '.')); // Convert to float, replace comma with dot
}

const payment = async function (params) {
    console.log(params)
    try {
        const resPayment = await fetch(`${PAYMENT_API}/?orderId=${params}`, {
            method: 'POST', // HTTP PUT method
            headers: {
                'Content-Type': 'application/json' // Specify JSON content type
            },
        });
        if (!resPayment.ok) {
            throw new Error(`HTTP error! status: ${resPayment.status}`);
        }
        const result = await resPayment.json(); // Parse JSON response
        if (!resPayment.ok) {
            throw new Error(`HTTP error! status: ${resPayment.status}`);
        }
        console.log(result)
        window.location.replace(result['vnpay_url'])

    } catch (error) {
        alert('Failed to payment.');
    }
}

const createOrder = async function (data) {
    try {
        const response = await fetch(`${ORDER_API}/onlineOrder`, {
            method: 'POST', // HTTP PUT method
            headers: {
                'Content-Type': 'application/json' // Specify JSON content type
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json(); // Parse JSON response
        if (result.status === 200) {
            if (data['paymentMethod'] === 'inperson')
                window.location.replace('http://127.0.0.1:5000/cart')
            else {
                await payment(result['orderId'])
            }
        }
    } catch (error) {
        alert('Failed to delete cart.');
    }
}


document.querySelectorAll('input[name="address"]').forEach((radio) => {
    radio.addEventListener('change', (e) => {
        const prev = document.querySelector(".active")
        prev.classList.remove("active")
        const activeAddress = document.getElementById(e.target.value)
        activeAddress.classList.add("active")
    });
})
window.addEventListener("beforeunload", function (event) {
    // Send a fetch request to destroy the session
    // navigator.sendBeacon(CART_API);
});
const listAddress = document.querySelector('.list-address')
const addressArea = document.querySelector('.select-address')
const inputAddress = document.querySelector(".input-address")
listAddress.querySelectorAll(".address-item").forEach(el =>
    el.addEventListener("click", (e) => {
        e.stopPropagation()
        let prev = document.querySelector(".address-item.active-address")
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
    else
        inputAddress.value = document.querySelector(".address-item.active-address").textContent

}

addressArea.addEventListener("click", (e) => {
        listAddress.style = 'display:block; opacity:1'
    }
)
const modalPayment = document.querySelector('.modal-payment')
const paymentArea = document.querySelector(".select-payment")
paymentArea.addEventListener('click', () => {
    modalPayment.style = 'display:flex'
})
const closeModalButton = modalPayment.querySelector(".close-form")
closeModalButton.addEventListener('click', () => {
    modalPayment.style = 'display:none'
})
const confirmButton = document.querySelector('.payment-confirm')
confirmButton.addEventListener('click', () => {
    const paymentIcon = document.querySelector('.payment-icon')
    const paymentText = document.querySelector('.payment-text')
    const method = document.querySelector('.payment-method-item-active')

    paymentArea.classList.add('select-payment-tick')
    paymentArea.setAttribute('value', method.getAttribute('value'))
    paymentIcon.innerHTML = method.querySelector('.payment-method-item-icon img').outerHTML
    paymentText.innerHTML = method.querySelector('.payment-method-item-text').textContent
    if (method.getAttribute('value') === 'VNPay') {
        document.querySelector('.ship-fee').textContent = '0 đ'
        document.querySelector('.final-price').textContent =
            VND.format(extractCurrencyNumber(document.querySelector('.final-price').textContent) - 30000)
    }
    modalPayment.style = 'display:none'
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
const modalAddress = document.querySelector('.modal-address')

function handleCloseForm() {
    modalAddress.style = 'display:none'
}

modalAddress.querySelector('.close-form').addEventListener('click', () => handleCloseForm())
modalAddress.querySelector('.btn-back').addEventListener('click', () => handleCloseForm())
addressUserList.forEach(addressUser => {
    const buttonUpdate = addressUser.querySelector(".update-link")
    buttonUpdate.addEventListener('click', () => modalAddress.style = 'display:flex')
    addressUser.addEventListener('click', (e) => {
        e.preventDefault()
        let prev = document.querySelector('input[name="address-item"]:checked')
        if (prev) {
            prev.checked = false
        }
        addressUser.querySelector('input[name="address-item"]').checked = true
    })
})

const handleCreateOrder = async function () {
    const inputAddress = document.getElementById('address')
    const checked = document.querySelector("input[name='address']:checked")
    const addressItem = document.querySelectorAll('.address-user')
    const isChekedPayment = document.querySelector('.select-payment.select-payment-tick')
    const policyCheckbox = document.querySelector('input[name="accept-policy"]')
    let addressSelected
    try {
        if (checked.getAttribute('value') === 'inperson') {
            if (inputAddress.value.trim() === '')
                throw Error("Addres null")
            else
                addressSelected = document.querySelector('.address-item.active-address')
                    .getAttribute('value')
        } else {
            isChecked = false
            for (let i = 0; i < addressItem.length; i++) {
                if (addressItem[i].querySelector("input[name='address-item']").checked) {
                    addressSelected = addressItem[i].getAttribute('value')
                    isChecked = true
                    break
                }
            }
            if (!isChecked)
                throw Error("Addres null")
        }
        if (!isChekedPayment)
            throw Error('payment null')
        if (!policyCheckbox.checked)
            throw Error("ok")

        const books = []
        document.querySelectorAll('.book-item').forEach(item => {
            book = {
                'bookId': parseInt(item.getAttribute('id')),
                'quantity': parseInt(item.querySelector('.book-item-quantity').textContent),
                'finalPrice': extractCurrencyNumber(item.querySelector('.book-item-price').textContent)
            }
            books.push(book)
        })

        let data = {
            "addressId": addressSelected,
            'shippingMethod': checked.getAttribute('value') === 'inperson' ? 'inperson' : 'ship',
            'shippingFee': extractCurrencyNumber(document.querySelector('.ship-fee').textContent),
            "books": books,
            "paymentMethod": isChekedPayment.getAttribute('value'),
            'note': document.querySelector('input[id="note"]').textContent
                ? document.querySelector('input[id="note"]').value : null
        }

        await createOrder(data)
    } catch (error) {
        console.log(error)
    }
}
const btnConfirm = document.querySelector('.btn-confirm')
btnConfirm.addEventListener('click', () => handleCreateOrder())