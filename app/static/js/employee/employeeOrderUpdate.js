//---------------------------------------------CONSTANTS---------------------------------------------
const vndCurrencyFormat = new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
});

function extractCurrencyNumber(currencyString) {
    const numericValue = currencyString.replace(/[^\d,]/g, ''); // Keep digits and comma
    return parseFloat(numericValue.replace(',', '.')); // Convert to float, replace comma with dot
}

const Color = {
    WARNING: "orange",
    ERROR: `var(--red)`,
    SUCCESS: "#6cbf6c"
}

const BOOK_API = "/api/v1/book"

//---------------------------------------------DOM ELEMENTS & STATES---------------------------------------------
const inputSearch = document.querySelector('.input-search');
const restoreOrderBtn = document.querySelector(".restore-btn");
const updateBtn = document.querySelector(".update-btn");

const orderContainer = document.querySelector(".order-container");
const productContainer = document.querySelector(".product-container");

const searchBtn = document.querySelector(".btn-search");
const resetBtn = document.querySelector(".btn-reset");

let initialOrderItemsState = {};
let currentOrderItemsState = {};


//---------------------------------------------RENDER---------------------------------------------
const renderToast = function (text, background) {
    Toastify({
        text: text,
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: "right", // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
            background: background,
        }
    }).showToast();
}

const renderBookItem = function (books) {
    const html = books.map(book => `
    <a class="product-item card col-3 cursor-pointer" id="${book['book_id']}">
        <img class="card-img-top"
             src="${book.images?.[0]?.image_url}"
             alt="Card image"
             style="height: auto !important;">
        <div class="card-body p-0">
            <p class="card-text product-name">${book['title']}</p>
            <p class="text-primary font-weight-bold mb-1 product-price">${vndCurrencyFormat.format(book['price'])}</p>
            <p class="text-dark font-weight-light mb-1">qty: ${book['quantity']}</p>
        </div>
    </a>`).join('');

    productContainer.innerHTML = '';
    productContainer.insertAdjacentHTML("beforeend", html);
}

const renderOrderItem = function (books) {
    const orderList = orderContainer.querySelector(".order-list");
    orderList.innerHTML = '';
    const html = books.map(book => `
        <tr class="order-item" id="${book.book_id}">
            <th scope="row">
                <div class="media align-items-center">
                    <div class="media-body text-left text-truncate book-item">
                        <span class="order-item-name mb-0 text-sm text-center w-100">${book.title}</span>
                    </div>
                </div>
            </th>
            <td class="budget text-center order-item-price">
                ${vndCurrencyFormat.format(book.price)}
            </td>
            <td>
                <div class="d-flex justify-content-center">
                    <div class="d-flex justify-content-between align-content-center w-100">
                        <span class="cursor-pointer decrement-qty-btn">-</span>
                        <input input-id="${book.book_id}" inputmode="numeric"
                               oninput="this.value = this.value.replace(/\\D+/g, '')"
                               class="text-center" value="${book.quantity}">
                        <span class="cursor-pointer increment-qty-btn">+</span>
                    </div>
                </div>
            </td>
            <td>
                <div class="d-flex align-items-center w-100 justify-content-center">
                    <span class="completion mr-2">${vndCurrencyFormat.format(+book.price * +book.quantity)}</span>
                </div>
            </td>
            <td class="text-right remove-order-item-btn">
                <div class="dropdown">
                    <a class="btn btn-sm btn-icon-only text-light cursor-pointer"  role="button">
                        <i class="fa fa-window-close" aria-hidden="true"></i>
                    </a>
                </div>
            </td>
        </tr>`).join('');
    const totalAmount = books.reduce((acc, obj) => acc + +obj['price'] * +obj['quantity'], 0);
    const shippingFee = extractCurrencyNumber(document.querySelector(".shipping-fee").textContent.trim());
    document.querySelector(".total-amount").textContent = vndCurrencyFormat.format(totalAmount + shippingFee);
    orderList.insertAdjacentHTML('beforeend', html);
}



