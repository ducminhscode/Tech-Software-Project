from flask import render_template, request, redirect, session, url_for
from phongmachtu import app, login
from flask_login import login_user, logout_user, current_user, login_required
import dao
from phongmachtu.admin import *

from phongmachtu.dao import get_patient_id


@app.route('/')
def index():
    return render_template('index.html')


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

        user = dao.auth_account(username,password)

        if user:
            login_user(user)
            if user.type == "patient":
                return redirect('/')
            elif user.type == "doctor":
                return redirect('/')
            elif user.type == 'nurse':
                return redirect('/')
            elif user.type == "administrator":
                return redirect('/')
            else:
                return redirect('/cashier/cash')

        else:
            err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return render_template('login.html', err_msg=err_msg)


# =================================PATIENT============================================
@app.route('/patient/booking', methods=['GET', 'POST'])
def booking():
    err_msg = None

    if request.method == 'POST':
        selected_time = request.form.get('time')
        selected_date = request.form.get('date')

        if not selected_time or not selected_date:
            err_msg = "Vui lòng chọn đầy đủ buổi khám và ngày khám."
        else:
            try:
                dao.save_booking(selected_time, selected_date)
                return redirect('/patient/booking')
            except Exception as e:
                err_msg = f"Có lỗi xảy ra: {e}"

    time = dao.get_all_period()
    return render_template('patient/booking.html', time=time, err_msg=err_msg)


# @app.route('/register-detail', methods=['get', 'post'])
# def register_detail():
#     err_msg = None
#     account = Account.id
#     if request.method.__eq__('POST'):
#         if account.type == "patient":
#             address = request.form.get("address")
#             day_of_birth = request.form.get("day_of_birth")
#             phone =  request.form.get("phone")
#             dao.add_patient(address=address, day_of_birth=day_of_birth, phone=phone)
#             return redirect('/login')
#         else:
#             _license = request.form.get("license")
#             dao.add_doctor_cashier(_license=_license)
#             return redirect('/login')
#
#     return render_template('register-detail.html', err_msg=err_msg)


# =================================REGISTER============================================
@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password.__eq__(confirm):
            username = request.form.get("username")
            name = request.form.get("name")

            _type = request.form.get("type")

            dao.add_account(name=name, username=username, password=password, type=_type)
            return redirect('/login')
        else:
            err_msg = "Mật khẩu không khớp!"

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
        doctor_id = current_user.id  # Lấy ID của người dùng đang đăng nhập
        patient_name= request.args.get('name')
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
@app.route('/nurse/confirm-registration')
def confirm_registration():
    return render_template('/nurse/confirm-registration.html')


@app.route('/nurse/regis-patient')
def regis_patient():
    return render_template('/nurse/regis-patient.html')



@app.route('/nurse/patient-list')
def patient_list_nurse():
    return render_template('/nurse/patient-list.html')


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