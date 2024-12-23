//---------------------------------------------CONSTANTS---------------------------------------------
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

const Color = {
    WARNING: "orange",
    ERROR: `var(--red)`,
    SUCCESS: "#6cbf6c"
}

const ORDER_API = `/api/v1/order`;
const url = new URL(window.location);

const orderParams = {
    DAT_ONLINE: {
        "orderType": 1 //Dat online
    },
    MUA_TRUC_TIEP: {
        "orderType": 2 //Mua truc tiep
    }
};

const sortParams = {
    NGAY_DAT_MOI: {
        "sortBy": "date",
        "dir": "desc"
    },
    NGAY_DAT_CU: {
        "sortBy": "date",
        "dir": "asc"
    },
    TONG_TIEN_TANG: {
        "sortBy": "total-amount",
        "dir": "asc"
    },
    TONG_TIEN_GIAM: {
        "sortBy": "total-amount",
        "dir": "desc"
    }
};
const statusParams = {
    DANG_XU_LY: {
        "status": 1
    },
    CHO_GIAO_HANG: {
        "status": 2
    },
    DANG_GIAO_HANG: {
        "status": 3
    },
    DA_HOAN_THANH: {
        "status": 4
    },
    DA_HUY: {
        "status": 5
    },
    DANG_CHO_THANH_TOAN: {
        "status": 6
    },
    DA_THANH_TOAN: {
        "status": 7
    },
    DANG_CHO_NHAN_HANG: {
        "status": 8
    }
};

const paymentMethodParams = {
    THE: {
        "paymentMethod": 1 //The
    },
    TIEN_MAT: {
        "paymentMethod": 2 //Tien mat
    }
};


//shipping method = 1: ship ve nha
//shipping method = 2: cua hang
const shippingStatus = {
    "1": {//shipping id
        "1": "Đang xử lý", //order status id
        "2": "Chờ giao hàng",
        "3": "Đang giao hàng",
        "4": "Đã hoàn thành"
    },
    "2": {
        "1": "Đang xử lý",
        "8": "Đang chờ nhận",
        "4": "Đã hoàn thành"
    }
};

const initialTabState = [
    {},
    {
        "orderType": 1,
        "paymentMethod": 2,
        "status": "1,2,8"
    },
    {
        "orderType": 1,
        "status": "1,2,3,8"
    },
    {
        "orderType": 1,
        "paymentMethod": 2,
        "status": "1,2,8"
    }
]


/**
 *     DANG_XU_LY = 1
 *     CHO_GIAO_HANG = 2
 *     DANG_GIAO_HANG = 3
 *     DA_HOAN_THANH = 4
 *     DA_HUY = 5
 *     DANG_CHO_THANH_TOAN = 6
 *     DA_THANH_TOAN = 7
 *     DANG_CHO_NHAN_HANG = 8
 */


//---------------------------------------------DOM ELEMENTS & STATES---------------------------------------------
const orderList = document.querySelector(".order-list");
const pagination = document.querySelector(".pagination");
const filterLabelContainer = document.querySelector(".filter-label-container");

const orderType = document.querySelector(".order-type");
const sortType = document.querySelector(".sort-type");
const statusType = document.querySelector(".status-type");
const paymentMethodType = document.querySelector(".payment-method-type");


const orderTab = document.querySelector(".order-tab");
const dateSearchContainer = document.querySelector(".date-search-container");
const filterDropListContainer = document.querySelector(".filter-droplist-container");
const modal = document.querySelector(".modal");
const modalUpdateOrderStatusBody = document.querySelector(".modal-update-order-status");
const modalCancelOrder = document.querySelector(".modal-cancel-order");
const overlay = document.querySelector(".overlay");

const btnResetAll = document.querySelector(".btn-reset-all");
const btnSearch = document.querySelector(".btn-search");
const inputStartDate = document.querySelector(".input-start-date");
const inputEndDate = document.querySelector(".input-end-date");
const inputSearch = document.querySelector(".input-search");

