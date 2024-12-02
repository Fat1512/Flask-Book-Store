const vndCurrencyFormat = new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
});

function extractCurrencyNumber(currencyString) {
    const numericValue = currencyString.replace(/[^\d,]/g, ''); // Keep digits and comma
    return parseFloat(numericValue.replace(',', '.')); // Convert to float, replace comma with dot
}

const dateFormatter = new Intl.DateTimeFormat('vi-VN', {
    weekday: 'short', // e.g., Thứ Sáu
    year: 'numeric',
    month: 'numeric', // e.g., Tháng 1
    day: 'numeric',
    // timeZoneName: 'short' // e.g., GMT
});

const timeFormatter = new Intl.DateTimeFormat('vi-VN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    // timeZoneName: 'short' // e.g., GMT
});

const ORDER_API = `/api/v1/order`;

const url = new URL(window.location)

const orderParams = [
    {
        "orderType": 1 //Dat online
    },
    {
        "orderType": 2 //Mua truc tiep
    }
]
const sortParams = [
    {
        "sortBy": "date",
        "dir": "desc"
    },
    {
        "sortBy": "date",
        "dir": "asc"
    },
    {
        "sortBy": "total-amount",
        "dir": "asc"
    },
    {
        "sortBy": "total-amount",
        "dir": "desc"
    }
]
const statusParams = [
    {
        "status": 1 //Dang xu ly
    },
    {
        "status": 2 //Cho giao hang
    },
    {
        "status": 3 //Dang giao hang
    },
    {
        "status": 4 //Da hoan thanh
    },
    {
        "status": 5 //Da huy
    }
]
const paymentMethodParams = [
    {
        "paymentMethod": 1 //The
    },
    {
        "paymentMethod": 2 //Tien mat
    }
]

//shipping method = 1: ship ve nha
const shippingStatus = {
    "1": {//shipping id
        "1": "Đang xử lý", //order status id
        "2": "Chờ giao hàng",
        "3": "Đang giao hàng",
        "7": "Đã hoàn thành"
    },
    "2": {
        "1": "Đang xử lý",
        "8": "Đang chờ nhận",
        "7": "Đã hoàn thành"
    }
};
//shipping method = 2: cua hang

/**
 *     DANG_XU_LY = 1
 *     CHO_GIAO_HANG = 2
 *     DANG_GIAO_HANG = 3
 *
 *     DA_HOAN_THANH = 4
 *     DA_HUY = 5
 *
 *     DANG_CHO_THANH_TOAN = 6
 *     DA_THANH_TOAN = 7
 *
 *     DANG_CHO_NHAN = 8
 * @type {Element}
 */

//---------------------------------------------CONTAINER---------------------------------------------
const productSearchBox = document.querySelector('.product-search-box');
const orderTable = document.querySelector(".order-table");
const orderList = document.querySelector(".order-list");
const pagination = document.querySelector(".pagination");
const filterLabelContainer = document.querySelector(".filter-label-container");
//---------------------------------------------FILTER---------------------------------------------
const orderType = document.querySelector(".order-type");
const sortType = document.querySelector(".sort-type");
const statusType = document.querySelector(".status-type");
const paymentMethodType = document.querySelector(".payment-method-type");

//=======================================
const orderTab = document.querySelector(".order-tab");
const dateSearchContainer = document.querySelector(".date-search-container");
const filterContainer = document.querySelector(".filter-container");
const modal = document.querySelector(".modal");
const modalBody = document.querySelector(".modal-update-order-item-status");
const overlay = document.querySelector(".overlay");

//---------------------------------------------FUNCTION---------------------------------------------

let currentLabel = {};
let currentUpdateOrderStatus = {};
const resetAllState = function () {
    currentLabel = {};
    renderLabel()
    document.querySelectorAll("input:checked").forEach(input => input.checked = false);
    url.search = "";
    window.history.pushState({}, '', url);
}

const hideFilter = function () {
    filterContainer.classList.add("hide");
    dateSearchContainer.classList.add("hide");
}

const unhideFilter = function () {
    filterContainer.classList.remove("hide");
    dateSearchContainer.classList.remove("hide");
}

