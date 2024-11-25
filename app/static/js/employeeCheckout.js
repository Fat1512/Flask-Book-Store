const modal = document.querySelector(".modal");
const qrBtn = document.querySelector(".qr-code-btn");
const overlay = document.querySelector(".overlay")
const orderContainer = document.querySelector(".order-container");
const productContainer = document.querySelector(".product-container");

const deleteAllBtn = document.querySelector(".delete-all-btn");
const checkoutBtn = document.querySelector(".checkout-btn");

let currentOrderItemsState = {};

async function onScanSuccess(decodedText, decodedResult) {
    // handle the scanned code as you like, for example:
    console.log(`Code matched = ${decodedText}`, decodedResult);
    const barcode = decodedText;
    html5QrcodeScanner.pause(1);

    setTimeout(() => {
        html5QrcodeScanner.resume();
        modal.classList.remove("d-flex")
        overlay.classList.remove("d-flex");
    }, 1000);
    const data = await fetchBookByBarcode(barcode);


    if(currentOrderItemsState[data['book_id']]) {
        console.log(currentOrderItemsState)
        currentOrderItemsState[data['book_id']]['quantity'] = +currentOrderItemsState[data['book_id']]['quantity'] + 1;
    } else {
        currentOrderItemsState[data['book_id']] = data;
        currentOrderItemsState[data['book_id']]['quantity'] = 1;
    }
    renderOrderItem(Object.entries(currentOrderItemsState).map(item => item[1]));}

function onScanFailure(error) {

}

async function fetchBookByBarcode(barcode) {
    const res = await fetch(`/api/v1/book/barcode/${barcode}`, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const data = await res.json();
    return data;
}


let html5QrcodeScanner = new Html5QrcodeScanner(
    "reader",
    {
        fps: 10,
        qrbox: {width: 300, height: 200},
    },
    /* verbose= */ false
);
html5QrcodeScanner.render(onScanSuccess, onScanFailure);

qrBtn.addEventListener("click", async function () {
    modal.classList.add("d-flex");
    overlay.classList.add("d-flex");
});

overlay.addEventListener("click", function () {
    modal.classList.remove("d-flex")
    overlay.classList.remove("d-flex");
})

deleteAllBtn.addEventListener("click", function() {
    currentOrderItemsState = {};
    renderOrderItem(Object.entries(currentOrderItemsState).map(item => item[1]));
})

checkoutBtn.addEventListener("click", async function() {
     const res = await fetch(`/api/v1/order/add`, {
            method: "POST",
            body: JSON.stringify(Object.values(currentOrderItemsState)),
            headers: {
                'Content-Type': 'application/json'
            }
        });
    if (!res.ok) throw new Error("Something went wrong");
    const {order_id} = await res.json();
    window.location.replace(`${window.location.origin}/employee/order/${order_id}/detail`);
})

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
            'price': productItem.querySelector(".product-price").textContent.split(".")[0].trim(),
            'discount': productItem.querySelector(".discount").textContent,
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

const renderOrderItem = function (books) {
    const orderList = orderContainer.querySelector(".order-list");
    orderList.innerHTML = '';
    const html = books.map(book => `
        <tr class="order-item" id="${book.book_id}">
            <th scope="row">
                <div class="media align-items-center">
                    <div class="media-body text-left text-truncate book-item">
                        <span class="name mb-0 text-sm text-center w-100">${book.title}</span>
                    </div>
                </div>
            </th>
            <td class="budget text-center">
                ${book.price} VNĐ
            </td>
            <td>
                <span class="badge badge-dot mr-4 text-center w-100">
                <span class="status text-center">${book.discount}</span>
                </span>
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
                    <span class="completion mr-2">${+book.price * +book.quantity}</span>
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
    document.querySelector(".total-amount").textContent = books.reduce((acc, obj) => acc + +obj['price'] * +obj['quantity'], 0) + ' VND';
    document.querySelector(".total-qty").textContent = books.reduce((acc, book) => acc + +book.quantity, 0);
    orderList.insertAdjacentHTML('beforeend', html);
}