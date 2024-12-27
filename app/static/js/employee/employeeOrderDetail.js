//---------------------------------------------CONSTANTS---------------------------------------------
const Color = {
    WARNING: "orange",
    ERROR: `var(--red)`,
    SUCCESS: "#6cbf6c"
}
//---------------------------------------------DOM ELEMENTS & STATES---------------------------------------------
const printInvoiceBtn = document.querySelector(".btn-invoice");
const modal = document.querySelector(".modal");
const overlay = modal.querySelector(".overlay");

//---------------------------------------------RENDER---------------------------------------------
const renderToast = function (text, background) {
    Toastify({
        text: text,
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: "top",
        position: "right",
        stopOnFocus: true,
        style: {
            background: background,
        }
    }).showToast();
}
//---------------------------------------------DOM UTILITY---------------------------------------------
const toggleModal = function() {
    console.log(overlay)
    modal.classList.toggle("d-flex");
    overlay.classList.toggle("d-flex");
}

//---------------------------------------------EVENTS---------------------------------------------
overlay.addEventListener("click", toggleModal);

printInvoiceBtn.addEventListener("click", toggleModal)

modal.addEventListener("click", function(e) {
    const pdfDownloadBtn = e.target.closest(".btn-download-pdf");
    if (!pdfDownloadBtn) return;

    const {jsPDF} = window.jspdf;

    renderToast("Đang tải xuống...", Color.WARNING);

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

        pdf.save(`invoice_${document.querySelector('[order-id]').getAttribute("order-id")}.pdf`);
        renderToast("Đã tải thành công !", Color.SUCCESS);
    });
});
