import datetime
import os
from operator import or_
from wsgiref.util import request_uri

from dotenv import load_dotenv
from flask import render_template, request, redirect, session, url_for, jsonify
from wtforms.validators import email

from phongmachtu import app, login
from flask_login import login_user, logout_user, current_user, login_required
import dao
from phongmachtu.admin import *
from phongmachtu.dao import *
import cloudinary.uploader
import hashlib


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
    success_msg = None
    if request.method.__eq__('POST'):
        dao.update_info(day_of_birth=request.form.get('day_of_birth'),
                        phone=request.form.get('phone'),
                        address=request.form.get('address'),
                        avatar=request.files.get('avatar'),
                        gender=request.form.get('gender'),
                        patient_id=current_user.id)
        success_msg = "Thay đổi thông tin cá nhân thành công"
    return render_template('info.html', success_msg=success_msg)


@app.route('/change-password', methods=['get', 'post'])
def change_password():
    err_msg = None
    success_msg = None
    if request.method.__eq__('POST'):
        hashed_old_password = request.form.get('old_password')
        old_password = str(hashlib.md5(hashed_old_password.encode('utf-8')).hexdigest())
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if (current_user.password != old_password) or new_password != confirm_password:
            err_msg = "Thay đổi mật khẩu thất bại"
        else:
            update_password(current_user.id, new_password)
            success_msg = "Thay đổi mật khẩu thành công"

    return render_template('change-password.html', success_msg=success_msg, err_msg=err_msg)


# =================================PATIENT============================================
@app.route('/patient/booking', methods=['GET', 'POST'])
def booking():
    err_msg = None
    success_msg = None
    if request.method.__eq__('POST'):
        selected_time = request.form.get('time')
        selected_date = request.form.get('date')
        symptom = request.form.get('symptom')
        patient_id = current_user.id

        if dao.check_booking(patient_id, selected_date):
            err_msg = "Bạn đã đăng kí lịch khám vào ngày này rồi"
        else:
            if dao.save_booking(selected_date, symptom, patient_id, selected_time):
                success_msg = "Đăng kí thành công."
            else:
                err_msg = "Số lượng khám trong ngày đã giới hạn"


    time = dao.get_all_period()
    return render_template('patient/booking.html', time=time, err_msg=err_msg, success_msg=success_msg)


@app.route('/patient/history')
def history_patient():
    appoint = dao.get_appointment(current_user.id)

    return render_template('patient/history.html', appoint=appoint)


@app.route('/patient/history_prescription_details/<int:appointment_id>', methods=['GET'])
def history_prescription_details(appointment_id):
    result = dao.get_examination_form(appointment_id)
    prescription_data = dao.get_prescription(appointment_id)
    if result:
        return render_template(
            'patient/history_prescription_details.html',
            result=result,
            prescription_data=prescription_data
        )
    else:
        return redirect(url_for('history_patient'))


@app.route('/patient/invoice_details/<int:appointment_id>', methods=['GET'])
def invoice_details(appointment_id):
    receipt = dao.show_receipt_by_appointment_id(appointment_id)
    if receipt:
        return render_template('patient/invoice_details.html', receipt=receipt)
    else:
        return redirect(url_for('history_patient'))


@app.route('/patient/medical-schedule')
def medical_schedule():
    appoint = dao.get_appointment(current_user.id)
    return render_template('patient/medical-schedule.html', appoint=appoint)


@app.route('/register', methods=['GET', 'POST'])
def register():
    err_msg = None
    avatar_path = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        username = request.form.get('username')
        name = request.form.get('name')
        address = request.form.get('address')
        day_of_birth = request.form.get('day_of_birth')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        avatar = request.files.get('avatar')
        email = request.form.get('email')
        if avatar:
            my_folder = os.getenv('my_folder')
            response = cloudinary.uploader.upload(avatar, folder=my_folder)
            avatar_path = response['secure_url']

        error = dao.check_account(username, phone, email)
        if error:
            err_msg = error[0]
        else:
            dao.add_patient(name=name, username=username, password=password, avatar=avatar_path, address=address,
                            day_of_birth=day_of_birth,
                            gender=gender, phone=phone, email=email)
            return redirect('/login')

    return render_template('register.html', err_msg=err_msg)


@app.route('/check_account', methods=['POST'], endpoint='check_account_route')
def check_account():
    data = request.get_json()  # Nhận dữ liệu từ AJAX
    username = data.get('username')
    phone = data.get('phone')
    email = data.get('email')

    errors = dao.check_account(username, phone, email)

    if errors:
        return jsonify({'status': 'error', 'messages': errors})
    else:
        return jsonify({'status': 'success'})


# =================================CASHIER============================================
@app.route('/cashier/receipt-list', methods=['GET', 'POST'])
def receipt_list():
    msg = None
    receipts = []

    if request.method == 'POST':
        kw = request.form.get('patientPhone')
        if kw:
            patient = dao.check_phone(kw)
            if patient:
                receipts = dao.show_receipt(patient.id)
            else:
                msg = "Không tìm thấy bệnh nhân với số điện thoại này."
        else:
            msg = "Vui lòng nhập số điện thoại."

    return render_template('cashier/receipt-list.html', receipts=receipts, err_msg=msg)


@app.route('/cashier/check-receipt', methods=['GET', 'POST'])
def check_receipt():
    patient_id = None
    receipt = None
    err_msg = None
    if request.method == 'POST':
        patient_id = request.form.get('invoiceCode')

        if not patient_id:
            err_msg = "Vui lòng nhập bệnh nhân."
            return render_template('cashier/check-receipt.html', err_msg=err_msg)

        receipt = dao.check_receipt(patient_id)
        if receipt:
            return redirect(url_for('cashing', receipt_id=receipt.id))
        else:
            err_msg = "Không tìm thấy hóa đơn cần thanh toán"

    return render_template('cashier/check-receipt.html', err_msg=err_msg)


