const printInvoiceBtn = document.querySelector(".btn-invoice");
const modal = document.querySelector(".modal");
const overlay = document.querySelector(".overlay");


const toggleModal = function() {
    modal.classList.toggle("d-flex");
    overlay.classList.toggle("d-flex");
}

printInvoiceBtn.addEventListener("click", function() {
    toggleModal();
    const html = `
        <div id="invoice" class="container mt-4">
            <div class="card">
                <div class="card-header text-center">
                    <img class="image-fluid w-25"
                         src="https://cdn0.fahasa.com/skin/frontend/ma_vanese/fahasa/images/fahasa-logo.png" alt="">
                </div>
                <div class="card-header invoice-header text-center">
                    <class
                    ="mb-0">Mã đơn: 79686 &nbsp; | &nbsp; Ngày đặt: 12/13/2022 &nbsp; | &nbsp; Hotline: 19008386
                    &nbsp; | &nbsp; Trạng thái: Đã hoàn thành &nbsp; | &nbsp; Loại đơn: Mua trực tiếp</p>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-12">
                            <h1 class="text-center pb-3">THÔNG TIN HÓA ĐƠN</h1>
                        </div>
        
                        <div class="col-md-6">
                            <p>
                                <strong>Tên:</strong> Phát đẹp trai số 1 OU<br>
                                <strong>Địa chỉ:</strong> 301 Hồ Hảo Hớn, P Cô Giang, Q1<br>
                                <strong>Thành phố:</strong> Hố chí minh <br>
                                <strong>Nước:</strong> Việt Nam <br>
                                <strong>Số điện thoại:</strong> +02 782 390 782 <br>
        
                            </p>
                        </div>
                        <div class="col-md-6 text-right">
                            <p>
                                <strong>Phương thức vận chuyển:</strong> Giao hàng <br>
                                <strong>Phương thức thanh toán:</strong> Thẻ
                            </p>
                        </div>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-bordered">
                            <thead>
                            <tr class="text-center">
                                <th>Barcode</th>
                                <th>Tên sách</th>
                                <th>Giá</th>
                                <th>Số lượng</th>
                                <th>Giảm giá</th>
                                <th>Tổng tiền</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr class="text-center">
                                <td>30566205</td>
                                <td>3D Cannon Camera</td>
                                <td>25.00</td>
                                <td>1</td>
                                <td>10.00</td>
                                <td>23.00</td>
                            </tr>
                            <tr class="text-center">
                                <td>30566206</td>
                                <td>Green Lemon</td>
                                <td>70.00</td>
                                <td>1</td>
                                <td>0.00</td>
                                <td>70.00</td>
                            </tr>
                            <tr class="text-right">
                                <td colspan="5"><strong>Tổng tiền:</strong></td>
                                <td class="text-center">$93.00</td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="row">
                        <div class="col-md-6">
                            <p>
                                <strong>Ghi chú:</strong> Lorem ipsum dolor sit amet consectetur adipisicing elit. Quos
                                aut provident aperiam expedita mollitia cumque rerum pariatur, reprehenderit ab eveniet
                                molestiae hic iure doloremque cum ullam fugit. Enim, assumenda incidunt.<br>
                            </p>
                        </div>
                        <div class="col-md-6 text-right">
                            <p>
                                <strong>Phí ship:</strong> 100.00<br>
                                <strong>Tổng tiền:</strong> 193.00<br>
                            </p>
                        </div>
                    </div>
                    <div class="row mt-3">
                        <div class="col-md-6">
                            <p>
                                <strong>Created By:</strong> Richard Joseph<br>
                                <strong>Email:</strong> info@example.com
                            </p>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="downloadPDF" class="btn text-white btn-print btn-download-pdf">Print</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>`;
});

overlay.addEventListener("click", function() {
    toggleModal();
});

modal.addEventListener("click", function(e) {
    const pdfDownloadBtn = e.target.closest(".btn-download-pdf");
    if (!pdfDownloadBtn) return;

    const {jsPDF} = window.jspdf;

    // Capture HTML content
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
        pdf.save("invoice.pdf");
    });
});

const orderItems = document.querySelectorAll(".order-item")
orderItems.forEach(orderItem => {
    const barcode = orderItem.querySelector(".order-item-barcode")?.textContent.trim();
    const title = orderItem.querySelector(".order-item-title")?.textContent.trim();
    const price = orderItem.querySelector(".order-item-price")?.textContent.trim();
    const discount = orderItem.querySelector(".order-item-discount")?.textContent.trim();
    const quantity = orderItem.querySelector(".order-item-quantity")?.textContent.trim();
    const subTotalAmount = orderItem.querySelector(".order-item-subtotal-amount")?.textContent.trim();
    const shippingFee = orderItem.querySelector(".order-shipping-fee")?.textContent.trim();
    const totalAmount = orderItem.querySelector(".order-total-amount")?.textContent.trim();
    console.log({
        barcode,
        title,
        price,
        discount,
        quantity,
        subTotalAmount,
        shippingFee,
        totalAmount
    });
});