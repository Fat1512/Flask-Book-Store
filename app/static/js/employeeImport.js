const bookList = document.querySelector(".book-list");
const modal = document.querySelector(".modal");
const modalBody = document.querySelector(".modal-body");
const overlay = document.querySelector(".overlay");

const openModalBtn = document.querySelector(".open-modal-btn");
const allCheckBox = document.querySelector(".all-check-box");
const statusType = document.querySelector(".status-type");
const addBookBtn = document.querySelector(".add-book-btn");
const importList = document.querySelector(".import-list");
const importContainer = document.querySelector(".import-container");

const deleteBtn = document.querySelector(".delete-all-btn");
const exportBtn = document.querySelector(".export-btn");

let currentCheckedBookState = {};
let currentItemState = {};

const url = new URL(window.location);
const BOOK_API = "/api/v1/book/manage"
const CONFIG_API = "/api/v1/config"
let config;

const openModal = function () {
    modal.classList.add("d-flex");
    overlay.classList.add("d-flex");
}

const closeModal = function () {
    modal.classList.remove("d-flex");
    overlay.classList.remove("d-flex");
}

const removeAllCheckedBox = function() {
    currentCheckedBookState = {};
    bookList.querySelectorAll("input").forEach(input => input.checked = false);
    allCheckBox.checked = false;
}

overlay.addEventListener("click", () => {
    closeModal();
    removeAllCheckedBox();
});
openModalBtn.addEventListener("click", openModal);

bookList.addEventListener("click", function (e) {
    const bookItem = e.target.closest(".book-item");
    if (!bookItem) return;

    const checkedBox = bookItem.querySelector("input");
    checkedBox.checked = !checkedBox.checked;
    const bookItemData = extractBookItemData(bookItem);

    if (checkedBox.checked) {
        currentCheckedBookState[bookItemData['bookId']] = bookItemData;
    } else {
        delete currentCheckedBookState[bookItemData['bookId']];
    }
});

allCheckBox.addEventListener("click", function (e) {
    if (allCheckBox.checked) {
        document.querySelectorAll(".book-item").forEach(bookItem => {
            bookItem.querySelector("input").checked = true;
            const bookItemData = extractBookItemData(bookItem);
            currentCheckedBookState[bookItemData['bookId']] = bookItemData;
        });
    } else {
        document.querySelectorAll(".book-item").forEach(bookItem => {
            bookItem.querySelector("input").checked = false;
            const bookItemData = extractBookItemData(bookItem);
            delete currentCheckedBookState[bookItemData['bookId']];
        });
    }
});

addBookBtn.addEventListener("click", function() {
    Object.entries(currentCheckedBookState).forEach(item => {
        if(currentItemState[item[0]]) {
            currentItemState[item[0]]['quantity'] += 1;
        } else {
            currentItemState[item[0]] = item[1];
            currentItemState[item[0]]['quantity'] = config['min_restock_qty'];
        }
    });

    renderImportedItems();
    removeAllCheckedBox();
    closeModal();
});

statusType.addEventListener("click", async function(e)  {

    const filterItem = e.target.closest(".filter-type-item");
    if (!filterItem) return;

    const toggleId = +filterItem.getAttribute("id");
    let isToggle = false;

    statusType.querySelectorAll(".filter-type-item").forEach(item => {
        const itemId = +item.getAttribute("id");
        const input = item.querySelector("input")

        input.checked = itemId === toggleId ? !input.checked : false;
        isToggle ||= input.checked;
    })
    url.searchParams.delete("quantityStatus");

    if(isToggle)
        url.searchParams.set("quantityStatus", toggleId);
    try {
        const data = await fetchBook();
        renderBookItems(data['books']);
    } catch (err) {
        alert(err.message);
    }
});

importContainer.addEventListener("click", function(e) {
    const removeBtn = e.target.closest(".remove-import-item-btn");
    const incrementBtn = e.target.closest(".increment-qty-btn");
    const decrementBtn = e.target.closest(".decrement-qty-btn");
    const id = e.target.closest(".import-item")?.getAttribute("id");

    let isTriggered = false;

    if (removeBtn) {
        delete currentItemState[+id];
        isTriggered ||= true;
    }
    if (incrementBtn) {
        const input = incrementBtn.previousElementSibling;
        currentItemState[+id]['quantity'] = +input.value + 1;
        isTriggered ||= true;
    }
    if (decrementBtn) {
        const input = decrementBtn.nextElementSibling;
        currentItemState[+id]['quantity'] = input.value > 1 ? +input.value - 1 : input.value;
        isTriggered ||= true;
    }
    isTriggered && renderImportedItems();
})

importContainer.addEventListener("change", function(e) {
    const input = e.target;
    if (input.value < config['min_restock_qty'] || input.value === '') input.value = config['min_restock_qty'];
    currentItemState[+input.getAttribute("input-id")]['quantity'] = +input.value;
    renderImportedItems()
})

