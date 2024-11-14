const ele = document.querySelector("#home_category_section");

async function f() {
    const res = await fetch('/category');
    const data = await res.json();
    data.forEach(category => {
        const div = document.createElement("div");
        div.id = category.id;
        div.className = 'px-5';
        div.textContent = category.name;
        ele.appendChild(div);
    })
    return data;
}

data = await f();
ele.addEventListener("click", function(e) {
    const ele = e.target;
    const id = e.getAttribute("id");
    if(!id) return;
    data.forEach(category => {
        if(category.id === id) {
            category.product.slice(0, 10).forEach
        }
    })
})

const renderProduct = function() {

}