//---------------------------------------------API UTILITY---------------------------------------------
async function fetchBooks() {
    try {
        const res = await fetch(`${BOOK_API}`, {
            method: "GET",
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!res.ok) throw new Error("Có lỗi xảy ra");
        const data = await res.json();
        if(data['status'] !== 200) throw new Error(data['message']);
        return data['data'];
    } catch (err) {
        throw err;
    }
}


const fetchBookByBarcode = async function (barcode) {
    try {
        const res = await fetch(`/api/v1/book/barcode/${barcode}`, {
            method: "GET",
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!res.ok) throw new Error("Có lỗi xảy ra");
        const data = await res.json();
        if(data['status'] !== 200) throw new Error(data['message']);

        return data['data'];
    } catch (err) {
        throw err;
    }
}

//---------------------------------------------EVENT---------------------------------------------
productContainer.addEventListener("click", function (e) {
    const productItem = e.target.closest(".product-item");
    if (!productItem) return;
    const id = productItem.getAttribute("id");

    if (currentOrderItemsState[id]) {
        const input = orderContainer.querySelector(`[input-id="${id}"]`);
        currentOrderItemsState[id]['quantity'] = +input.value + 1;
    } else {
        currentOrderItemsState[id] = {
            'book_id': id,
            'price': extractCurrencyNumber(productItem.querySelector(".product-price").textContent),
            'title': productItem.querySelector(".product-name").textContent,
            'quantity': 1
        };
    }

    renderOrderItem(Object.entries(currentOrderItemsState).map(item => item[1]));
});

orderContainer.addEventListener("click", function (e) {
    const removeBtn = e.target.closest(".remove-order-item-btn");
    const incrementBtn = e.target.closest(".increment-qty-btn");
    const decrementBtn = e.target.closest(".decrement-qty-btn");
    const id = e.target.closest(".order-item")?.getAttribute("id");
    let isTriggered = false;

    if (removeBtn) {
        if (Object.keys(currentOrderItemsState).length === 1) {
            renderToast("Đơn phải có ít nhất 1 sản phẩm", Color.ERROR);
            return;
        }
        delete currentOrderItemsState[+id];
        isTriggered ||= true;
    }
    if (incrementBtn) {
        const input = incrementBtn.previousElementSibling;
        currentOrderItemsState[+id]['quantity'] = +input.value + 1;
        isTriggered ||= true;
    }
    if (decrementBtn) {
        const input = decrementBtn.nextElementSibling;
        currentOrderItemsState[+id]['quantity'] = input.value > 1 ? +input.value - 1 : input.value;
        isTriggered ||= true;
    }
    isTriggered && renderOrderItem(Object.entries(currentOrderItemsState).map(item => item[1]));
});

searchBtn.addEventListener("click", async function () {
    try {
        const barcode = inputSearch.value;
        const book = await fetchBookByBarcode(barcode);
        renderBookItem([book]);
    } catch (err) {
        renderToast(err.message, Color.ERROR);
    }
});

resetBtn.addEventListener("click", async function () {
    try {
        const books = await fetchBooks();
        renderBookItem(books['books']);
        inputSearch.value = '';
    } catch (err) {
        renderToast(err.message, Color.ERROR);
    }
});

orderContainer.addEventListener("change", function (e) {
    const input = e.target;
    if (input.value === 0 || input.value === '' | isNaN(input.value)) input.value = 1;

    currentOrderItemsState[+input.getAttribute("input-id")]['quantity'] = +input.value;
    renderOrderItem(Object.entries(currentOrderItemsState).map(item => item[1]))
})


restoreOrderBtn.addEventListener("click", () => {
    renderOrderItem(Object.entries(initialOrderItemsState).map(item => item[1]))
    currentOrderItemsState = JSON.parse(JSON.stringify(initialOrderItemsState));
});


updateBtn.addEventListener("click", async function (e) {
    updateBtn.classList.remove("bg-blue")
    updateBtn.classList.add("btn-disable")
    updateBtn.disabled = true
    restoreOrderBtn.classList.remove("bg-red")
    restoreOrderBtn.classList.add("btn-disable")
    restoreOrderBtn.disabled = true

    console.log(Object.values(currentOrderItemsState))

    try {
        const res = await fetch(`/api/v1/order/${+updateBtn.getAttribute("order-id")}/update`, {
            method: "POST",
            body: JSON.stringify(Object.values(currentOrderItemsState)),
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!res.ok) throw new Error("Có lỗi xảy ra !");
        initialOrderItemsState = JSON.parse(JSON.stringify(currentOrderItemsState));
        renderToast("Cập nhật thành công !", Color.SUCCESS)
    } catch (err) {
        renderToast(err.message, Color.ERROR);
    } finally {
        updateBtn.classList.add("bg-blue")
        updateBtn.classList.remove("btn-disable")
        updateBtn.disabled = false
        restoreOrderBtn.classList.add("bg-red")
        restoreOrderBtn.classList.remove("btn-disable")
        restoreOrderBtn.disabled = false
    }
})

orderContainer.querySelectorAll(".order-item").forEach(orderItem => {
    const obj = {
        'book_id': orderItem.getAttribute("id"),
        'price': extractCurrencyNumber(orderItem.querySelector(".order-item-price").textContent),
        'title': orderItem.querySelector(".order-item-name").textContent,
        'quantity': orderItem.querySelector(`[input-id="${orderItem.getAttribute("id")}"]`).value
    }
    initialOrderItemsState[obj["book_id"]] = obj;
    currentOrderItemsState[obj["book_id"]] = obj;
});
