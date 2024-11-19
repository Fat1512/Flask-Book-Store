const ele = document.querySelector(".home_category_heading");
const homeProductContainer = document.querySelector('.home_product_container');

let all_data;
async function preLoadCategory() {
    const res = await fetch('/category');
    const data = await res.json();
    const id = data[0].id;
    data.forEach(category => {
        renderCategoryHeading(category.name, category.id, id == category.id)
    })

    all_data = data;
    homeProductContainer.innerHTML = '';
    all_data[0]['product'].slice(0, 10).forEach(data => {
        renderProduct(data);
    })
}
preLoadCategory();

ele.addEventListener("click", function (e) {
    const ele = e.target;
    const id = ele.getAttribute("id");
    if (!id) return;

    e.currentTarget.innerHTML = '';
    all_data.forEach(category => {
        renderCategoryHeading(category.name, category.id, id == category.id)
    })

    homeProductContainer.innerHTML = '';
    all_data.forEach(category => {
        if (category.id == id) {
            category['product'].slice(0, 10).forEach(product => {
                renderProduct(product);
            })
        }
    })
})

const renderCategoryHeading = function (name, id, isActive) {
    const html = `<div id="${id}" class="px-5 home_category_item ${isActive ? 'active' : ''}">${name}</div>`
    ele.insertAdjacentHTML('beforeend', html);
}

const renderProduct = function(product) {
    const html = `
            <a href="#" class="card col-5th">
                <span class="discount text-white">10%</span>
                <img class="card-img-top"
                     src="${product['image_src']}"
                     alt="Card image">
                <div class="card-body p-0">
                    <p class="card-text">${product['product_name']}</p>
                    <p class="text-primary font-weight-bold mb-1">${product['product_price']}đ</p>
                    <p class="text-secondary text-decoration-line-through mb-1">${product['product_price']}đ</p>
                </div>
                <div class="rating">
                    <i class="fa-regular fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                    <i class="fa-regular fa-star"></i>
                </div>
            </a>`;
    homeProductContainer.insertAdjacentHTML('beforeend', html);
}

