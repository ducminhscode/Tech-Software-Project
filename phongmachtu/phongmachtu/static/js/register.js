function checkField(inputId, value) {
    fetch('/check_account', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ [inputId]: value })
    })
    .then(response => response.json())
    .then(data => {
        const feedback = document.querySelector(`#${inputId}-feedback`);
        const input = document.getElementById(inputId);

        if (data.status === 'error') {
            input.classList.add('is-invalid');
            feedback.innerHTML = data.messages.join('<br>');
            feedback.style.display = 'block';
            isFormValid = false;
        } else {
            input.classList.remove('is-invalid');
            feedback.style.display = 'none';
            isFormValid = true;
        }
    })
    .catch(error => console.error('Error:', error));
}

function checkPasswords() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm').value;

    const feedback = document.getElementById('confirm-feedback');
    const confirmInput = document.getElementById('confirm');

    if (password !== confirmPassword) {
        confirmInput.classList.add('is-invalid');
        feedback.style.display = 'block';
        isFormValid = false;
    } else {
        confirmInput.classList.remove('is-invalid');
        feedback.style.display = 'none';
        isFormValid = true;
    }
}