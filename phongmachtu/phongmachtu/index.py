from flask import render_template, request, redirect, session, url_for
from phongmachtu import app, login
from flask_login import login_user, logout_user, current_user, login_required
import dao
from phongmachtu.admin import *


@app.route('/')
def index():
    return render_template('index.html')

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


@app.route('/booking')
def booking_self():
    time = dao.get_all_period()
    return render_template('booking.html', time=time)


@app.route('/cashier/receipt-list')
def receipt_list():
    return render_template('cashier/receipt-list.html')


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
            return redirect('login')
        else:
            err_msg = "Mật khẩu không khớp!"

    return render_template('register.html', err_msg=err_msg)


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


@app.route('/cashier/cash')
def cashing():
    return render_template('cashier/cash.html')


@app.route('/doctor/examination-form')
def examination_form():
    return render_template('/doctor/examination-form.html')


@app.route('/doctor/patient-list')
def patinent_list():
    return render_template('/doctor/patient-list.html')


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')


@login.user_loader
def load_account(user_id):
    return dao.get_account_by_id(user_id)


if __name__ == "__main__":
    app.run(debug=True)