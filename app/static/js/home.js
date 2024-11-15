const ele = document.querySelector(".home_category_heading");
const homeProductContainer = document.querySelector('.home_product_container');

let all_data;
async function preLoadCategory() {
    const res = await fetch('/category');
    const data = await res.json();
    data.forEach(category => {
        const div = document.createElement("div");
        div.id = category.id;
        div.className = 'px-5';
        div.textContent = category.name;
        ele.appendChild(div);
    })
    all_data = data;
    homeProductContainer.innerHTML = '';
    console.log(data)
    all_data[0]['product'].slice(0, 10).forEach(data => {
        renderProduct(data);
    })
}
preLoadCategory();

ele.addEventListener("click", function (e) {
    const ele = e.target;
    const id = ele.getAttribute("id");
    if (!id) return;

    homeProductContainer.innerHTML = '';

    all_data.forEach(category => {
        if (category.id == id) {
            category['product'].slice(0, 10).forEach(product => {
                renderProduct(product);
            })
        }
    })
})

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

