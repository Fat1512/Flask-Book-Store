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

//---------------------------------------------FUNCTION---------------------------------------------

const currentLabel = {};

const deleteParams = (params) => params.forEach(param => url.searchParams.delete(param))
const addParams = (params) => params.forEach(param => url.searchParams.set(param[0], param[1]))
const renderOrder = function (orders) {
    console.log(orders);
    orderList.innerHTML = '';
    const html = orders.map(order => `
        <tr>
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
                        ${ +order['order_type']['id'] === 1 && +order['payment']['payment_method']['id'] === 2 && (+order['status']['id'] === 1 || +order['status']['id'] === 2) ? `
                            <a class="dropdown-item"
                               href="/employee/order/${order['order_id']}/update">Cap nhat</a>` : ''}
                        ${ +order['order_type']['id'] === 1 && +order['payment']['payment_method']['id'] === 2 && +order['status']['id'] === 1 ? `
                        <a class="dropdown-item" value="confirm" order-id="${order['order_id']}" href="">Xac nhan</a>` : ''} 
                        
                        
                        <a class="dropdown-item"
                           href="/employee/order/${order['order_id']}/detail">Chi
                            tiet</a>
                        <a class="dropdown-item" href="#">Huy</a>
                    </div>
                </div>
            </td>
        </tr>`).join("");
    orderList.insertAdjacentHTML('beforeend', html);
}
const renderPagination = function (total_page, current_page) {
    console.log(current_page, total_page)
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

const fetchOrder = async function (param) {
    try {
        const res = await fetch(`${ORDER_API}${param}`);
        if (!res.ok) throw new Error("Cannot fetch order");
        return await res.json();
    } catch (err) {
        alert(err.message);
    }
};

const modifyOrderStatus = async function (orderId) {
    try {
        try {
            const res = await fetch(`${ORDER_API}/${orderId}/confirm`);
            if (!res.ok) throw new Error("update order status");
            return await res.json();
        } catch (err) {
            alert(err.message);
        }
    } catch(err) {
        alert(err.message);
    }
}

//---------------------------------------------EVENT---------------------------------------------

orderList.addEventListener("click", async function (e) {
    const target = e.target.closest(".dropdown-item");
    if (!target) return;
    const isConfirmed = e.target.getAttribute("value");
    if (isConfirmed !== "confirm") return;
    const orderId = e.target.getAttribute("order-id");
    await modifyOrderStatus(orderId);

});

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