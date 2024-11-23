const API = `/api/v1/order`;
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

//---------------------------------------------FILTER---------------------------------------------
const orderType = document.querySelector(".order-type");
const sortType = document.querySelector(".sort-type");
const statusType = document.querySelector(".status-type");
const paymentMethodType = document.querySelector(".payment-method-type");

//---------------------------------------------FUNCTION---------------------------------------------
const deleteParams = (params) => params.forEach(param => url.searchParams.delete(param))
const addParams = (params) => params.forEach(param => url.searchParams.set(param[0], param[1]))
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
                    <span class="name mb-0 text-sm">${order['order_type']['name']}</span>
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
                    ${ order['payment']['payment_method']['name'] }
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
                        ${+order['status']['id'] === 1 || +order['status']['id'] === 2 ? `
                            <a class="dropdown-item"
                               href="/employee/order/${order['order_id']}/update">Cap nhat</a>`: ''}
                        <a class="dropdown-item"
                           href="/employee/order/${order['order_id']}/detail">Chi
                            tiet</a>
                        <a class="dropdown-item" href="#">Huy</a>
                    </div>
                </div>
            </td>
        </tr>`
    orderList.insertAdjacentHTML('beforeend', html);
}
const renderPagination = function(total_page, current_page) {
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
const fetchOrder = async function(url) {
    const res = await fetch(url);
    console.log(res, url)

    const data = await res.json();
    orderList.innerHTML = '';
    data['orders'].forEach(order => renderOrder(order));
    renderPagination(data['total_page'], data['current_page']);
};
//---------------------------------------------EVENT---------------------------------------------
sortType.addEventListener("click", (e) => {
    const item = e.target.closest(".filter-type-item");
    if(!item) return;

    const toggleId = +item.getAttribute("id");
    handleFilterChange(sortType, Object.entries(sortParams[toggleId - 1]), ["sortBy", "dir"], toggleId);
});


statusType.addEventListener("click", (e) => {
    const item = e.target.closest(".filter-type-item");
    if(!item) return;

    const toggleId = +item.getAttribute("id");
    handleFilterChange(statusType, Object.entries(statusParams[toggleId - 1]), ["status"], toggleId);
});


paymentMethodType.addEventListener("click", (e) => {
    const item = e.target.closest(".filter-type-item");
    if(!item) return;

    const toggleId = +item.getAttribute("id");
    handleFilterChange(paymentMethodType, Object.entries(paymentMethodParams[toggleId - 1]), ["paymentMethod"], toggleId);
});

orderType.addEventListener("click", (e) => {
    const item = e.target.closest(".filter-type-item");
    if(!item) return;

    const toggleId = +item.getAttribute("id");
    handleFilterChange(orderType, Object.entries(orderParams[toggleId - 1]), ["orderType"], toggleId);
});

pagination.addEventListener("click", (e) => {
    const item = e.target.closest(".page-item");
    if(!item || item.classList.contains("disabled") || item.classList.contains("active")) return;

    deleteParams(["page"])
    addParams([["page", item.getAttribute("page")]]);
    window.history.pushState({}, '', url);
    fetchOrder(`${API}${url.search}`);
})


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
    fetchOrder(`${API}${url.search}`);
}

