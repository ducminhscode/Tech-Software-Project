import hashlib
from datetime import datetime
from click.decorators import R
from flask import render_template, Flask

import phongmachtu
from models import *
from phongmachtu import db
from sqlalchemy import extract, func, nullsfirst


def add_patient(name, username, password, address, day_of_birth, gender, phone):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = Patient(name=name, username=username, password=password, address=address, day_of_birth=day_of_birth,
                gender=gender, phone=phone)
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




def get_account_by_id(user_id):
    return Account.query.get(user_id)


# ================================= ADMIN ============================================
def stats_revenue(month=None):
    query = (db.session.query(extract('day', Receipt.created_date).label('Ngày'),
                              func.count(Patient.id).label('Số lượt khám'),
                              func.sum(Receipt.total_price).label('Doanh thu'),
                              extract('month', Receipt.created_date).label('Tháng'),
                              extract('year', Receipt.created_date).label('Năm'))
             .join(Receipt, Receipt.patient_id.__eq__(Patient.id))).group_by(extract('day', Receipt.created_date),
                                                                             extract('month', Receipt.created_date),
                                                                             extract('year', Receipt.created_date))
    if month:
        query = query.filter(Receipt.created_date.contains(month))

    return query.all()


def stats_frequency(month=None):
    query = db.session.query(extract('day', ExaminationForm.datetime).label('Ngày'),
                             (func.count(ExaminationForm.id) / 40 * 100).label('Tần suất khám'),
                             func.count(ExaminationForm.id).label('Số lượng'),
                             extract('month', ExaminationForm.datetime).label('Tháng'),
                             extract('year', ExaminationForm.datetime).label('Năm')
                             ).group_by(
        extract('day', ExaminationForm.datetime),
        extract('month', ExaminationForm.datetime),
        extract('year', ExaminationForm.datetime))

    if month:
        query = query.filter(ExaminationForm.datetime.contains(month))

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
    u = ExaminationForm(datetime=now, disease=disease, description=description, doctor_id=doctor_id,
                        patient_id=patient_id)
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


# ================================= NURSE ============================================
def add_patient_by_nurse(name, address, day_of_birth, gender, phone):
    u = Patient(name=name, address=address, day_of_birth=day_of_birth, gender=gender, phone=phone)
    db.session.add(u)
    db.session.commit()
    return u

def check_phone(phone_number):
    return Patient.query.filter_by(phone=phone_number).first()


def load_registration_form():
    return RegistrationForm.query.filter_by(lenLichKham=False).all()


def confirm_registration(reg_id):
    try:
        registration = RegistrationForm.query.get(reg_id)
        if registration:
            registration.lenLichKham = True
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Lỗi khi xác nhận lịch khám: {e}")
        db.session.rollback()
        return False


def registration_form_date(date):
    return RegistrationForm.query.filter_by(booked_date=date, lenLichKham = True).all()


# ================================= BOOKS ============================================
def save_booking(selected_date, symptom, patient_id, selected_time):
    u = RegistrationForm(
        booked_date=selected_date,
        desc=symptom,
        patient_id=patient_id,
        time_id=selected_time
    )
    db.session.add(u)
    db.session.commit()

def save_booking_by_nurse(selected_date, symptom, patient_id, selected_time):
    u = RegistrationForm(
        booked_date=selected_date,
        desc=symptom,
        patient_id=patient_id,
        time_id=selected_time,
        lenLichKham = True
    )
    db.session.add(u)
    db.session.commit()

# def load_times():
#     return Times.query.all()

def get_time_by_period(selected_time):
    return Times.query.filter_by(period=selected_time).first()

def get_all_period():
    periods = Times.query.with_entities(Times.id, Times.period).all()
    return periods
