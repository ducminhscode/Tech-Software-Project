import json
import hashlib
from models import *
from phongmachtu import db
from sqlalchemy import extract, func

def add_account(name, username, password, type):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = Account(name=name, username=username, password=password,type=type)
    db.session.add(u)
    db.session.commit()


def add_patient(address, day_of_birth, gender, phone):
    u = Patient(address=address, day_of_birth=day_of_birth, gender=gender, phone=phone)
    db.session.add(u)
    db.session.commit()


def add_doctor(license):
    u = Doctor(license=license)
    db.session.add(u)
    db.session.commit()


def add_cashier(license):
    u = Cashier(license=license)
    db.session.add(u)
    db.session.commit()


def auth_account(username, password):

    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return Account.query.filter(Account.username.__eq__(username),
                             Account.password.__eq__(password)).first()



def get_user_type(username, password):
    account = Account.query.filter_by(username=username).first()

    if account and password:
        if account.type == 'patient':
            return 'patient'
        return account.type
    return None


def get_all_period():
    # Truy vấn tất cả các giá trị period và id từ bảng Time
    periods = Times.query.with_entities(Times.id, Times.period).all()

    # Trả về danh sách các tuple chứa (id, period)
    return periods


def get_account_by_id(user_id):
    return Account.query.get(user_id)


def stats_revenue(month):
    with app.app_context():
        query = db.session.query(
            extract('month', Receipt.created_date).label('Tháng'),
            func.sum(Receipt.total_price).label('Doanh thu')
        ).group_by(extract('month', Receipt.created_date))

        results = query.all()

        return results


def stats_frequency(month):
    with app.app_context():
        query = db.session.query(
            extract('month', ExaminationForm.datetime).label('Tháng'),
            (func.count(ExaminationForm.id) / 40*100).label('Tần suất khám')
        ).group_by(extract('month', ExaminationForm.datetime))

        results = query.all()

        return results


def stats_medicine(kw=None, from_date=None, to_date=None):
    query = db.session.query(Medicine.id, Medicine.name, Medicine.unit,
                             func.sum(Prescription.quantity)) \
        .join(Medicine, Medicine.id.__eq__(Prescription.medicine_id), isouter=True)

    if kw:
        query = query.filter(Medicine.name.contains(kw))

    if from_date:
        query = query.filter(ExaminationForm.datetime.__ge__(from_date))

    if to_date:
        query = query.filter(ExaminationForm.datetime.__le__(to_date))

    return query.group_by(Medicine.id).order_by(Medicine.id).all()


# def load_books():
#     query = Books.query
#     return query.all()
#
#
# def load_book_patient_id(q=None):
#
#     query = db.session.query(Patient.id,
#                              func.sum(Books.booked_date)) \
#             .join(Patient, Patient.id.__eq__(Books.patient_id), isouter=True)
#
#     if q:
#         query = query.filter(Books.name.contains(q))
#
#     return query.all()