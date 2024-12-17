const IMPORT_API = `/api/v1/book/import`;
const url = new URL(window.location);
const vndCurrencyFormat = new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
});

function extractCurrencyNumber(currencyString) {
    const numericValue = currencyString.replace(/[^\d,]/g, ''); // Keep digits and comma
    return parseFloat(numericValue.replace(',', '.')); // Convert to float, replace comma with dot
}

const dateFormatter = new Intl.DateTimeFormat('vi-VN', {
    weekday: 'short', // e.g., Thứ Sáu
    year: 'numeric',
    month: 'numeric', // e.g., Tháng 1
    day: 'numeric',
    // timeZoneName: 'short' // e.g., GMT
});

const timeFormatter = new Intl.DateTimeFormat('vi-VN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    // timeZoneName: 'short' // e.g., GMT
});

const modalBodyExport = document.querySelector(".modal-body-export")
const pagination = document.querySelector(".pagination");
const modal = document.querySelector(".modal");
const overlay = document.querySelector(".overlay");

const inputStartDate = document.querySelector(".input-start-date");
const inputEndDate = document.querySelector(".input-end-date");
const inputSearch = document.querySelector(".input-search");

const importList = document.querySelector(".import-list");

const resetAllBtn = document.querySelector(".btn-reset-all");
const searchBtn = document.querySelector(".btn-search");
const printBtn = document.querySelector(".btn-print-import-form");
let currentSearchParam = {};

const deleteCurrentParams = (params) => params.forEach(param => delete currentSearchParam[param]);
const addCurrentParams = (params) => params.forEach(param => currentSearchParam[param[0]] = param[1]);

const deleteUrlParams = (params) => params.forEach(param => url.searchParams.delete(param));
const addUrlParams = (params) => params.forEach(param => url.searchParams.set(param[0], param[1]));


const fetchImportForm = async function () {
    try {
        const param = '?' + Object.entries(currentSearchParam).map(pr => pr[0] + '=' + pr[1]).join("&");
        const res = await fetch(`${IMPORT_API}${param}`);
        if (!res.ok) throw new Error("Cannot fetch import form");
        const data = await res.json();
        return data['data'];
    } catch (err) {
        throw err;
    }
};

const fetchImportFormDetail = async function (importFormId) {
    try {
        const res = await fetch(`${IMPORT_API}/${importFormId}/detail`);
        if (!res.ok) throw new Error("Cannot fetch import form detail");
        const data = await res.json();
        return data['data'];
    } catch (err) {
        throw err;
    }
}

const resetAllState = function () {
    inputStartDate.value = '';
    inputEndDate.value = '';
    inputSearch.value = '';

    currentSearchParam = {};
    url.search = "";
    window.history.pushState({}, '', url);
}

const openModal = function () {
    overlay.classList.add("d-flex");
    modal.classList.add("d-flex");
}

const closeModal = function () {
    overlay.classList.remove("d-flex");
    modal.classList.remove("d-flex");
}

modalBodyExport.addEventListener("click", function (e) {
    const pdfDownloadBtn = e.target.closest(".btn-download-pdf");
    if (!pdfDownloadBtn) return;

    const {jsPDF} = window.jspdf;

    Toastify({
        text: "Đang tải xuống...",
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: "right", // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
            background: "orange",
        }
    }).showToast();

    html2canvas(document.querySelector("#invoice"), {
        useCORS: true,
        allowTaint: false,
        scale: 2 // Improves image quality
    }).then(canvas => {
        const imgData = canvas.toDataURL("image/png");
        const pdf = new jsPDF("p", "mm", "a4");

        // Add image to PDF
        const imgProps = pdf.getImageProperties(imgData);
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

        pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);

        pdf.save(`form_import_${document.querySelector('[form-import-id]').getAttribute("form-import-id")}.pdf`);
        Toastify({
            text: "Đã tải thành công !",
            duration: 3000,
            newWindow: true,
            close: true,
            gravity: "top", // `top` or `bottom`
            position: "right", // `left`, `center` or `right`
            stopOnFocus: true, // Prevents dismissing of toast on hover
            style: {
                background: "#6cbf6c",
            }
        }).showToast();
    });
})

resetAllBtn.addEventListener("click", async function () {
    resetAllState();
    try {
        const form = await fetchImportForm();
        renderImportItems(form['form_imports']);
        renderPagination(form['total_page'], form['current_page']);
    } catch (err) {
        alert(err.message);
    }
});

overlay.addEventListener("click", closeModal)

importList.addEventListener("click", async function (e) {
    const printBtn = e.target.closest(".btn-print-import-form");
    console.log(printBtn)
    if (!printBtn) return;
    try {
        const formImportId = e.target.closest(".import-item").getAttribute("id");
        const form = await fetchImportFormDetail(formImportId);
        openModal();
        renderImportForm(form);
    } catch (err) {
        alert(err.message);
    }
});

searchBtn.addEventListener("click", async function () {
    const formImportId = inputSearch.value;
    resetAllState();
    currentSearchParam['formImportId'] = formImportId;

    const form = await fetchImportForm();
    renderImportItems(form['form_imports']);
    renderPagination(form['total_page'], form['current_page']);
});

inputStartDate.addEventListener("change", async function () {
    const value = inputStartDate.value;

    deleteCurrentParams(["startDate", "page", "formImportId"])
    deleteUrlParams(["startDate", "page", "formImportId"]);
    inputSearch.value = '';

    if (value) {
        addCurrentParams([["startDate", value]]);
        addUrlParams([["startDate", value]]);
    }

    window.history.pushState({}, '', url);

    const form = await fetchImportForm();
    renderImportItems(form['form_imports']);
    renderPagination(form['total_page'], form['current_page']);
});