const extractBookItemData = function (bookItem) {
    const bookId = +bookItem.querySelector(".book-item-id").textContent.trim();
    const title = bookItem.querySelector(".book-item-title").textContent.trim();
    const gerne = bookItem.querySelector(".book-item-gerne").textContent.trim();
    const author = bookItem.querySelector(".book-item-author").textContent.trim();
    const img = bookItem.querySelector(".book-item-img").getAttribute("src");
    return {
        bookId,
        img,
        title,
        gerne,
        author,
    };
};

const renderImportedItems = function() {
    importList.innerHTML = '';
    const html = Object.entries(currentItemState).map(item => {
        return `
        <tr class="import-item" id="${item[1]['bookId']}">
            <th scope="row">
                <div class="media align-items-center">
                    <div class="media-body text-center">
                        <span class="name mb-0 text-sm text-center w-100">${item[1]['bookId']}</span>
                    </div>
                </div>
            </th>
            <td scope="row" class="justify-content-center">
                <div class="media align-items-center text-center" style="width:50px">
                    <img src="${item[1]['img']}"
                         alt="" class="h-100 img-fluid book-item-img">
                </div>
            </td>
            <td class="budget text-center">
                <div class="media align-items-center">
                    <div class="media-body text-left text-truncate" style="width: 100px !important;">
                        <span class="order-item-name mb-0 text-sm text-center w-100">${item[1]['title']}</span>
                    </div>
                </div>
            </td>
            <td>
                <span class="badge badge-dot mr-4 text-center w-100">
                <span class="status text-center">${item[1]['gerne']}</span>
                </span>
            </td>
            <td>
                <div class="d-flex align-items-center w-100 justify-content-center">
                    <span class="completion mr-2">${item[1]['author']}</span>
                </div>
            </td>
            <td>
                <div class="d-flex justify-content-center">
                    <div class="d-flex justify-content-between align-content-center w-100">
                        <span class="cursor-pointer decrement-qty-btn">-</span>
                        <input input-id="${item[1]['bookId']}" inputmode="numeric"
                               oninput="this.value = this.value.replace(/\\\\D+/g, '')"
                               class="text-center" value="${item[1]['quantity']}">
                        <span class="cursor-pointer increment-qty-btn">+</span>
                    </div>
                </div>
            </td>
            <td class="text-right remove-import-item-btn">
                <div class="dropdown">
                    <a class="btn btn-sm btn-icon-only text-light cursor-pointer" role="button">
                        <i class="fa fa-window-close" aria-hidden="true"></i>
                    </a>
                </div>
            </td>
        </tr>`}).join("");
    importList.insertAdjacentHTML("beforeend", html);
}

const renderBookItems = function(books) {
    bookList.innerHTML = '';
    const html = books.map(book => `
        <tr class="cursor-pointer book-item" id="${book['book_id']}">
            <th scope="row">
                <div class="media align-items-center">
                    <input type="checkbox" ${currentCheckedBookState[book['book_id']] != null ? 'checked' : ''}>
                </div>
            </th>
            <td scope="row">
                <div class="media align-items-center">
                    <div class="book-item-id" id="1">${book['book_id']}</div>
                </div>
            </td>
            <td scope="row" class="justify-content-center">
                <div class="media align-items-center text-center" style="width:50px">
                    <img src="${book.images?.[0]?.image_url}" 
                         alt="" class="h-100 img-fluid book-item-img">
                </div>
            </td>
            <td>
                <div class="media-body text-truncate" style="width:200px">
                    <span class="name mb-0 text-xs w-100 book-item-title">${book['title']}</span>
                </div>
            </td>
            <td>
                <div class="media-body">
                    <span class="name mb-0 text-xs book-item-barcode">${book['barcode']}</span>
                </div>
            </td>
            <td class="budget book-item-gerne">
                ${book['gerne']['name']}
            </td>
            <td>
                <span class="badge badge-dot mr-4">
                <i class="bg-warning"></i>
                <span class="status book-item-quantity">${book['quantity']}</span>
                </span>
            </td>
            <td>
                <div class="media-body text-truncate book-item-author" style="width:200px">
                    <span class="name mb-0 text-xs w-100 book-item-title">${book['author']}</span>
                </div>
            </td>
            <td>
                <div class="avatar-group book-item-price">
                    ${book['price']}
                </div>
            </td>
            <td>
                <div class="product-qty-status text-xs ${book['quantity'] < config['min_restock_level'] ? 'product-qty-status-shortage' : ''}  text-center py-1 cursor-pointer">
                    ${book['quantity'] >= config['min_restock_level'] ? "Đủ số lượng" : "Cần nhập thêm"} 
                </div>
            </td>
        </tr>`).join("");
    bookList.insertAdjacentHTML("beforeend", html);
}

const fetchBook = async function() {
    try {
        const res = await fetch(`${BOOK_API}${url.search}`)
        if(!res.ok) throw new Error("Cannot fetch books");
        return await res.json();
    } catch(err) {
        throw err;
    }
}
window.addEventListener("load", async function() {
    try {
        const res = await fetch(`${CONFIG_API}`);
        if(!res.ok) throw new Error("cannot fetch config");
        config = await res.json();
    } catch(err) {
        alert(err.message);
    }
})