const deleteParams = (params) => params.forEach(param => url.searchParams.delete(param))
const addParams = (params) => params.forEach(param => url.searchParams.set(param[0], param[1]))
const renderOrder = function (orders, tab = 0) {
    orderList.innerHTML = '';
    currentOrderItemsState = {};
    const html = orders.map(order => {
        currentOrderItemsState[order['order_id']] = order;
        return `
            <tr class="order-id" id="${order['order_id']}">
                <th scope="row">
                    <div class="media align-items-center">
                        <div order-id="${order['order_id']}" id="${order['order_id']}">${order['order_id']}</div>
                    </div>
                </th>
                <td>
                    <div class="media-body">
                        <span class="name mb-0 text-sm">${order['order_type']['name']}</span>
                    </div>
                </td>
                <td class="budget">
                    ${vndCurrencyFormat.format(+order['total_amount'])}
                </td>
                <td>
                <span class="badge badge-dot mr-4">
                <i class="bg-warning"></i>
                <span class="status">${order['status']['name']}</span>
                </span>
                </td>
                <td>
                    <div class="avatar-group">
                        ${dateFormatter.format(new Date(order['created_at']))} - ${timeFormatter.format(new Date(order['created_at']))}
                    </div>
                </td>
                <td>
                    <div class="avatar-group">
                        ${order['payment']['payment_method']['name']}
                    </div>
                </td>
                <td class="text-right">
                    <div class="dropdown">
                        <a class="btn btn-sm btn-icon-only text-light" href="#" role="button"
                           data-toggle="dropdown"
                           aria-haspopup="true" aria-expanded="false">
                            <i class="fas fa-ellipsis-v"></i>
                        </a>
                        <div class="dropdown-menu dropdown-menu-right dropdown-menu-arrow">                      
                            <a class="dropdown-item" tab="${tab}">${tab === 0 ? "Chi tiết" : tab === 1 || tab === 2 ? "Cập nhật" : "Huỷ"}</a>
                        </div>
                    </div>
                </td>
            </tr>`
    }).join("");
    orderList.insertAdjacentHTML('beforeend', html);
}
const renderPagination = function (total_page, current_page) {
    const prev = `
        <li class="page-item ${current_page == 1 ? "disabled" : ""}" page=${current_page - 1}>
            <div class="page-link" tabindex="-1">
                <i class="fas fa-angle-left "></i>
                <span class="sr-only">Previous</span>
            </div>
        </li>`;
    const content = [...Array(total_page).keys()].map(page => {
        return `
            <li class="page-item ${page + 1 == current_page ? "active" : ""}" page=${page + 1}>
                <div class="page-link" >${page + 1}</div>
            </li>`;
    }).join('');
    const next = `
        <li class="page-item ${current_page == total_page ? "disabled" : ""}" page=${current_page + 1}>
            <div class="page-link" >
                <i class="fas fa-angle-right"></i>
                <span class="sr-only">Next</span>
            </div>
        </li>`;
    pagination.innerHTML = '';
    pagination.insertAdjacentHTML('beforeend', prev)
    pagination.insertAdjacentHTML('beforeend', content)
    pagination.insertAdjacentHTML('beforeend', next)
}
const renderLabel = function () {
    filterLabelContainer.innerHTML = '';
    const html = Object.entries(currentLabel).map(label =>
        `<span class="badge badge-secondary bg-red text-white cursor-pointer mr-2">${label[0]}</span>`).join('');

    filterLabelContainer.insertAdjacentHTML('beforeend', html);
}
const renderStatusUpdateForm = function (order, statusArray) {
    const html = `
    <div class="card p-5 order-modal" id="${order['order_id']}">
        <div class="d-flex justify-content-between">
          
        </div>
        <div class="card-header pl-0 bg-transparent border-0">
            <h3 class="mb-0 display-4">Thông tin đơn</h3>
        </div>
        <div class="row justify-content-between">
            <div class="col-6">
                <div class="d-flex">
                    <h2 class="pr-3">Mã đơn: </h2>
                    <h2 class="font-weight-400" order-id="">${order['order_id']}</h2>
                </div>
                <div class="d-flex">
                    <h2 class="pr-3">Trạng thái: </h2>
                    <h2 class="font-weight-400 ">${order['status']['name']}</h2>
                </div>
                <div class="d-flex">
                    <h2 class="pr-3">Phương thức thanh toán: </h2>
                    <h2 class="font-weight-400"> ${order['payment']['payment_method']['name']}</h2>
                </div>
                <div class="d-flex">
                    <h2 class="pr-3">Ngày tạo: </h2>
                    <h2 class="font-weight-400"> ${order['created_at']} </h2>
                </div>
            </div>
            <div class="col-6">
                <div class="d-flex">
                    <h2 class="pr-3 w-600">Loại đơn: </h2>
                    <h2 class="font-weight-400"> ${order['order_type']['name']} </h2>
                </div>
                ${order['order_type']['id'] === 1 ? `
                <div class="d-flex">
                    <h2 class="pr-3">Phương thức vận chuyển: </h2>
                    <h2 class="font-weight-400">${order['order_type']['detail']['shipping_method']['name']}</h2>
                </div>
                ` : ''}
                 ${order['order_type']['id'] === 2 ? `
                 <div class="d-flex">
                    <h2 class="pr-3">Nhân viên thanh toán: </h2>
                    <h2 class="font-weight-400"> }}</h2>
                </div>
                 ` : ''}
            </div>
        </div>
        <div class="card-body">
            <form>
                <div class="row pb-4">
                    <div class="col-6">
                        <h6 class=" display-4 text-muted mb-4">Thông tin</h6>
                        <div class="pl-lg-4">
                            <div class="row">
                                <div class="col-lg-12">
                                        <span class="form-control-label"
                                              for="input-address">Họ và tên: </span>
                                    <span>${order['address']['first_name']} ${order['address']['last_name']}</span>
                                </div>
                                <div class="col-lg-12">
                                        <span class="form-control-label"
                                              for="input-address">Địa chỉ: </span>
                                    <span>${order['address']['address']}</span>
                                </div>
                                <div class="col-lg-12">
                                    <span class="form-control-label" for="input-city">Thành phố: </span>
                                    <span>${order['address']['city']}</span>
                                </div>
                                <div class="col-lg-12">
                                    <span class="form-control-label" for="input-city">Nước: </span>
                                    <span>${order['address']['country']}</span>
                                </div>
                                <div class="col-lg-12">
                                        <span class="form-control-label"
                                              for="input-city">Số điện thoại: </span>
                                    <span>${order['address']['phone_number']}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </form>
        </div>
        <div>Trạng thái</div>
            <ul>
                ${statusArray.map(status => `
                    <li  class="d-flex align-content-center cursor-pointer">
                        <div class="pr-3">
                            <div class="">
                                <input id="${status[0]}" type="checkbox">
                            </div>
                        </div>
                        <div scope="row">
                            <div class="">
                                <div class="book-item-id" id="1">${status[1]}</div>
                            </div>
                        </div>
                    </li>
                `).join("")}
            </ul>
            <div class="text-right">
            <div class="btn btn-primary btn-confirm-change-status">Xác nhận</div>
        </div>
    </div>`;
    modalBody.innerHTML = '';
    modalBody.insertAdjacentHTML("beforeend", html);
}

