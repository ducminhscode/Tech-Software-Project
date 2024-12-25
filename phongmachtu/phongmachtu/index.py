import datetime

from flask import render_template, request, redirect, session, url_for
from phongmachtu import app, login
from flask_login import login_user, logout_user, current_user, login_required
import dao
from phongmachtu.admin import *
from phongmachtu.dao import *
import cloudinary.uploader


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
                return redirect('/')
            else:
                err_msg = "Tài khoản hoặc mật khẩu không đúng!"
                logout_my_user()

        else:
            err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return render_template('login.html', err_msg=err_msg)


@app.route('/info', methods=['get', 'post'])
def update():
    err_msg = ""

    if request.method.__eq__('POST'):
        try:
            dao.update_info(day_of_birth=request.form.get('day_of_birth'),
                            phone=request.form.get('phone'),
                            address=request.form.get('address'),
                            avatar=request.files.get('avatar'),
                            gender=request.form.get('gender'),
                            patient_id=current_user.id)
        except:
            err_msg = 'Hệ thống đang bận, vui lòng thử lại sau!'
        else:
            err_msg = "Cập nhật thành công"
        return redirect('/info')
    return render_template('info.html', err_msg=err_msg)


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
    avatar_path = None
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
            avatar = request.files.get('avatar')
            if avatar:
                my_folder = "PhongMachTu"
                response = cloudinary.uploader.upload(avatar, folder=my_folder)
                avatar_path = response['secure_url']
            dao.add_patient(name=name, username=username, password=password, avatar=avatar_path, address=address, day_of_birth=day_of_birth,
                            gender=gender, phone=phone)
            return redirect('/login')
    return render_template('register.html', err_msg=err_msg)


# =================================CASHIER============================================
@app.route('/cashier/receipt-list', methods=['GET', 'POST'])
def receipt_list():
    msg =None
    kw = request.form.get('patientPhone')
    patient = dao.check_phone(kw)
    if patient:
        receipts = dao.load_receipt(patient.id)
    else:
        receipts = []

    return render_template('cashier/receipt-list.html', receipts=receipts, err_msg=msg)


@app.route('/cashier/cash', methods=['GET', 'POST'])
def cashing():
    patient_code = None
    receipt = None
    if request.method == 'POST':
        patient_code = request.form.get('invoiceCode')
        receipt = dao.get_receipt_by_id_and_time(patient_code)
        if receipt:
            return render_template('cashier/cash.html', receipt = receipt)

    return render_template('cashier/cash.html', receipt = receipt)

# =================================DOCTOR============================================
@app.route('/doctor/examination-form', methods=['get', 'post'])
@login_required
def examination_form():
    today_date = datetime.today().date()

    registrations = dao.load_registration_form_by_day(today_date)
    medicines = dao.load_medicine()

    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        doctor_id = current_user.id
        disease = request.form.get('disease')

        medicine_names = request.form.getlist('medicineName')
        quantities = request.form.getlist('quantity')
        units = request.form.getlist('unit')
        usages = request.form.getlist('usage')

        prescription_id = dao.add_examination_form(doctor_id, patient_id, disease, medicine_names, quantities, units, usages)
        dao.change_isKham(patient_id)
        dao.set_receipt(prescription_id, patient_id,medicine_names, quantities)

    return render_template('doctor/examination-form.html', reg = registrations, medicines = medicines)

@app.route('/doctor/history-examination', methods=['get', 'post'])
def history_examination():
    patient_history = None

    if request.method.__eq__('POST'):
        patient_id = request.form.get('patient_id')
        if patient_id:
            patient_history = dao.get_information_examination(patient_id)

    return render_template('/doctor/history-examination.html', patient_history = patient_history)




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
