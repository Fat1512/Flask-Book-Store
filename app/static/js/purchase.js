const ACCOUNT_API = '/api/v1/account'
const CART_API = '/api/v1/cart'
const orderArea = document.querySelector(".order-area")

const VND = new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
});

function extractCurrencyNumber(currencyString) {
    const numericValue = currencyString.replace(/[^\d,]/g, ''); // Keep digits and comma
    return parseFloat(numericValue.replace(',', '.')); // Convert to float, replace comma with dot
}

const fetchOrder = async function (prefix, params) {
    try {
        const response = await fetch(`${ACCOUNT_API}/${prefix}?${params}`, {
            method: 'GET', // HTTP PUT method
            headers: {
                'Content-Type': 'application/json' // Specify JSON content type
            },
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json(); // Parse JSON response

        if (result['status'] === 200)
            return result['orders']
    } catch (error) {
        alert('Failed to delete cart.');
    }
}
const addCartItem = async function (books) {
    try {
        const response = await fetch(`${CART_API}/books`, {
            method: 'POST', // HTTP PUT method
            headers: {
                'Content-Type': 'application/json' // Specify JSON content type
            },
            body: JSON.stringify(books)
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json(); // Parse JSON response
        if (result['status'] === 200)
            window.location.replace('http://127.0.0.1:5000/cart')

    } catch (error) {
        alert('Failed to add cart.');
    }
}

async function handleReBuy(book_id) {
    await addCartItem(book_id)
}

const renderOderArea = function (orders) {

    if (orders.length) {
        orderArea.innerHTML = orders.map(order => {
            const orderList = order['order_detail']
            const orderDetailHTML = orderList.map(od =>
                `
        <div class="purchase-item">
            <div class="item-infor d-flex align-items-center">
                <div class="item-infor-image">
                    <img class="w-100"
                         src="${od.book.images[0].image_url}">
                </div>
                <div class="item-infor-detail">
                    <p>${od.book.title}</p>
                    <p class="text-secondary"> Thể loại: SGK </p>
                    <p>x1</p>
                </div>
                <div class="item-infor-price text-center">
                    <span class="text-secondary text-decoration-line-through">${VND.format(od.book.price)}</span>
                    <span class="text-primary">${VND.format(od.book.price)}</span>
                </div>
            </div>
        </div>
        `
            ).join('')

            return ` <ul class="list-unstyled m-0">
                <li class="item-bg-color mt-3 mb-3 p-3">
                    <div class="purchase-header pb-3">
                        <p class="text-right m-0">
                            ${order.status.id === 4 && `<span style="color: #26aa99">Giao hàng thành công</span>`}             
                            <span class="separator"> | </span>
                            <span class="text-primary">${order.status.name}</span></p>
                    </div>
                    <div class="purchase-list">
                       ${orderDetailHTML}
                    </div>
                    <div class="purchase-controll pb-2 text-right">
                        <p>Thành tiền: <span
                                class="text-primary">${VND.format(order.total_amount)}</span></p>
                        <div>
                            <button onclick="handleReBuy(${JSON.stringify(order.order_detail.map(od => od.book.book_id))})"  class="btn btn-primary btn-large">Mua lại</button>
                        </div>
                    </div>

                </li>
        </ul>`
        }).join("")

    } else {
        orderArea.innerHTML = ` <li class="item-bg-color item-null mt-3 mb-3 p-3">
                                    <div class="content-null"></div>
                                    <div class="text">Chưa có đơn hàng</div>
                                </li>`
    }
}

async function handleOnClickFilter(e) {
    const orders = await fetchOrder("/purchase", `status=${e.target.id}`)
    const prev = headerItem.querySelector(".home_category_item.active")
    if (prev)
        prev.classList.remove('active')
    e.target.classList.add("active")
    renderOderArea(orders)
}

const headerItem = document.querySelector(".home_category_heading")
headerItem.querySelectorAll(".home_category_item").forEach(el => {
    el.addEventListener('click', (e) => handleOnClickFilter(e))
})