const fetchOrder = async function (param) {
    try {
        const res = await fetch(`${ORDER_API}${param}`);
        if (!res.ok) throw new Error("Cannot fetch order");
        return await res.json();
    } catch (err) {
        alert(err.message);
    }
};
const modifyOrderStatus = async function (orderId, orderStatusId) {
    try {
        const res = await fetch(`${ORDER_API}/${orderId}/status`, {
            method: "POST",
            body: JSON.stringify({"id": orderStatusId}),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!res.ok) throw new Error("update order status");
        return await res.json();
    } catch (err) {
        alert(err.message);
    }
}

const openModal = function () {
    overlay.classList.add("d-flex");
    modal.classList.add("d-flex");
    modalBody.classList.add("d-flex");
}

const closeModal = function () {
    overlay.classList.remove("d-flex");
    modal.classList.remove("d-flex");
    modalBody.classList.remove("d-flex");
}

//---------------------------------------------EVENT---------------------------------------------

let currentOrderItemsState = {};

modalBody.addEventListener("click", function (e) {
    const input = e.target.closest("input");
    const confirmBtn = e.target.closest(".btn-confirm-change-status");
    if (input) {
        const currentState = input.checked;
        modalBody.querySelectorAll("input").forEach(inp => inp.checked = false);
        input.checked = currentState;
    }
    if(confirmBtn) {
        const orderId = modalBody.querySelector(".order-modal").getAttribute("id");
        const selectedStatusId = modalBody.querySelector("input:checked").getAttribute("id");
        modifyOrderStatus(orderId, selectedStatusId);
    }
});

orderTab.addEventListener("click", async function (e) {
    const allOrder = e.target.closest(".all-order");
    const updateOrderInfo = e.target.closest(".update-order-info");
    const updateOrderStatus = e.target.closest(".update-order-status");
    const cancelOrder = e.target.closest(".cancel-order");

    let data;
    let tab = 0;

    if (allOrder) {
        data = await fetchOrder('');
        unhideFilter();
        tab = 0;
    }
    if (updateOrderInfo) {
        data = await fetchOrder('?orderType=1&paymentMethod=2&status=1,2,8');
        hideFilter()
        tab = 1;
    }
    if (updateOrderStatus) {
        data = await fetchOrder('?orderType=1&paymentMethod=2&status=1,2,3,8');
        hideFilter()
        tab = 2;
    }
    if (cancelOrder) {
        data = await fetchOrder('?orderType=1&paymentMethod=2&status=1,2,8');
        hideFilter()
        tab = 3;
    }
    renderOrder(data['orders'], tab);
    renderPagination(data['total_page'], data['current_page']);
    resetAllState()
});

orderList.addEventListener("click", async function (e) {
    const target = e.target.closest(".dropdown-item");
    if (!target) return;
    const tab = +target.getAttribute("tab");
    const orderId = e.target.closest(".order-id").getAttribute("id");
    /**
     * tab = 0: view order detail
     * tab = 1: update order info
     * tab = 2: update order status
     * tab = 4: cancel order
     */
    switch (tab) {
        case 0: {
            window.open(`/employee/order/${orderId}/detail`, "_blank");
            break;
        }
        case 1: {
            window.open(`/employee/order/${orderId}/update`, "_blank");
            break;
        }
        // const shippingStatus = {
        //     "1": {//shipping id
        //         "1": "Đang xử lý", //order status id
        //         "2": "Chờ giao hàng",
        //         "3": "Đang giao hàng",
        //         "7": "Đã hoàn thành"
        //     },
        //     "2": {
        //         "1": "Đang xử lý",
        //         "8": "Đang chờ nhận",
        //         "7": "Đã hoàn thành"
        //     }
        // };
        case 2: {
            const order = currentOrderItemsState[orderId];

            const shippingMethodId = order['order_type']['detail']['shipping_method']['id'];
            const statusId = order['status']['id'];

            const idx = Object.keys(shippingStatus[shippingMethodId]).indexOf(`${statusId}`);
            const statusArray = Object.entries(shippingStatus[shippingMethodId]).slice(idx + 1);
            renderStatusUpdateForm(order, statusArray);

            openModal()
            // window.open(`/employee/order/${orderId}/detail`, "_blank");
            break;
        }
        case 3: {
            // window.open(`/employee/order/${orderId}/detail`, "_blank");
            break;
        }
    }
    console.log(target)
});

overlay.addEventListener("click", closeModal)

sortType.addEventListener("click", (e) => {
    const item = e.target.closest(".filter-type-item");
    if (!item) return;

    const toggleId = +item.getAttribute("id");
    handleFilterChange(sortType, Object.entries(sortParams[toggleId - 1]), ["sortBy", "dir"], toggleId);
});

statusType.addEventListener("click", (e) => {
    const item = e.target.closest(".filter-type-item");
    if (!item) return;

    const toggleId = +item.getAttribute("id");
    handleFilterChange(statusType, Object.entries(statusParams[toggleId - 1]), ["status", "page"], toggleId);
});

paymentMethodType.addEventListener("click", (e) => {
    const item = e.target.closest(".filter-type-item");
    if (!item) return;

    const toggleId = +item.getAttribute("id");
    handleFilterChange(paymentMethodType, Object.entries(paymentMethodParams[toggleId - 1]), ["paymentMethod", "page"], toggleId);
});

orderType.addEventListener("click", (e) => {
    const item = e.target.closest(".filter-type-item");
    if (!item) return;

    const toggleId = +item.getAttribute("id");
    handleFilterChange(orderType, Object.entries(orderParams[toggleId - 1]), ["orderType", "page"], toggleId);
});

pagination.addEventListener("click", async function (e) {
    const item = e.target.closest(".page-item");
    if (!item || item.classList.contains("disabled") || item.classList.contains("active")) return;

    deleteParams(["page"])
    addParams([["page", item.getAttribute("page")]]);
    window.history.pushState({}, '', url);

    const data = await fetchOrder(url.search);
    renderOrder(data['orders'])
    renderPagination(data['total_page'], data['current_page']);
})


const handleFilterChange = async function (parent, setParams, deletedParams, toggleId) {
    deleteParams(deletedParams);
    let isToggle = false;
    parent.querySelectorAll(".filter-type-item").forEach(item => {
        const itemId = +item.getAttribute("id");
        const input = item.querySelector("input")
        const label = item.querySelector(".dropdown-item")
        input.checked = itemId === toggleId ? !input.checked : false;
        if (input.checked) {
            currentLabel[label.textContent] = true;
        } else {
            delete currentLabel[label.textContent];
        }
        isToggle ||= input.checked;
    })
    if (isToggle)
        addParams(setParams);

    window.history.pushState({}, '', url);

    const data = await fetchOrder(url.search);
    renderOrder(data['orders'])
    renderPagination(data['total_page'], data['current_page']);
    renderLabel();
}

window.addEventListener("load", function () {
    document.querySelectorAll(".filter-type-item").forEach(item => {
        const input = item.querySelector("input")
        const label = item.querySelector(".dropdown-item")
        if (input.checked) {
            currentLabel[label.textContent] = true;
        } else {
            delete currentLabel[label.textContent];
        }
    })
    renderLabel();
})