inputEndDate.addEventListener("change", async function () {
    const value = inputEndDate.value;
    deleteCurrentParams(["endDate", "page", "formImportId"])
    deleteUrlParams(["endDate", "page", "formImportId"]);
    inputSearch.value = '';
    if (value) {
        addCurrentParams([["endDate", value]]);
        addUrlParams([["endDate", value]]);
    }

    window.history.pushState({}, '', url);

    const form = await fetchImportForm();
    renderImportItems(form['form_imports']);
    renderPagination(form['total_page'], form['current_page']);
});

pagination.addEventListener("click", async function (e) {
    const item = e.target.closest(".page-item");
    if (!item || item.classList.contains("disabled") || item.classList.contains("active")) return;

    deleteUrlParams(["page"]);
    deleteCurrentParams(["page"]);

    addUrlParams([["page", item.getAttribute("page")]]);
    addCurrentParams([["page", item.getAttribute("page")]]);

    window.history.pushState({}, '', url);

    const form = await fetchImportForm();

    renderImportItems(form['form_imports']);
    renderPagination(form['total_page'], form['current_page']);
});

const renderPagination = function (total_page, current_page) {
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
};

const renderImportItems = function (formImportItems) {
    const html = formImportItems.map(formImport => `
        <tr class="import-item" id="${formImport['form_import_id']}">
            <th scope="row">
                <div class="media align-items-center">
                    <div class="media-body text-center">
                        <span class="name mb-0 text-sm text-center w-100">${formImport['form_import_id']}</span>
                    </div>
                </div>
            </th>
            <td scope="row">
                <div class="media align-items-center">
                    <div class="media-body text-left text-truncate book-item"
                         style="width:100px!important;">
                        <span class="order-item-name mb-0 text-sm text-center w-100">${formImport['employee']['name']}</span>
                    </div>
                </div>
            </td>
            <td>
                <div class="d-flex align-items-center w-100 justify-content-center">
                    <span class="completion mr-2">${dateFormatter.format(new Date(formImport['created_at']))}</span>
                </div>
            </td>
            <td class="text-right">
                <div class="">
                    <a class="btn btn-sm btn-icon-only text-light btn-print-import-form" href="#" role="button"
                       data-toggle=""
                       aria-haspopup="true" aria-expanded="false">
                        <i class="fa-solid fa-print"></i>
                    </a>
                </div>
            </td>
        </tr>`).join('');

    importList.innerHTML = '';
    importList.insertAdjacentHTML("beforeend", html);
};

const renderImportForm = function (form) {
    const html = `
    <div id="invoice" class="mt-4 w-100" form-import-id="${form['form_import_id']}">
        <div class="card">
            <div class="card-header text-center">
                <img class="image-fluid w-25"
                     src="https://cdn0.fahasa.com/skin/frontend/ma_vanese/fahasa/images/fahasa-logo.png" alt="">
            </div>
            <div class="card-header invoice-header text-center">
                <p class="mb-0 font-weight-600">Mã phiếu: ${form['form_import_id']} &nbsp; | &nbsp; Ngày nhập: ${dateFormatter.format(new Date(form['created_at']))} &nbsp; |
                    &nbsp; Hotline:
                    19008386 &nbsp;</p>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-12">
                        <h1 class="text-center pb-3 display-3 text-black">PHIẾU NHẬP SÁCH</h1>
                    </div>
                    <div class="col-md-6">
                        <p>
                            <strong class="font-weight-600">Tên nhân viên:</strong>${form['employee']['name']}<br>
                            <strong class="font-weight-600">Ngày giờ nhập:</strong> ${timeFormatter.format(new Date(form['created_at']))} ${dateFormatter.format(new Date(form['created_at']))}
                        </p>
                    </div>
                    <div class="col-md-6 text-right"></div>
                    <div class="table-responsive">
                        <table class="table table-bordered">
                            <thead>
                            <tr class="text-center">
                                <th>ID</th>
                                <th>Tên</th>
                                <th>Thể loại</th>
                                <th>Tác giả</th>
                                <th>Số lượng</th>
                            </tr>
                            </thead>
                            <tbody>
                            ${form['detail'].map(book => `
                            <tr class="text-center">
                                <td>${book['book_detail']['book_id']}</td>
                                <td class="wrap-text text-left">${book['book_detail']['title']}</td>
                                <td>${book['book_detail']['gerne']['name']}</td>
                                <td>${book['book_detail']['author']}</td>
                                <td>${book['quantity']}</td>
                            </tr>`).join('')}
                            <tr class="text-right">
                                <td colspan="4"><strong>Tổng số lượng:</strong></td>
                                <td class="text-center">${form['total_quantity']}</td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="col-6 pt-5">
                        <div class="row">
                            <div class="col-md-12">
                                <div class="d-flex flex-column align-items-center" style="padding-left: 2%">
                                    <strong class="pb-5">Người lập phiếu</strong>
                                    <div class="pt-5">${form['employee']['name']}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-6 pt-5">
                        <div class="row">
                            <div class="col-md-12 flex-end">
                                <p class="text-right">
                                    <button id="downloadPDF"
                                            class="btn text-right text-white btn-print btn-download-pdf">Print
                                    </button>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>`;
    modalBodyExport.innerHTML = '';
    modalBodyExport.insertAdjacentHTML("beforeend", html);
};