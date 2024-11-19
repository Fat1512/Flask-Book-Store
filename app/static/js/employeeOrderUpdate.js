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
})
