from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, false
from sqlalchemy.orm import relationship
from phongmachtu import app, db
from flask_login import UserMixin


class Account(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now)


class Doctor(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    start_date = Column(String(50), nullable=False)
    patients = relationship('Patient', backref='doctor', lazy=True)


class Nurse(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    start_date = Column(String(50), nullable=False)
    patients = relationship('Patient', backref='nurses', lazy=True)


class Patient(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    address = Column(String(50))
    day_of_birth = Column(String(50))
    gender = Column(Boolean)
    phone = Column(String(10))


class Cashier(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    receipts = relationship('Receipt', backref='cashier', lazy=True)


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now)
    cashier_id = Column(Integer, ForeignKey(Cashier.id), nullable=False)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)
    examines_price = Column(Float, default=100000)
    total_price = Column(Float, default=0)
    receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class Time(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    period = Column(String(20), nullable=False)
    books_times = relationship('Books', backref='time', lazy=True)


class Books(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    booked_date = Column(DateTime, default=datetime.now)
    patient_id = Column(Integer, ForeignKey(Patient.id, onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    patient_name = Column(String(50), nullable=False)
    rel = Column(String(50), nullable=False) #Quan hệ voi nguoi dat lich kham
    time_id = Column(Integer, ForeignKey(Time.id), nullable=False)
    desc = Column(String(500))
    lenLichKham = Column(Boolean, default=False)
    isKham = Column(Boolean, default=False)


class MedicalForm(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.now)
    description = Column(String(100))
    disease = Column(String(50), nullable=False)
    doctor_id = Column(Integer, ForeignKey(Doctor.id), nullable=False)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)
    prescription = relationship('Prescription', backref='medicalForm', lazy=True)


class Medicine(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    unit = Column(String(10), nullable=False)
    price = Column(Integer, nullable=False)
    prescription = relationship('Prescription', backref='medicine', lazy=True)


class Prescription(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    quantity = Column(Integer, default=0)
    guide = Column(String(100))
    medicalForm_id = Column(Integer, ForeignKey(MedicalForm.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='prescription', lazy=True)


class ReceiptDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    medicines_price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    prescription_id = Column(Integer, ForeignKey(Prescription.id), nullable=False)


if __name__ == "__main__":
    with app.app_context():
        import hashlib
        u = Patient(name="ChuongTN", username="admin",
             password=str(hashlib.md5("123".encode('utf-8')).hexdigest()))
        db.session.add(u)

        time_periods = ["Sáng", "Chiều", "Tối"]

        for period in time_periods:
            time = Time(period=period)
            db.session.add(time)


        db.create_all()
        db.session.commit()
