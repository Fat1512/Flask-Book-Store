const modal = document.querySelector(".modal");
const modalBody = document.querySelector(".modal-body");
const qrBtn = document.querySelector(".qr-code-btn");
const overlay = document.querySelector(".overlay")
const orderContainer = document.querySelector(".order-container");
const productContainer = document.querySelector(".product-container");

const deleteAllBtn = document.querySelector(".delete-all-btn");
const checkoutBtn = document.querySelector(".checkout-btn");

let currentOrderItemsState = {};

let html5QrcodeScanner = new Html5QrcodeScanner(
    "reader", {
        fps: 10,
        qrbox: {width: 300, height: 200},
    },
    false
);
html5QrcodeScanner.render(onScanSuccess, onScanFailure);

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

    if (currentOrderItemsState[data['book_id']]) {
        currentOrderItemsState[data['book_id']]['quantity'] = +currentOrderItemsState[data['book_id']]['quantity'] + 1;
    } else {
        currentOrderItemsState[data['book_id']] = data;
        currentOrderItemsState[data['book_id']]['quantity'] = 1;
    }
    renderOrderItem(Object.entries(currentOrderItemsState).map(item => item[1]));
}

function onScanFailure(error) {

}

async function fetchBookByBarcode(barcode) {
    const res = await fetch(`/api/v1/book/barcode/${barcode}`, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json'
        }
    });
    return await res.json();
}

const toggleModal = function () {
    modal.classList.toggle("d-flex");
    overlay.classList.toggle("d-flex");
}

const resetState = function () {
    currentOrderItemsState = {};
    renderOrderItem(Object.entries(currentOrderItemsState).map(item => item[1]));
}

qrBtn.addEventListener("click", toggleModal);

overlay.addEventListener("click", toggleModal);

deleteAllBtn.addEventListener("click", resetState);

