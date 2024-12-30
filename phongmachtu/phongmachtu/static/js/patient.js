function checkDateAndTime(date, time) {
    const feedback_date = document.getElementById('feedback-date');
    const feedback_time = document.getElementById('feedback-time');
    const currentDate = new Date();
    const currentHour = currentDate.getHours();
    const today = currentDate.toISOString().split('T')[0];

    feedback_date.style.display = 'none';
    feedback_time.style.display = 'none';
    isFormValid = true;

    if (date < today) {
        feedback_date.innerText = "Chọn ngày hợp lệ";
        feedback_date.style.display = 'block';
        isFormValid = false;
        return;
    }

    if (date === today) {
        if (time === '1' && currentHour > 11) {
            feedback_time.innerText = "Không thể chọn buổi sáng sau 11 giờ.";
            feedback_time.style.display = 'block';
            isFormValid = false;
        } else if (time === '2' && currentHour > 17) {
            feedback_time.innerText = "Không thể chọn buổi chiều sau 17 giờ.";
            feedback_time.style.display = 'block';
            isFormValid = false;
        } else if (time === '3' && currentHour > 22) {
            feedback_time.innerText = "Không thể chọn buổi tối sau 22 giờ.";
            feedback_time.style.display = 'block';
            isFormValid = false;
        }
    }

    if (!date) {
        feedback_date.innerText = "Vui lòng chọn ngày khám.";
        feedback_date.style.display = 'block';
        isFormValid = false;
    }
    if (!time) {
        feedback_time.innerText = "Vui lòng chọn buổi khám.";
        feedback_time.style.display = 'block';
        isFormValid = false;
    }
}