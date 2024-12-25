import hashlib
from datetime import datetime
from click.decorators import R
from flask import render_template, Flask

import phongmachtu
from models import *
from phongmachtu import db
from sqlalchemy import extract, func, nullsfirst
import cloudinary.uploader


def add_patient(name, username, password, avatar, address, day_of_birth, gender, phone):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = Patient(name=name, username=username, password=password, avatar=avatar, address=address, day_of_birth=day_of_birth,
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


def update_info(day_of_birth, phone, address, avatar, patient_id, gender):
    p = Patient.query.filter_by(id=patient_id).first()
    a = Account.query.filter_by(id=patient_id).first()
    if p:
        p.day_of_birth = day_of_birth
        p.phone = phone
        p.address = address
        p.gender = gender
        if avatar:
            my_folder = "PhongMachTu"
            response = cloudinary.uploader.upload(avatar, folder=my_folder)
            a.avatar = response['secure_url']

        db.session.commit()


def update_password(user_id, new_password):
    user = Account.query.get(user_id)
    if user:
        hashed_password = str(hashlib.md5(new_password.encode('utf-8')).hexdigest())
        user.password = hashed_password
        db.session.commit()
        return True
    else:
        return False


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
                             func.sum(PrescriptionMedicine.quantity)) \
        .join(Medicine, Medicine.id.__eq__(PrescriptionMedicine.medicine_id), isouter=True)

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


def check_phone(phone_number):
    return Patient.query.filter_by(phone=phone_number).first()


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


def load_medicine():
    medicines = Medicine.query.with_entities(Medicine.name, Medicine.unit).all()
    return medicines


def add_examination_form(doctor_id, patient_id, disease, medicine_names, quantities, units, usages):
    today_date = datetime.today().date()

    examination_form = ExaminationForm(
        datetime=today_date,
        disease=disease,
        doctor_id=doctor_id,
        patient_id=patient_id
    )
    db.session.add(examination_form)
    db.session.commit()  # Commit để có id cho examination_form

    prescription = Prescription(
        exam_date=today_date,
        examinationForm_id=examination_form.id
    )
    db.session.add(prescription)
    db.session.commit()

    for i in range(len(medicine_names)):
        medicine = Medicine.query.filter_by(name=medicine_names[i]).first()

        if medicine:
            prescription_medicine = PrescriptionMedicine(
                prescription_id=prescription.id,
                medicine_id=medicine.id,
                quantity=quantities[i],
                guide=usages[i]
            )

            # Thêm vào bảng PrescriptionMedicine
            db.session.add(prescription_medicine)
            db.session.commit()

    return prescription.id


def change_isKham(patient_id):
    today_date = datetime.today().date()
    registration = RegistrationForm.query.filter_by(patient_id=patient_id, booked_date=today_date).first()

    if registration:
        registration.isKham = True
        db.session.commit()
        return True
    else:
        return False



def load_registration_form_by_day(today):
    return RegistrationForm.query.filter_by(lenLichKham=True, booked_date=today, isKham=False).all()


# ================================= NURSE ============================================
def add_patient_by_nurse(name, address, day_of_birth, gender, phone):
    u = Patient(name=name, address=address, day_of_birth=day_of_birth, gender=gender, phone=phone)
    db.session.add(u)
    db.session.commit()
    return u


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
    return RegistrationForm.query.filter_by(booked_date=date, lenLichKham=True).all()


# ================================= CASHIER ============================================
def set_receipt(prescription_id, patient_id, medicine_names, quantities):
    try:
        new_receipt = Receipt(
            created_date=datetime.now(),
            examines_price=100000,
            isPaid=False,
            patient_id=patient_id
        )

        db.session.add(new_receipt)
        db.session.flush()

        total_price = 0
        for name, quantity in zip(medicine_names, quantities):
            medicine = Medicine.query.filter_by(name=name).first()
            if not medicine:
                raise ValueError(f"Medicine with name {name} not found.")

            quantity = float(quantity)
            medicines_price = quantity * medicine.price
            total_price += medicines_price

        new_detail = ReceiptDetails(
            medicines_price=total_price,
            receipt_id=new_receipt.id,
            prescription_id=prescription_id
        )

        db.session.add(new_detail)
        new_receipt.total_price = total_price + new_receipt.examines_price
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return None

def get_receipt_by_id_and_time(patient_code):
    return Receipt.query.filter_by(patient_id = patient_code, isPaid = False).first()

def load_receipt(kw):
    return Receipt.query.filter_by(patient_id=kw).all()


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
        lenLichKham=True
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


def get_information_examination(patient_id):
    examinations = ExaminationForm.query.filter_by(patient_id=patient_id).all()

    result = []
    for exam in examinations:
        result.append({
            "id": exam.id,
            "datetime": exam.datetime.strftime('%Y-%m-%d'),
            "disease": exam.disease,
            "doctor_name": Doctor.query.get(exam.doctor_id).name if Doctor.query.get(exam.doctor_id) else None,
            "prescriptions": [
                {
                    "medicine_name": pres_med.medicine.name,
                    "quantity": pres_med.quantity,
                    "unit": pres_med.medicine.unit,
                    "guide": pres_med.guide
                }
                for pres in exam.prescription
                for pres_med in pres.prescription_medicines
            ]
        })

    return result


