const bookList = document.querySelector(".book-list");
const modal = document.querySelector(".modal");
const modalBody = document.querySelector(".modal-body");
const overlay = document.querySelector(".overlay");
const addBookBtn = document.querySelector(".add-book-btn");
const allCheckBox = document.querySelector(".all-check-box");

let currentOrderItemsState = {};
let checkedBookState;

const openModal = function() {
    modal.classList.add("d-flex");
    overlay.classList.add("d-flex");
}

const closeModal = function() {
    modal.classList.remove("d-flex");
    overlay.classList.remove("d-flex");
}

overlay.addEventListener("click", closeModal);
addBookBtn.addEventListener("click", openModal);

