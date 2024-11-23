const API = `/api/v1/order`;
const url = new URL(window.location)

const sortParams = [
    {
        "sortBy": "date",
        "dir": "asc"
    },
    {
        "sortBy": "date",
        "dir": "desc"
    },
    {
        "sortBy": "total-amount",
        "dir": "asc"
    },
    {
        "sortBy": "total-amount",
        "dir": "asc"
    }
]

const statusParams = [
    {
        "status": 1
    },
    {
        "status": 2
    },
    {
        "status": 3
    },
    {
        "status": 4
    },
    {
        "status": 5
    }
]
const paymentMethodParams = [
    {
        "payment-method": 1
    },
    {
        "payment-method": 2
    }
]

//---------------------------------------------CONTAINER---------------------------------------------
const dropDownBtn = document.querySelector(".dropdown-btn");
const productSearchBox = document.querySelector('.product-search-box');
const orderTable = document.querySelector(".order-table");
const orderList = document.querySelector(".order-list");

//---------------------------------------------FILTER---------------------------------------------
const orderType = document.querySelector(".order-type");
const sortType = document.querySelector(".sort-type");
const statusType = document.querySelector(".status-type");
const paymentMethodType = document.querySelector(".payment-method-type");

//---------------------------------------------FUNCTION---------------------------------------------
const deleteParams = (params) => params.forEach(param => url.searchParams.delete(param))
const addParams = (params) => params.forEach(param => url.searchParams.set(param[0], param[1]))
const fetchOrder = async function(url) {
    const res = await fetch(url);
    console.log(res, url)

    const data = await res.json();
    console.log(data)
    orderList.innerHTML = '';
    data['orders'].forEach(order => renderOrder(order));
};
//---------------------------------------------EVENT---------------------------------------------
sortType.addEventListener("click", (e) => {
    const item = e.target.closest(".filter-type-item");
    if(!item) return;

    const toggleId = +item.getAttribute("id");
    const parent = item.closest(".sort-type");
    handleFilterChange(parent, Object.entries(sortParams[toggleId - 1]), ["sortBy", "dir"], toggleId);
});


statusType.addEventListener("click", (e) => {
    const item = e.target.closest(".filter-type-item");
    if(!item) return;

    const toggleId = +item.getAttribute("id");
    const parent = item.closest(".status-type");
    handleFilterChange(parent, Object.entries(statusParams[toggleId - 1]), ["status"], toggleId);
});


paymentMethodType.addEventListener("click", (e) => {
    const item = e.target.closest(".filter-type-item");
    if(!item) return;

    const toggleId = +item.getAttribute("id");
    const parent = item.closest(".payment-method-type");
    handleFilterChange(parent, Object.entries(paymentMethodParams[toggleId - 1]), ["payment-method"], toggleId);
});


const handleFilterChange = function(parent, setParams, deletedParams, toggleId) {
    deleteParams(deletedParams);

    let isToggle = false;
    parent.querySelectorAll(".filter-type-item").forEach(item => {
        const itemId = +item.getAttribute("id");
        const input = item.querySelector("input")
        input.checked = itemId === toggleId ? !input.checked : false;
        isToggle ||= input.checked;
    })

    if(isToggle)
        addParams(setParams);
    window.history.pushState({}, '', url);
    console.log(url)
    fetchOrder(`${API}${url.search}`);
}



const renderOrder = function (order) {
    const html = `
        <tr>
            <th scope="row">
                <div class="media align-items-center">
                    <div id="${order['order_id']}">${order['order_id']}</div>
                </div>
            </th>
            <td>
                <div class="media-body">
                    <span class="name mb-0 text-sm">${order['type']['name']}</span>
                </div>
            </td>
            <td class="budget">
                ${order['total_amount']}
            </td>
            <td>
            <span class="badge badge-dot mr-4">
            <i class="bg-warning"></i>
            <span class="status">${ order['status']['name'] }</span>
            </span>
            </td>
            <td>
                <div class="avatar-group">
                    ${ order['created_at'] }
                </div>
            </td>
            <td>
                <div class="avatar-group">
                    ${ order['payment_method']['name'] }
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
                        <a class="dropdown-item"
                           href="/employee/order/update?order_id={{ 123 }}">Cap
                            nhat</a>
                        <a class="dropdown-item"
                           href="/employee/order/{{ order['order_id'] }}/detail">Chi
                            tiet</a>
                        <a class="dropdown-item" href="#">Huy</a>
                    </div>
                </div>
            </td>
        </tr>`
    orderList.insertAdjacentHTML('beforeend', html);
}
