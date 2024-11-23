const TIME_OUT = 50;
const placeHolderAttribute = ["Nhap ten san pham", "Nhap barcode"]
let fetchOption = 0;
let currentTimeOutId;

const productSearchBox = document.querySelector('.product-search-box');
const dropDownBtn = document.querySelector(".dropdown-btn");

const orderContainer = document.querySelector(".order-container");
const productContainer = document.querySelector(".product-container");
const orderList = document.querySelector(".order-list");
const currentOrderItem = {};

const fetchProductByBarcode = async function () {
    console.log("Fetching by barcode");
    //Logic................
}

const fetchProductByName = async function () {
    console.log("Fetching by name");
    //Logic................
}

const productFetchingFunction = [fetchProductByName, fetchProductByBarcode];

productSearchBox.addEventListener("input", function () {
    clearTimeout(currentTimeOutId);
    currentTimeOutId = setTimeout(function () {
        productFetchingFunction[fetchOption]();
    }, TIME_OUT);
});

dropDownBtn.addEventListener("click", function (e) {
    e.preventDefault();
    const target = e.target.closest('.dropdown-item');
    if (!target) return;
    fetchOption = +e.target.getAttribute("id");
    productSearchBox.setAttribute("placeholder", placeHolderAttribute[fetchOption]);
});

productContainer.addEventListener("click", function (e) {
    const productItem = e.target.closest(".product-item");
    if (!productItem) return;
    const id = productItem.getAttribute("id");

    if(currentOrderItem[id]) {
        const input = orderContainer.querySelector(`[input-id="${id}"]`);
        console.log(input)
        input.value = +input.value + 1;
        return;
    }
    const book = {
        'book_id': id,
        'price': productItem.querySelector(".product-price").textContent.split(".")[0],
        'image_url': productItem.querySelector(".card-img-top").getAttribute("src"),
        'discount': productItem.querySelector(".discount").textContent,
        'title': productItem.querySelector(".product-name").textContent,
        'qty': 1
    }
    currentOrderItem[id] = true;
    renderOrderItem(book);
});


orderContainer.addEventListener("click", function (e) {
    const removeBtn = e.target.closest(".remove-order-item-btn");
    const incrementBtn = e.target.closest(".increment-qty-btn");
    const decrementBtn = e.target.closest(".decrement-qty-btn");
    if (removeBtn) {
        delete currentOrderItem[+removeBtn.closest(".order-item").getAttribute("id")];
        removeBtn.closest(".order-item").remove();

    }
    if (incrementBtn) {
        const input = incrementBtn.previousElementSibling;
        input.value = +input.value + 1;
    }
    if (decrementBtn) {
        const input = decrementBtn.nextElementSibling;
        input.value = input.value > 1 ? +input.value - 1 : input.value;
    }
});


orderContainer.querySelectorAll(".order-item").forEach(orderItem => currentOrderItem[orderItem.getAttribute("id")] = true)
console.log(currentOrderItem)
const renderOrderItem = function (book) {
    console.log(book)
    const html = `
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
                               class="text-center" value="${book.qty}">
                        <span class="cursor-pointer increment-qty-btn">+</span>
                    </div>
                </div>
            </td>
            <td>
                <div class="d-flex align-items-center w-100 justify-content-center">
                    <span class="completion mr-2">${+book.price * +book.qty}</span>
                </div>
            </td>
            <td class="text-right remove-order-item-btn">
                <div class="dropdown">
                    <a class="btn btn-sm btn-icon-only text-light cursor-pointer"  role="button">
                        <i class="fa fa-window-close" aria-hidden="true"></i>
                    </a>
                </div>
            </td>
        </tr>`;
    orderList.insertAdjacentHTML('beforeend', html);
}


// async function test() {
//     await fetch('/api/v1/order/1/update', {
//         method: "POST",
//         body: JSON.stringify(
//             [
//                 {
//                     'order_id': 1,
//                     'product_id': 2,
//                     'quantity': 3,
//                     'price': 12
//                 },
//                 {
//                     'order_id': 2,
//                     'product_id': 3,
//                     'quantity': 3,
//                     'price': 12
//                 }
//             ]
//         ),
//         headers: {
//             'Content-Type': 'application/json'
//         }
//     })
// }
//
// test();