from flask import render_template, request, redirect, session, url_for
from phongmachtu import app, login
from flask_login import login_user, logout_user, current_user, login_required
import dao
from phongmachtu.admin import *


@app.route('/')
def index():
    return render_template('index.html')


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
                return redirect('/cash')

        else:
            err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return render_template('login.html', err_msg=err_msg)


@app.route('/booking')
def booking_self():
    time = dao.get_all_period()
    return render_template('booking.html', time=time)


@app.route('/receipt-list')
def receipt_list():
    return render_template('receipt-list.html')


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password.__eq__(confirm):
            username = request.form.get("username")
            name = request.form.get("name")


            dao.add_account(name=name, username=username, password=password)
            return redirect('/login')
        else:
            err_msg = "Mật khẩu không khớp!"

    return render_template('register.html', err_msg=err_msg)


@app.route('/cash')
def cashing():
    return render_template('cash.html')


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')


@login.user_loader
def load_account(user_id):
    return dao.get_account_by_id(user_id)


if __name__ == "__main__":
    app.run(debug=True)