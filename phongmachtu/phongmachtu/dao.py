import json
import hashlib
from models import *
from phongmachtu import db

def add_account(name, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = Patient(name=name, username=username, password=password)
    db.session.add(u)
    db.session.commit()


def auth_account(username, password):

    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return Account.query.filter(Account.username.__eq__(username),
                             Account.password.__eq__(password)).first()


def get_all_period():
    # Truy vấn tất cả các giá trị period và id từ bảng Time
    periods = Time.query.with_entities(Time.id, Time.period).all()

    # Trả về danh sách các tuple chứa (id, period)
    return periods


def get_account_by_id(user_id):
    return Account.query.get(user_id)



