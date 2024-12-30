function filterMedicines() {
        const searchInput = document.getElementById('searchInput').value.toLowerCase(); // Lấy giá trị tìm kiếm
        const table = document.getElementById('medicines');
        const rows = table.getElementsByTagName('tr'); // Lấy tất cả các dòng trong bảng

        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const cells = row.getElementsByTagName('td');
            const medicineName = cells[0].textContent.toLowerCase(); // Lấy tên thuốc từ cột đầu tiên

            if (medicineName.includes(searchInput)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    }

function selectMedicine(name, unit) {
    const table = document.getElementById('medicineTable').getElementsByTagName('tbody')[0];
    const rowCount = table.rows.length;
    const row = table.insertRow();

    row.innerHTML = `
        <td>${rowCount + 1}</td>
        <td><input type="text" class="form-control" value="${name}" name="medicineName" required></td>
        <td><input type="text" class="form-control" placeholder="Nhập số lượng" name="quantity" required></td>
        <td><input type="text" class="form-control" value="${unit}" name="unit" required></td>
        <td><input type="text" class="form-control" placeholder="Nhập cách dùng" name="usage" required></td>
        <td class="text-center"><button type="button" class="btn btn-danger btn-sm" onclick="deleteRow(this)">Xóa</button></td>
    `;

    const modal = bootstrap.Modal.getInstance(document.getElementById('medicineModal'));
    modal.hide();
}

function deleteRow(button) {
    const row = button.parentElement.parentElement;
    const table = row.parentElement;
    table.removeChild(row);

    Array.from(table.rows).forEach((row, index) => {
        row.cells[0].textContent = index + 1;
    });
}

function viewPrescription(button) {

    const prescriptionsJson = button.getAttribute('data-prescriptions');
    const prescriptions = JSON.parse(prescriptionsJson);

    let content = `<ul>`;
    prescriptions.forEach(prescription => {
        content += `<li>${prescription.medicine_name}: ${prescription.quantity} ${prescription.unit} - ${prescription.guide}</li>`;
    });
    content += `</ul>`;

    document.getElementById('prescriptionContent').innerHTML = content;

    const modal = new bootstrap.Modal(document.getElementById('prescriptionModal'));
    modal.show();
}