@app.route('/cashier/cashing', methods=['GET', 'POST'])
def cashing():
    receipt_id = request.args.get('receipt_id')
    receipt = dao.show_receipt_by_receipt_id(receipt_id)

    if receipt is None:
        return render_template('cashier/cashing.html', error_message="Không tìm thấy hóa đơn cho bệnh nhân này.")

    if request.method == 'POST':
        dao.update_receipt(receipt.id, current_user.id)
        return render_template('cashier/cashing.html', receipt=receipt, success_message="Hóa đơn đã được thanh toán!")

    return render_template('cashier/cashing.html', receipt=receipt)


# =================================DOCTOR============================================
@app.route('/doctor/examination-form', methods=['get', 'post'])
@login_required
def examination_form():
    today_date = datetime.today().date()
    registrations = dao.load_registration_form_by_day(today_date)

    return render_template('doctor/examination-form.html', reg=registrations)


@app.route('/doctor/examination/<int:registration_id>', methods=['GET', 'POST'])
@login_required
def examination_detail(registration_id):
    registration = dao.get_registration_by_id(registration_id)
    medicines = dao.load_medicine()

    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        doctor_id = current_user.id
        examination_id = request.form.get('examination_id')

        disease = request.form.get('disease')
        medicine_names = request.form.getlist('medicineName')
        quantities = request.form.getlist('quantity')
        units = request.form.getlist('unit')
        usages = request.form.getlist('usage')

        prescription_id = dao.add_examination_form(examination_id, doctor_id, patient_id, disease,
                                                   medicine_names, quantities, units, usages)
        dao.change_isKham(patient_id)
        dao.set_receipt(prescription_id, patient_id, medicine_names, quantities)

        return redirect('/doctor/examination-form')

    return render_template('doctor/examination-details.html', registration=registration, medicines=medicines)


@app.route('/doctor/history-examination', methods=['get', 'post'])
def history_examination():
    patient_history = None

    if request.method.__eq__('POST'):
        patient_id = request.form.get('patient_id')
        if patient_id:
            patient_history = dao.get_information_examination(patient_id)

    return render_template('/doctor/history-examination.html', patient_history=patient_history)


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
            return redirect(url_for('regis_patient', msg=msg))

    return render_template('/nurse/check-phone.html')


@app.route('/nurse/patient-booking', methods=['GET', 'POST'])
def patient_booking():
    patient_id = request.args.get('patient_id')
    patient_name = request.args.get('patient_name')
    msg = request.args.get('msg')
    if msg is None:
        msg = ""

    err_msg = None
    success_msg = None
    if request.method.__eq__('POST'):
        selected_time = request.form.get('time')
        selected_date = request.form.get('date')
        symptom = request.form.get('symptom')

        if dao.check_booking(patient_id, selected_date):
            err_msg = "Bạn đã đăng kí lịch khám vào ngày này rồi"
        else:
            u_id = dao.save_booking(selected_date, symptom, patient_id, selected_time)
            if u_id:
                if dao.confirm_registration(u_id, selected_date, selected_time):
                    success_msg = "Đăng kí thành công."
            else:
                err_msg = "Số lượng khám trong ngày đã giới hạn"

    time = dao.get_all_period()
    return render_template('/nurse/patient-booking.html', msg=msg, time=time, err_msg=err_msg,
                           patient_name=patient_name, success_msg=success_msg)


@app.route('/nurse/regis-patient', methods=['GET', 'POST'])
def regis_patient():
    msg = request.args.get('msg')

    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        day_of_birth = request.form.get('day_of_birth')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        email = request.form.get('email')
        patient = dao.add_patient_by_nurse(name=name, address=address, day_of_birth=day_of_birth, gender=gender,
                                           phone=phone, email=email)
        return redirect(url_for('patient_booking', patient_id=patient.id, patient_name=patient.name))

    return render_template('/nurse/regis-patient.html', msg=msg)


@app.route('/nurse/confirm-registration', methods=['GET', 'POST'])
def confirm_registration():
    registrations = load_registration_form()
    date = request.form.get('date')
    reg_id = request.form.get('registration_id')
    selected_time = request.form.get('time')

    if reg_id:
        if dao.confirm_registration(reg_id, date, selected_time):
            return redirect('/nurse/confirm-registration')

    return render_template('/nurse/confirm-registration.html', reg=registrations)


@app.route('/nurse/confirm-all-registrations', methods=['GET', 'POST'])
def confirm_all_registrations():
    registrations = load_registration_form()

    for r in registrations:
        dao.confirm_registration(r.id, r.booked_date, r.time.id)

    return redirect('/nurse/confirm-registration')


@app.route('/nurse/cancel-registration', methods=['GET', 'POST'])
def cancel_registration():
    registrations = load_registration_form()

    reg_id = request.form.get('registration_id')
    if reg_id:
        if dao.cancel_registration(reg_id):
            return redirect('/nurse/cancel-registration')

    return render_template('/nurse/confirm-registration.html', reg=registrations)


@app.route('/nurse/delete-registration/<int:registration_id>', methods=['POST'])
def delete_registration(registration_id):
    result = dao.cancel_registration(registration_id)

    if result:
        return redirect('/nurse/patient-list')
    else:
        return "Có lỗi xảy ra khi hủy lịch khám!", 400


@app.route('/nurse/patient-list', methods=['GET', 'POST'])
def patient_list_nurse():
    date_str = request.form.get('selectedDate')
    if date_str:
        date_str = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date_str = None

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


def configure():
    load_dotenv()


if __name__ == "__main__":
    configure()
    app.run(debug=True)
