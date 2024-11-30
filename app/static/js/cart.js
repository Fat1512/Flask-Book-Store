const CART_API = '/api/v1/cart'
const CHECKOUT_API = '/cart/checkout'
const groupControll = document.querySelectorAll('.cart-item')
const toggleAllButton = document.getElementById("toggleAll")
const checkboxs = document.querySelectorAll('.checkbox')

const buttonPayment = document.querySelector(".btn-payment")
let totalCheckbox = checkboxs.length
let cnt = 0
let toggle = false


toggleAllButton.addEventListener("click", () => {
    if (!toggle) {
        checkboxs.forEach(el => {
            if (!el.checked) {
                el.checked = true
                el.dispatchEvent(new Event('change'));
            }
        })
    } else
        checkboxs.forEach(el => {
            if (el.checked) {
                el.checked = false
                el.dispatchEvent(new Event('change'));
            }
        })
    toggle = !toggle
})
const VND = new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
});

function extractCurrencyNumber(currencyString) {
    const numericValue = currencyString.replace(/[^\d,]/g, ''); // Keep digits and comma
    return parseFloat(numericValue.replace(',', '.')); // Convert to float, replace comma with dot
}

const renderCheckAll = function () {
    toggleAllButton.checked = cnt === totalCheckbox;
}
const renderButtonPayment = function () {
    buttonPayment.disabled = cnt === 0
}
const moveCartItemToCheckOut = async function (data) {
    try {
        const response = await fetch(CHECKOUT_API, {
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
    } catch (error) {
        alert('Failed to delete cart.');
    }
}

async function handleOnClickPayment() {
    let cartItemChecked = []
    groupControll.forEach(el => {
            if (el.querySelector('.checkbox:checked')) {
                data = {
                    "bookId": el.getAttribute('id'),
                    "quantity": el.querySelector('.cart-item-quantity').textContent,
                    'price': extractCurrencyNumber(el.querySelector('.cart-item-price ').textContent),
                    'img': el.querySelector('.cart-item-image').getAttribute('src'),
                    'title': el.querySelector('.cart-item-detail-title').textContent
                }
                cartItemChecked.push(data)
            }
        }
    )
    await moveCartItemToCheckOut(cartItemChecked)
    window.location.replace('http://127.0.0.1:5000/cart/checkout')
}

buttonPayment.addEventListener("click", () => handleOnClickPayment()
)


const deleteCartItem = async function (id) {
    try {
        const response = await fetch(`${CART_API}/${id}`, {
            method: 'DELETE', // HTTP PUT method
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
        alert('Failed to delete cart.');
    }
}
const updateCart = async function (data) {
    try {
        const response = await fetch(CART_API, {
            method: 'PUT', // HTTP PUT method
            headers: {
                'Content-Type': 'application/json' // Specify JSON content type
            },
            body: JSON.stringify(data) // Convert data to JSON string
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json(); // Parse JSON response
        console.log('Cart updated:', result);
        alert(result.message);
    } catch (error) {
        console.error('Error updating cart:', error);
        alert('Failed to update cart.');
    }

}
groupControll.forEach(el => {
    const buttonDescrease = el.querySelector(".cart-item-descrease")
    const buttonIncrease = el.querySelector(".cart-item-increase")
    const quantityEl = el.querySelector(".cart-item-quantity")
    const totalprice = el.querySelector(".cart-item-price")
    const deletButton = el.querySelector(".fa-solid.fa-trash-can")
    const checkButon = el.querySelector(".checkbox")
    const totalPrice = document.querySelector(".total-price")

    checkButon.addEventListener('change', () => {
            const numTotalPrice = extractCurrencyNumber(totalPrice.textContent)
            const itemPrice = extractCurrencyNumber(quantityEl.textContent) *
                parseInt(buttonIncrease.getAttribute('value'))
            if (checkButon.checked) {
                totalPrice.innerHTML = VND.format(numTotalPrice + itemPrice)
                cnt++
            } else {
                totalPrice.innerHTML = VND.format(numTotalPrice - itemPrice)
                cnt--
            }
            renderCheckAll()
            renderButtonPayment()
        }
    )

    deletButton.addEventListener('click', () => {
        deleteCartItem(el.getAttribute("id"))
        el.remove()
    })
    buttonIncrease.addEventListener('click', () => {
        quantityEl.innerHTML = parseInt(quantityEl.textContent) + 1
        totalprice.innerHTML = VND.format(parseInt(quantityEl.textContent) *
            parseInt(buttonIncrease.getAttribute('value')))

        if (checkButon.checked) {
            const numTotalPrice = extractCurrencyNumber(totalPrice.textContent)
            const itemPrice = parseInt(buttonIncrease.getAttribute('value'))
            totalPrice.innerHTML = VND.format(numTotalPrice + itemPrice)
        }
        data = {
            "cartId": 2,
            "cartItems": [
                {
                    "bookId": el.getAttribute("id"),
                    "quantity": quantityEl.innerHTML
                }
            ]
        }
        updateCart(data)
    })
    buttonDescrease.addEventListener('click', () => {
        if (quantityEl.textContent === "1") return
        quantityEl.innerHTML = parseInt(quantityEl.textContent) - 1
        totalprice.innerHTML = VND.format(parseInt(quantityEl.textContent) *
            parseInt(buttonDescrease.getAttribute('value')))
        if (checkButon) {
            const numTotalPrice = extractCurrencyNumber(totalPrice.textContent)
            const itemPrice = parseInt(buttonIncrease.getAttribute('value'))
            totalPrice.innerHTML = VND.format(numTotalPrice - itemPrice)
        }
        data = {
            "cartId": 2,
            "cartItems": [
                {
                    "bookId": el.getAttribute("id"),
                    "quantity": quantityEl.innerHTML
                }
            ]
        }
        updateCart(data)
    })
})
