const TIME_OUT = 100;
const placeHolderAttribute = ["Nhap ten san pham", "Nhap barcode"]
let fetchOption = 0;
let currentTimeOutId;

const productSearchBox = document.querySelector('.product-search-box');
const dropDownBtn = document.querySelector(".dropdown-btn");

const orderContainer = document.querySelector(".order-container");
const productContainer = document.querySelector(".product-container");

const fetchProductByBarcode = async function() {
    console.log("Fetching by barcode");
    //Logic................
}

const fetchProductByName = async function() {
    console.log("Fetching by name");
    //Logic................
}

const productFetchingFunction = [fetchProductByName, fetchProductByBarcode];

productSearchBox.addEventListener("input", function () {
    clearTimeout(currentTimeOutId);
    currentTimeOutId = setTimeout(function() {
        productFetchingFunction[fetchOption]();
    }, TIME_OUT);
});

dropDownBtn.addEventListener("click", function(e) {
    e.preventDefault();
    const target = e.target.closest('.dropdown-item');
    if(!target) return;
    fetchOption = +e.target.getAttribute("id");
    productSearchBox.setAttribute("placeholder", placeHolderAttribute[fetchOption]);
});

productContainer.addEventListener("click", function(e) {
    const productItem = e.target.closest(".product-item");
    if(!productItem) return;
    console.log(productItem)
});

orderContainer.addEventListener("click", function(e) {
    const productItem = e.target.closest(".remove-order-item-btn");
    if(!productItem) return;
    productItem.closest(".order-item").remove();
});

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