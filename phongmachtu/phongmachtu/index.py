from flask import render_template, request, redirect, session, url_for
from phongmachtu import app, login
from flask_login import login_user, logout_user, current_user, login_required
import dao
from phongmachtu.admin import *
from phongmachtu.dao import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/introduce')
def introduce():
    return render_template('introduce.html')


@app.route('/service')
def service():
    return render_template('service.html')


# =================================LOGIN============================================
@app.route('/login-admin', methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_account(username=username, password=password, type='administrator')
    if user:
        login_user(user)
        if current_user.type == 'administrator':
            return redirect('/admin')
    return redirect('/admin')


@app.route('/login', methods=['get', 'post'])
def login_my_user():
    if current_user.is_authenticated:
        return redirect("/")

    err_msg = None
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_account(username, password)

        if user:
            login_user(user)
            if user.type == "patient":
                return redirect('/')
            elif user.type == "doctor":
                return redirect('/')
            elif user.type == "nurse":
                return redirect('/')
            elif user.type == "cashier":
                return redirect('/cashier/cash')
            else:
                err_msg = "Tài khoản hoặc mật khẩu không đúng!"
                logout_my_user()

        else:
            err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return render_template('login.html', err_msg=err_msg)


# =================================PATIENT============================================
@app.route('/patient/booking', methods=['GET', 'POST'])
def booking():
    err_msg = None
    if request.method.__eq__('POST'):
        selected_time = request.form.get('time')
        selected_date = request.form.get('date')
        symptom = request.form.get('symptom')

        patient_id = current_user.id

        if not selected_time or not selected_date or not symptom:
            err_msg = "Vui lòng chọn đầy đủ thông tin."
        else:
            dao.save_booking(selected_date, symptom, patient_id, selected_time)
            err_msg = "Đăng kí thành công."

    time = dao.get_all_period()
    return render_template('patient/booking.html', time=time, err_msg=err_msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if not password.__eq__(confirm):
            err_msg = "Mật khẩu không khớp!"
            return render_template('register.html', err_msg=err_msg)
        else:
            username = request.form.get('username')
            name = request.form.get('name')
            address = request.form.get('address')
            day_of_birth = request.form.get('day_of_birth')
            gender = request.form.get('gender')
            phone = request.form.get('phone')
            dao.add_patient(name=name, username=username, password=password, address=address, day_of_birth=day_of_birth,
                            gender=gender, phone=phone)
            return redirect('/login')
    return render_template('register.html', err_msg=err_msg)


# =================================CASHIER============================================
@app.route('/cashier/receipt-list')
def receipt_list():
    return render_template('cashier/receipt-list.html')


@app.route('/cashier/cash')
def cashing():
    return render_template('cashier/cash.html')


# =================================DOCTOR============================================
@app.route('/doctor/examination-form', methods=['get', 'post'])
@login_required  # Chỉ cho phép người dùng đã đăng nhập truy cập
def examination_form():
    if request.method == 'POST':
        disease = request.args.get('disease')
        description = request.args.get('description')
        doctor_id = current_user.id
        patient_name = request.args.get('name')
        patient_id = get_patient_id(patient_name)

        # Thêm phiếu khám bệnh vào cơ sở dữ liệu
        dao.add_examination_form(disease=disease, description=description, doctor_id=doctor_id, patient_id=patient_id)
        return redirect('/doctor/patient-list')

    kw = request.args.get('keyword')
    patient = dao.get_patient_id(kw)

    return render_template('doctor/examination-form.html', patient=patient)


@app.route('/doctor/patient-list')
def patient_list_doctor():
    list_patient = dao.list_examination_by_doctor(Doctor.id)

    return render_template('nurse/patient-list.html', patients=list_patient)


# =================================NURSE============================================
@app.route('/nurse/check-phone', methods=['GET', 'POST'])
def check_phone():
    msg = None
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        patient = dao.check_phone(phone_number)

        if patient:
            msg = "Số điện thoại tồn tại."
            return redirect(url_for('patient_booking', patient_id=patient.id, patient_name=patient.name, msg=msg))
        else:
            msg = "Số điện thoại không tồn tại, đăng kí bệnh nhân mới."
            return redirect(url_for('regis_patient', msg = msg))

    return render_template('/nurse/check-phone.html')


@app.route('/nurse/patient-booking', methods=['GET', 'POST'])
def patient_booking():
    patient_id = request.args.get('patient_id')
    patient_name = request.args.get('patient_name')
    msg = request.args.get('msg')
    if msg is None:
        msg = ""

    err_msg = None
    if request.method.__eq__('POST'):
        selected_time = request.form.get('time')
        selected_date = request.form.get('date')
        symptom = request.form.get('symptom')

        if not selected_time or not selected_date or not symptom:
            err_msg = "Vui lòng chọn đầy đủ thông tin."
        else:
            dao.save_booking(selected_date, symptom, patient_id, selected_time)
            err_msg = "Đăng kí thành công."
            return redirect('/nurse/patient-list')

    time = dao.get_all_period()
    return render_template('/nurse/patient-booking.html', msg=msg, time=time, err_msg=err_msg,patient_name=patient_name)


@app.route('/nurse/regis-patient', methods=['GET', 'POST'])
def regis_patient():
    msg = request.args.get('msg')

    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        day_of_birth = request.form.get('day_of_birth')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        patient = dao.add_patient_by_nurse(name=name, address=address, day_of_birth=day_of_birth, gender=gender, phone=phone)
        return redirect(url_for('patient_booking', patient_id=patient.id, patient_name=patient.name))

    return render_template('/nurse/regis-patient.html', msg = msg)


@app.route('/nurse/confirm-registration', methods=['GET', 'POST'])
def confirm_registration():
    registrations = load_registration_form()

    reg_id = request.form.get('registration_id')
    if reg_id:
        if dao.confirm_registration(reg_id):
            return redirect('/nurse/patient-list')

    return render_template('/nurse/confirm-registration.html', reg = registrations)


@app.route('/nurse/patient-list', methods=['GET', 'POST'])
def patient_list_nurse():
    date_str = request.form.get('selectedDate')
    if date_str:
        date_str = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date_str = datetime.now().date()

    list_patient = registration_form_date(date_str)
    return render_template('/nurse/patient-list.html', reg=list_patient)


# =================================LOGOUT============================================
@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')


@login.user_loader
def load_account(user_id):
    return dao.get_account_by_id(user_id)


if __name__ == "__main__":
    app.run(debug=True)
