import hashlib
from datetime import datetime
from click.decorators import R

from models import *
from phongmachtu import db
from sqlalchemy import extract, func, nullsfirst


def add_account(name, username, password, type):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = Account(name=name, username=username, password=password, type=type)
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


def auth_account(username, password, type=None):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    query = Account.query.filter(Account.username.__eq__(username),
                                 Account.password.__eq__(password))
    if type:
        query = query.filter(Account.type.__eq__(type))
    return query.first()


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


# ================================= ADMIN ============================================
def stats_revenue(month=None):
    query = db.session.query(Receipt.created_date, func.count(Patient.id), func.sum(Receipt.total_price)).join(Receipt,
                                                                                                               Receipt.patient_id.__eq__(
                                                                                                                   Patient.id))
    if month:
        query = query.filter(Receipt.created_date.contains(month))

    return query.group_by(Receipt.created_date).all()


def stats_frequency(year=None):
    query = db.session.query(extract('month', ExaminationForm.datetime).label('Tháng'),
                             (func.count(ExaminationForm.id) / 40 * 100).label('Tần suất khám')).group_by(
        extract('month', ExaminationForm.datetime))

    if year:
        query = query.filter(ExaminationForm.datetime.contains(year))

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


# =================================Patient============================================
def load_patient():
    return Patient.query.all()


def get_patient_id(kw=None):
    if not kw:  # Nếu không có từ khóa, trả về None hoặc []
        return []  # Hoặc return []

    query = Patient.query.filter(Patient.name.contains(kw))
    return query.all()


def load_examination_form(kw=None):
    query = ExaminationForm.query
    if kw:
        query = (db.session.query(ExaminationForm.datetime, ExaminationForm.description)
                 .join(Patient, Patient.id == ExaminationForm.patient_id)
                 .filter(Patient.name.contains(kw)))

    return query.all()

# =================================Doctor============================================
def load_doctor():
    return Doctor.query.all()


def add_examination_form(description, disease, doctor_id, patient_id):
    now = datetime.now()
    u = ExaminationForm(datetime=now, disease=disease, description=description, doctor_id=doctor_id, patient_id=patient_id)
    db.session.add(u)
    db.session.commit()


def list_examination_by_doctor(doctor_id):
    query = (
        db.session.query(Patient.name, Patient.day_of_birth, Patient.gender, Patient.phone)
        .join(ExaminationForm, Patient.id == ExaminationForm.patient_id)  # Patient~~ExaminationForm
        .filter(ExaminationForm.doctor_id == doctor_id)
    )
    return query.all()


def examination_form_by_patient_id(patient_id=None):
    query = (
        db.session.query(Patient.name, Patient.day_of_birth, Patient.gender)
        .join(ExaminationForm, Patient.id == ExaminationForm.patient_id)  # Patient~~ExaminationForm
        .filter(ExaminationForm.patient_id == patient_id))

    return query.first()


# ================================= BOOKS ============================================
def save_booking(selected_time, selected_date):
    return None