let currentLabel = {};
let currentSearchParam = {};
let currentOrderItemsState = {};
let currentTab = 0;
//---------------------------------------------RENDER---------------------------------------------
const renderOrder = function (orders, tab = 0) {
    let html = orders.map(order => {
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
    }).join('');
    orderList.innerHTML = '';

    if (orders.length === 0) {
        html = `
        <tr>
            <td colspan="6">
                <div class="text-center w-100 display-4">Không có đơn</div>
            </td>
        </tr>`;
    }
    orderList.insertAdjacentHTML('beforeend', html);
};

const renderPagination = function (total_page, current_page) {
    const prev = `
        <li class="page-item ${current_page == 1 || total_page == 0 ? "disabled" : ""}" page=${current_page - 1}>
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
        <li class="page-item ${current_page == total_page || total_page == 0 ? "disabled" : ""}" page=${current_page + 1}>
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
    <div class="card p-5 order-update-modal" id="${order['order_id']}">
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
                    <h2 class="font-weight-400"> ${dateFormatter.format(new Date(order['created_at']))} </h2>
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
                                    <span>${order['address']['fullname']}</span>
                                </div>
                                <div class="col-lg-12">
                                        <span class="form-control-label"
                                              for="input-address">Địa chỉ: </span>
                                    <span>${order['address']['address']} ${order['address']['province']}</span>
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
    modalUpdateOrderStatusBody.innerHTML = '';
    modalUpdateOrderStatusBody.insertAdjacentHTML("beforeend", html);
};

const renderCancelForm = function (order) {
    const html = `
        <div class="w-100 d-flex justify-content-center align-content-center flex-column order-cancel-modal" id="${order['order_id']}">
            <h1 class="modal-title d-flex justify-content-center pt-4" id="modalLabel">
                <i class="fas fa-exclamation-circle text-warning display-1"></i>
            </h1>
             <h2 class="text-center">Lý do hủy ?</h2>
            <input type="text" class="cancel-reason">
            <div class="d-flex pt-4">
                <button type="button"
                        class="cancel-back-btn w-50 btn btn-primary bg-white text-black border border-0"
                        style="color: var(--black-color) !important">
                    Trở lại
                </button>
                <button type="button"
                        class="cancel-btn w-50 btn btn-primary border border-0"
                        style="color: var(--white-color) !important; background-color: var(--red)">
                    Hủy
                </button>
            </div>
        </div>`;
    modalCancelOrder.innerHTML = '';
    modalCancelOrder.insertAdjacentHTML("beforeend", html);
};

const renderToast = function (text, background) {
    Toastify({
        text: text,
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: "top",
        position: "right",
        stopOnFocus: true,
        style: {
            background: background,
        }
    }).showToast();
}
//---------------------------------------------API UTILITY---------------------------------------------
const fetchOrder = async function () {
    try {
        const param = '?' + Object.entries(currentSearchParam).map(pr => pr[0] + '=' + pr[1]).join("&");
        const res = await fetch(`${ORDER_API}${param}`);
        if (!res.ok) throw new Error("Có lỗi khi lấy đơn");

        const data = await res.json();
        if (data['status'] !== 200) throw new Error(data['message']);

        return data['data'];
    } catch (err) {
        throw err;
    }
};

const modifyOrderStatus = async function (orderId, orderStatusId) {
    try {
        const res = await fetch(`${ORDER_API}/${orderId}/status`, {
            method: "POST",
            body: JSON.stringify({"orderStatusId": orderStatusId}),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!res.ok) throw new Error("Có lỗi khi cập nhật trạng thái");

        const data = await res.json();
        if (data['status'] !== 200) throw new Error(data['message']);

        return data['data'];
    } catch (err) {
        throw err;
    }
};

const cancelOrder = async function (orderId, reason) {
    try {
        const res = await fetch(`${ORDER_API}/orderCancellation`, {
            method: "POST",
            body: JSON.stringify({
                "orderId": orderId,
                "reason": reason
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!res.ok) throw new Error("Có lỗi khi hủy");

        const data = await res.json();
        if (data['status'] !== 200) throw new Error(data['message']);

        return data['data'];
    } catch (err) {
        throw err;
    }
}

//---------------------------------------------DOM UTILITY---------------------------------------------
const openModal = function () {
    overlay.classList.add("d-flex");
    modal.classList.add("d-flex");
}

const closeModal = function () {
    overlay.classList.remove("d-flex");
    modal.classList.remove("d-flex");
    modalUpdateOrderStatusBody.classList.add("d-none");
    modalCancelOrder.classList.add("d-none");
}

const openUpdateOrderStatusModal = function () {
    openModal();
    modalUpdateOrderStatusBody.classList.remove("d-none");
}

const openCancelOrderModal = function () {
    openModal();
    modalCancelOrder.classList.remove("d-none");
}

const resetAllState = function () {
    currentLabel = {};
    currentSearchParam = JSON.parse(JSON.stringify(initialTabState[currentTab]));
    inputStartDate.value = '';
    inputEndDate.value = '';
    inputSearch.value = '';

    renderLabel()
    document.querySelectorAll("input:checked").forEach(input => input.checked = false);

    url.search = "";
    window.history.pushState({}, '', url);
}

const hideFilter = function () {
    filterDropListContainer.classList.add("hide");
    dateSearchContainer.classList.add("hide");
}

const unhideFilter = function () {
    filterDropListContainer.classList.remove("hide");
    dateSearchContainer.classList.remove("hide");
};

const deleteCurrentParams = (params) => params.forEach(param => delete currentSearchParam[param]);

const addCurrentParams = (params) => params.forEach(param => currentSearchParam[param[0]] = param[1]);

const deleteUrlParams = (params) => params.forEach(param => url.searchParams.delete(param));

const addUrlParams = (params) => params.forEach(param => url.searchParams.set(param[0], param[1]));

const handleFilterChange = async function (parent, setParams, deletedParams, toggleId) {
    try {
        deleteUrlParams(deletedParams);
        deleteCurrentParams(deletedParams);

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

        if (isToggle) {
            addCurrentParams(setParams)
            addUrlParams(setParams);
        }

        window.history.pushState({}, '', url);

        const data = await fetchOrder();
        renderOrder(data['orders'])
        renderPagination(data['total_page'], data['current_page']);
        renderLabel();
    } catch (err) {
        renderToast(err.message, Color.ERROR);
    }
};


//---------------------------------------------EVENT---------------------------------------------
inputStartDate.addEventListener("change", async function (e) {
    try {
        const value = inputStartDate.value;
        if (!value) {
            deleteCurrentParams(["startDate"])
            deleteUrlParams(["startDate"]);
        } else {
            addCurrentParams([["startDate", value]]);
            addUrlParams([["startDate", value]]);
        }
        window.history.pushState({}, '', url);

        const data = await fetchOrder();

        renderOrder(data['orders']);
        renderPagination(data['total_page'], data['current_page']);
    } catch (err) {
        renderToast(err.message, Color.ERROR);
    }
});

inputEndDate.addEventListener("change", async function (e) {
    try {
        const value = inputEndDate.value;
        if (!value) {
            deleteCurrentParams(["endDate"])
            deleteUrlParams(["endDate"]);
        } else {
            addCurrentParams([["endDate", value]]);
            addUrlParams([["endDate", value]]);
        }
        window.history.pushState({}, '', url);

        const data = await fetchOrder();

        renderOrder(data['orders']);
        renderPagination(data['total_page'], data['current_page']);
    } catch (err) {
        renderToast(err.message, Color.ERROR);
    }
});

btnResetAll.addEventListener("click", async function () {
    try {
        resetAllState();

        const data = await fetchOrder();

        renderOrder(data['orders']);
        renderPagination(data['total_page'], data['current_page']);
    } catch (err) {
        renderToast(err.message, Color.ERROR);
    }
});

btnSearch.addEventListener("click", async function () {
    try {
        const orderId = inputSearch.value;
        if (orderId.trim() === '') return;

        resetAllState();
        currentSearchParam = JSON.parse(JSON.stringify(initialTabState[currentTab]));

        currentSearchParam['orderId'] = orderId;
        const data = await fetchOrder();

        renderOrder(data['orders'], currentTab);
        renderPagination(data['total_page'], data['current_page']);
    } catch (err) {
        renderToast(err.message, Color.ERROR);
    }
})

modalUpdateOrderStatusBody.addEventListener("click", async function (e) {
    try {
        const input = e.target.closest("input");
        const confirmBtn = e.target.closest(".btn-confirm-change-status");
        if (input) {
            const currentState = input.checked;
            modalUpdateOrderStatusBody.querySelectorAll("input").forEach(inp => inp.checked = false);
            input.checked = currentState;
        }
        if (confirmBtn) {
            const orderId = modalUpdateOrderStatusBody.querySelector(".order-update-modal").getAttribute("id");
            const selectedStatusId = modalUpdateOrderStatusBody.querySelector("input:checked").getAttribute("id");
            await modifyOrderStatus(orderId, selectedStatusId);
            renderToast("Cập nhật thành công", Color.SUCCESS);

            const data = await fetchOrder();
            renderOrder(data['orders'], currentTab)
            renderPagination(data['total_page'], data['current_page']);
            closeModal();
        }
    } catch (err) {
        renderToast(err.message, Color.ERROR);
    }
});

modalCancelOrder.addEventListener("click", async function (e) {
    try {
        const cancelBtn = e.target.closest(".cancel-btn");
        const backCancelBtn = e.target.closest(".cancel-back-btn");
        if (cancelBtn) {
            const orderId = modalCancelOrder.querySelector(".order-cancel-modal").getAttribute("id");
            const reason = modalCancelOrder.querySelector(".cancel-reason").value;

            await cancelOrder(orderId, reason);
            renderToast("Đã hủy thành công", Color.SUCCESS);

            const data = await fetchOrder();
            renderOrder(data['orders']);
            renderPagination(data['total_page'], data['current_page']);
            closeModal();
        }
        if (backCancelBtn) {
            closeModal();
        }
    } catch (err) {
        renderToast(err.message, Color.ERROR);
    }
});

orderTab.addEventListener("click", async function (e) {
    try {
        const allOrder = e.target.closest(".all-order");
        const updateOrderInfo = e.target.closest(".update-order-info");
        const updateOrderStatus = e.target.closest(".update-order-status");
        const cancelOrder = e.target.closest(".cancel-order");

        let data;
        if (allOrder) {
            currentTab = 0;
            currentSearchParam = JSON.parse(JSON.stringify(initialTabState[currentTab]));
            unhideFilter();
        } else {
            if (updateOrderInfo) {
                currentTab = 1;
                currentSearchParam = JSON.parse(JSON.stringify(initialTabState[currentTab]));
            }
            if (updateOrderStatus) {
                currentTab = 2;
                currentSearchParam = JSON.parse(JSON.stringify(initialTabState[currentTab]));
            }
            if (cancelOrder) {
                currentTab = 3;
                currentSearchParam = JSON.parse(JSON.stringify(initialTabState[currentTab]));
            }
            hideFilter()
        }

        data = await fetchOrder();
        renderOrder(data['orders'], currentTab);
        console.log(data);
        renderPagination(data['total_page'], data['current_page']);
        resetAllState();
    } catch (err) {
        renderToast(err.message, Color.ERROR);
    }
});

orderList.addEventListener("click", async function (e) {
    const target = e.target.closest(".dropdown-item");
    if (!target) return;
    const tab = +target.getAttribute("tab");
    const orderId = e.target.closest(".order-id").getAttribute("id");

    switch (tab) {
        case 0: {
            window.open(`/employee/order/${orderId}/detail`, "_blank");
            break;
        }
        case 1: {
            window.open(`/employee/order/${orderId}/update`, "_blank");
            break;
        }
        case 2: {
            const order = currentOrderItemsState[orderId];

            const shippingMethodId = order['order_type']['detail']['shipping_method']['id'];
            const statusId = order['status']['id'];

            const idx = Object.keys(shippingStatus[shippingMethodId]).indexOf(`${statusId}`);
            const statusArray = Object.entries(shippingStatus[shippingMethodId]).slice(idx + 1);

            renderStatusUpdateForm(order, statusArray);
            openUpdateOrderStatusModal();
            break;
        }
        case 3: {
            const order = currentOrderItemsState[orderId];

            renderCancelForm(order);
            openCancelOrderModal();
            break;
        }
    }
});

overlay.addEventListener("click", closeModal)

sortType.addEventListener("click", (e) => {
    const item = e.target.closest(".filter-type-item");
    if (!item) return;

    const toggleId = +item.getAttribute("id");
    handleFilterChange(sortType, Object.entries(sortParams[Object.keys(sortParams)[toggleId - 1]]), ["sortBy", "dir", "orderId"], toggleId);
});

statusType.addEventListener("click", (e) => {
    const item = e.target.closest(".filter-type-item");
    if (!item) return;

    const toggleId = +item.getAttribute("id");
    handleFilterChange(statusType, Object.entries(statusParams[Object.keys(statusParams)[toggleId - 1]]), ["status", "page", "orderId"], toggleId);
});

paymentMethodType.addEventListener("click", (e) => {
    const item = e.target.closest(".filter-type-item");
    if (!item) return;

    const toggleId = +item.getAttribute("id");

    handleFilterChange(paymentMethodType, Object.entries(paymentMethodParams[Object.keys(paymentMethodParams)[toggleId - 1]]), ["paymentMethod", "page", "orderId"], toggleId);
});

orderType.addEventListener("click", (e) => {
    const item = e.target.closest(".filter-type-item");
    if (!item) return;

    const toggleId = +item.getAttribute("id");
    handleFilterChange(orderType, Object.entries(orderParams[Object.keys(orderParams)[toggleId - 1]]), ["orderType", "page", "orderId"], toggleId);
});

pagination.addEventListener("click", async function (e) {
    try {
        const item = e.target.closest(".page-item");
        if (!item || item.classList.contains("disabled") || item.classList.contains("active")) return;

        deleteUrlParams(["page"]);
        deleteCurrentParams(["page"]);

        addUrlParams([["page", item.getAttribute("page")]]);
        addCurrentParams([["page", item.getAttribute("page")]]);

        window.history.pushState({}, '', url);

        const data = await fetchOrder();
        renderOrder(data['orders'])
        renderPagination(data['total_page'], data['current_page']);
    } catch (err) {
        renderToast(err.message, Color.ERROR);
    }
})

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

// const barcode = '12341234'
// let barcodeDigit = barcode.split('');
// barcodeDigit = barcodeDigit.slice(0, barcode.length - 1);
//
// const sumOdd = barcodeDigit.reduce((acc, cur, idx) => idx % 2 !== 0 ? acc + +cur : acc, 0);
// const sumEven = barcodeDigit.reduce((acc, cur, idx) => idx % 2 === 0 ? acc + +cur : acc, 0);
// const totalSum = sumOdd + sumEven;
// const checkDigit = (10 - (totalSum % 10)) % 10
// barcodeDigit.push(checkDigit)
// barcodeDigit = barcodeDigit.join('');
// console.log(barcode)
// console.log(barcodeDigit)
// console.log(barcode === barcodeDigit)