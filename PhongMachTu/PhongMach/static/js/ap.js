function addBook() {
    let desc = document.getElementById('descId');
    let date = document.getElementById('dateId');
    let selectElement = document.getElementById('timeId');
    let timeId = selectElement.value;
    if (desc !== null) {
        fetch('/api/booking-form', {
            method: 'post',
            body: JSON.stringify({
                'date': date.value,
                'desc': desc.value,
                'time_id': timeId
            }),
            headers: {
                'Content-Type': "application/json"
            }
        }).then(function (res) {
            return res.json();

        }).then(function (data) {
            if (data.status == 201) {
                alert('Đặt lịch hành công')
            } else if (data.status == 404) {
                alert('Đặt lịch thất bại')
            }
        })
    }
}


function lenlich(id) {
    checkPatientCount();
    fetch('/len-ds', {
        method: "post",
        body: JSON.stringify({
            "id": id,
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(function (res) {
        return res.json();

    }).then(function (data) {
        window.location.reload();
        alert('Đã thêm thành công bệnh nhân!');
    })
}


function lenphieukham(id) {
    fetch('/len-pk', {
        method: "post",
        body: JSON.stringify({
            "id": id,
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(function (res) {
        return res.json();

    }).then(function (data){
        window.location.href = "/phieukham" ;
    });
}


function checkPatientCount() {
    fetch('/api/check-patient-count')
        .then(response => response.json())
        .then(data => {
            if (data.patients_today >= 40) {
                // alert('Đã đủ 40 bệnh nhân, không thể đăng ký thêm!');
                document.getElementById('message-container').innerText = 'Đã đủ 40 bệnh nhân, không thể đăng ký thêm!';
                var buttons = document.querySelectorAll('button.book-btn');
                buttons.forEach(button => {
                    button.disabled = true;
                });
                var messageContainer = document.getElementById('message-container');
                messageContainer.innerText = message;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

window.onload = function () {
    checkPatientCount();
};


function addReceipt() {
    let examines_price = document.getElementById('examinespriceId')
    let total = document.getElementById('totalId')
    let patient_id = document.getElementById('patientId')
    if (examines_price !== null) {
        fetch('/api/receipt-form', {
            method: 'post',
            body: JSON.stringify({
                'examines_price': examines_price.value,
                'total': total.value,
                'patient_id': patient_id.value
            }),
            headers: {
                'Content-Type': "application/json"
            }
        }).then(function (res) {
            return res.json();

        }).then(function (data) {
            if (data.status == 201) {
                alert('Thanh toán thành công')
            } else if (data.status == 404) {
                alert('Thanh toán thất bại')
            }
        })
    }
}
