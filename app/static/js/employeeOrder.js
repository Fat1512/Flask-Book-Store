const dropDownBtn = document.querySelector(".dropdown-btn");
const productSearchBox = document.querySelector('.product-search-box');
const orderTable = document.querySelector(".order-table");

const API = `/api/v1/order`;
const orderType = document.querySelector(".order-type");

const sortType = document.querySelector(".sort-type");
const sortTypeItem = document.querySelectorAll(".sort-type-item")

const statusType = document.querySelector(".status-type");
const paymentMethodType = document.querySelector(".payment-method-type");


sortType.addEventListener("click", (e) => {
    const item = e.target.closest(".sort-type-item");
    if(!item) return;

    const toggleId = +item.getAttribute("id");
    sortTypeItem.forEach(item => {
        const itemId = +item.getAttribute("id");
        const input = item.querySelector("input")
        input.checked = itemId === toggleId ? !input.checked : false;
    })
});