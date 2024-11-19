const dropDownBtn = document.querySelector(".dropdown-btn");
const productSearchBox = document.querySelector('.product-search-box');
const orderTable = document.querySelector(".order-table");
const productDetail = document.querySelector(".product-detail");
const productDetailBack = document.querySelector(".product-detail-back-btn");

const TIME_OUT = 100;
const placeHolderAttribute = ["Nhap ten san pham", "Nhap barcode"]
let fetchOption = 0;
let currentTimeOutId;

const fetchProductByBarcode = async function() {
    console.log("Fetching by barcode");
    //Logic................
}

const fetchProductByName = async function() {
    console.log("Fetching by name");
    //Logic................
}

const productFetchingFunction = [fetchProductByName, fetchProductByBarcode];
dropDownBtn.addEventListener("click", function(e) {
    e.preventDefault();
    const target = e.target.closest('.dropdown-item');
    if(!target) return;
    fetchOption = +e.target.getAttribute("id");
    productSearchBox.setAttribute("placeholder", placeHolderAttribute[fetchOption]);
})

productSearchBox.addEventListener("input", function () {
    clearTimeout(currentTimeOutId);
    currentTimeOutId = setTimeout(function() {
        productFetchingFunction[fetchOption]();
    }, TIME_OUT);
});

orderTable.addEventListener("click", function(e) {
    const target = e.target.closest(".dropdown-item");
    if(!target) return;
    const optionId = +target.getAttribute("id");
    const orderID = +e.target.closest("tr").querySelector("#order-id").textContent;
    console.log(optionId);
    console.log(orderID);
    if(optionId === 1) {
        productDetail.classList.toggle("d-none");
        orderTable.classList.toggle("d-none");
    }
    //More logic...
    /*
    option = 1 => update
    option = 2 => cancel
    option = 3 => detail product
     */
})

productDetailBack.addEventListener("click", function() {
    console.log("2");
    productDetail.classList.toggle("d-none");
        orderTable.classList.toggle("d-none");
})