checkoutBtn.addEventListener("click", async function () {
    const res = await fetch(`/api/v1/order/add`, {
        method: "POST",
        body: JSON.stringify(Object.values(currentOrderItemsState)),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    if (!res.ok) throw new Error("Something went wrong");
    const order = await res.json();
    toggleModal();
    resetState();
    renderInvoice(order);

    document.querySelector(".btn-download-pdf").addEventListener("click", function () {
        const {jsPDF} = window.jspdf;

        Toastify({
            text: "Đang tải xuống...",
            duration: 3000,
            newWindow: true,
            close: true,
            gravity: "top", // `top` or `bottom`
            position: "right", // `left`, `center` or `right`
            stopOnFocus: true, // Prevents dismissing of toast on hover
            style: {
                background: "orange",
            }
        }).showToast();

        html2canvas(document.querySelector("#invoice"), {
            useCORS: true,
            allowTaint: false,
            scale: 2 // Improves image quality
        }).then(canvas => {
            const imgData = canvas.toDataURL("image/png");
            const pdf = new jsPDF("p", "mm", "a4");

            // Add image to PDF
            const imgProps = pdf.getImageProperties(imgData);
            const pdfWidth = pdf.internal.pageSize.getWidth();
            const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

            pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);

            pdf.save(`invoice_${document.querySelector('[order-id]').getAttribute("order-id")}.pdf`);

            Toastify({
                text: "Đã tải thành công !",
                duration: 3000,
                newWindow: true,
                close: true,
                gravity: "top", // `top` or `bottom`
                position: "right", // `left`, `center` or `right`
                stopOnFocus: true, // Prevents dismissing of toast on hover
                style: {
                    background: "#6cbf6c",
                }
            }).showToast();
        });
    });
});

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

const renderInvoice = function (order) {
    modalBody.innerHTML = '';
    const html = `
    <div id="invoice" class="mt-4 w-100" order-id="${order['order_id']}">
        <div class="card">
            <div class="card-header text-center">
                <img class="image-fluid w-25"
                     src="https://cdn0.fahasa.com/skin/frontend/ma_vanese/fahasa/images/fahasa-logo.png" alt="">
            </div>
            <div class="card-header invoice-header text-center">
                <p class="mb-0 font-weight-bold">Mã đơn: ${order['order_id']} &nbsp; | &nbsp; Ngày
                    đặt: ${order['created_at']}
                    &nbsp; | &nbsp; Hotline: 19008386
                    &nbsp; | &nbsp; Trạng thái: ${order['status']['name']} &nbsp; | &nbsp; Loại
                    đơn: ${order['order_type']['name']}</p>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-12">
                        <h1 class="text-center pb-3 display-3 text-black">THÔNG TIN HÓA ĐƠN</h1>
                    </div>
                    <div class="col-md-6">
                        <p>
                            <strong class="font-weight-600">Họ và Tên:</strong> ${order['address']['first_name']} ${order['address']['last_name']}<br>
                            <strong class="font-weight-600">Địa chỉ:</strong> ${order['address']['address']} <br>
                            <strong class="font-weight-600">Thành phố:</strong> ${order['address']['city']} <br>
                            <strong class="font-weight-600">Nước:</strong> ${order['address']['country']} <br>
                            <strong class="font-weight-600">Số điện thoại:</strong> ${order['address']['phone_number']} <br>
                        </p>
                    </div>
                    <div class="col-md-6 text-right">
                        <p>
                            ${order['order_type']['id'] === 1 ? `<strong class="font-weight-600"> Phương thức vận chuyển:</strong> ${order['order_type']['detail']['shipping_method']['name']}` : ''}
                            <strong class="font-weight-600">Phương thức thanh toán:</strong> ${order['payment']['payment_method']['name']}
                        </p>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-bordered">
                            <thead>
                            <tr class="text-center font-weight-700 text-black">
                                <th class="">Barcode</th>
                                <th class="">Tên sách</th>
                                <th class="">Giá</th>
                                <th class="">Giảm giá</th>
                                <th class="">Số lượng</th>
                                <th class="">Tổng tiền</th>
                            </tr>
                            </thead>
                            <tbody>
                            ${order['order_detail'].map(orderItem => `
                                <tr class="text-center">
                                    <td>${orderItem['book']['barcode']}</td>
                                    <td class="text-wrap text-left">
                                        <span class="w-100">${orderItem['book']['title']}</span>
                                    </td>
                                    <td>${orderItem['price']}</td>
                                    <td>0</td>
                                    <td>${orderItem['quantity']}</td>
                                    <td>${+orderItem['price'] * +orderItem['quantity']}</td>
                                </tr>`).join('')}
                            <tr class="text-right">
                            ${order['order_type']['id'] === 1 ? `
                                <td colspan="5"><strong>Phí ship:</strong></td>
                                <td class="text-center"> ${order['order_type']['detail']['shipping_fee']} </td>` : ''}
                            </tr>
                            <tr class="text-right">
                                <td colspan="5"><strong>Tổng tiền:</strong></td>
                                <td class="text-center">${order['total_amount']}</td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="row col-12 pt-3 justify-content-between">
                        <div class="col-md-6">
                                ${order['order_type']['id'] === 1 ? `
                                <p>
                                    <strong>Ghi chú:</strong> {% if order['order_type']['detail']['note'] %} order['note'] {% endif %}
                                    <br>
                                </p>` : ''}
                        </div>
                        <div class="col-md-6">
                            <p class="text-right">
                                ${order['order_type']['id'] === 2 ? `
                                <strong>Nhân viên thanh toán:</strong> ${order['order_type']['detail']['employee_name']}` : ''}
                                <br>
                                <strong>Ngày in hóa đơn:</strong> 2
                            </p>
                            <p class="text-right">
                                <button id="downloadPDF"
                                        class="btn text-right text-white btn-print btn-download-pdf">In hóa đơn
                                </button>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>`;
    modalBody.insertAdjacentHTML("beforeend", html);
}