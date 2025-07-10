function generatePDF() {
    const element = document.getElementById("report-content");
    if (!element) {
        alert("Element with id 'report-content' not found.");
        return;
    }

    const opt = {
        margin: 0.5,
        filename: 'Medical_Report.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
    };

    html2pdf().set(opt).from(element).save();
}
