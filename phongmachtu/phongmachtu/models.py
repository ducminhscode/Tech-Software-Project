from datetime import datetime
from enum import unique

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, false, Date, column
from sqlalchemy.orm import relationship
from phongmachtu import app, db
from flask_login import UserMixin


class Account(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    username = Column(String(50), unique=True)
    password = Column(String(50))
    joined_date = Column(DateTime, default=datetime.now)
    avatar = Column(String(255))

    type = Column(String(20), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }


class Administrator(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)

    regulations = relationship('Regulations', backref='administrator', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'administrator'
    }

    def __str__(self):
        return self.name


class Doctor(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    license = Column(String(200), nullable=False)
    examination_forms = relationship('ExaminationForm', backref='doctor', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'doctor'
    }

    def __str__(self):
        return self.name


class Nurse(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    phuTrachKhoa = Column(String(200))

    __mapper_args__ = {
        'polymorphic_identity': 'nurse'
    }

    def __str__(self):
        return self.name


class Patient(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    address = Column(String(200), nullable=False)
    day_of_birth = Column(String(50))
    gender = Column(String(10), nullable=False)
    phone = Column(String(10), unique=True, nullable=False)
    email = Column(String(255),unique=True,nullable=False)

    registration_form = relationship('RegistrationForm', cascade="all,delete", backref='patient', lazy=True)
    examination_forms = relationship('ExaminationForm', backref='patient', lazy=True)
    receipts = relationship('Receipt', backref='patient', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'patient'
    }

    def __str__(self):
        return self.name


class Cashier(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    license = Column(String(200), nullable=False)

    receipts = relationship('Receipt', backref='cashier', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'cashier'
    }

    def __str__(self):
        return self.name


class Times(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    period = Column(String(100), nullable=False)

    registration_form = relationship('RegistrationForm', backref='time', lazy=True)


class RegistrationForm(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    booked_date = Column(Date, default=datetime.now())
    desc = Column(String(500))
    lenLichKham = Column(Boolean, default=False)
    isKham = Column(Boolean, default=False)

    patient_id = Column(Integer, ForeignKey(Patient.id, onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    time_id = Column(Integer, ForeignKey(Times.id), nullable=False)

    def __repr__(self):
        return f"<YourModel(booked_date='{self.booked_date.strftime('%Y-%m-%d')}')>"

    def __str__(self):
        return self.id


class ExaminationForm(db.Model):
    id = Column(Integer, ForeignKey(RegistrationForm.id), primary_key=True)  # Dùng ForeignKey từ RegistrationForm
    datetime = Column(DateTime, default=datetime.now)
    disease = Column(String(200), nullable=False)

    doctor_id = Column(Integer, ForeignKey(Doctor.id), nullable=False)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)
    prescription = relationship('Prescription', backref='examinationForm', lazy=True)

    def __repr__(self):
        return f"<YourModel(booked_date='{self.booked_date.strftime('%Y-%m-%d')}')>"

    def __str__(self):
        return Patient.query.get(self.patient_id).name


class Medicine(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    unit = Column(String(10), nullable=False)
    price = Column(Integer, nullable=False)
    usage = Column(String(200))

    prescription_medicines = relationship('PrescriptionMedicine', backref='medicine', lazy=True)

    def __str__(self):
        return self.name


class Prescription(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    exam_date = Column(Date, default=datetime.now)

    examinationForm_id = Column(Integer, ForeignKey(ExaminationForm.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='prescription', lazy=True)
    prescription_medicines = relationship('PrescriptionMedicine', backref='prescription', lazy=True)

    def __str__(self):
        return Medicine.query.get(self.medicine_id).name


class PrescriptionMedicine(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    prescription_id = Column(Integer, ForeignKey(Prescription.id), nullable=False)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    quantity = Column(Integer, default=0)
    guide = Column(String(100))


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now)
    examines_price = Column(Float, default=100000)
    total_price = Column(Float, default=0)
    isPaid = Column(Boolean, default=False)

    receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)
    cashier_id = Column(Integer, ForeignKey(Cashier.id))
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)

    def __repr__(self):
        return f"<YourModel(booked_date='{self.booked_date.strftime('%Y-%m-%d')}')>"

    def __str__(self):
        return Patient.query.get(self.patient_id).name


class ReceiptDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    medicines_price = Column(Float, default=0)

    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    prescription_id = Column(Integer, ForeignKey(Prescription.id), nullable=False)


class Regulations(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    change_date = Column(Date, default=datetime.now)
    name = Column(String(50), nullable=False)
    value = Column(Integer, nullable=False)
    admin_id = Column(Integer, ForeignKey(Administrator.id), nullable=False)

    def __repr__(self):
        return f"<YourModel(booked_date='{self.booked_date.strftime('%Y-%m-%d')}')>"


if __name__ == "__main__":
    with app.app_context():
        import hashlib

        db.create_all()
        a = Administrator(name="Admin", username="admin",
                          password=str(hashlib.md5("1".encode('utf-8')).hexdigest()), type="administrator")

        d = Doctor(name="Doctor", username="doctor",
                   password=str(hashlib.md5("1".encode('utf-8')).hexdigest()), type="doctor",
                   license="Giấy phép hành nghề")

        n = Nurse(name='Nurse', username="nurse",
                  password=str(hashlib.md5("1".encode('utf-8')).hexdigest()), type="nurse", phuTrachKhoa="A")

        c = Cashier(name='Cashier', username="cashier",
                    password=str(hashlib.md5("1".encode('utf-8')).hexdigest()), type="cashier",
                    license="Giấy phép hành nghề")

        db.session.add(a)
        db.session.add(d)
        db.session.add(n)
        db.session.add(c)

        time_periods = ["Sáng: 7 giờ đến 11 giờ", "Chiều: 13 giờ đến 17 giờ", "Tối: 18 giờ đến 22 giờ"]

        for period in time_periods:
            time = Times(period=period)
            db.session.add(time)

        m1 = Medicine(name='Paracetamol', unit='Viên', price=5000, usage='Thuốc giảm đau, hạ sốt')
        m2 = Medicine(name='Ibuprofen', unit='Vỹ', price=50000, usage='Thuốc giảm đau, hạ sốt')
        m3 = Medicine(name='Aspirin', unit='Chai', price=200000, usage='Thuốc giảm đau, hạ sốt')


        m4 = Medicine(name='Diclofenac', unit='Vỹ', price=20000, usage='Thuốc kháng viêm')
        m5 = Medicine(name='Celecoxib', unit='Chai', price=60000, usage='Thuốc kháng viêm')
        m6 = Medicine(name='Prednisolone', unit='Viên', price=2000, usage='Thuốc kháng viêm')

        m7 = Medicine(name='Amoxicillin', unit='Viên', price=5000, usage='Thuốc kháng sinh')
        m8 = Medicine(name='Ciprofloxacin', unit='Chai', price=150000, usage='Thuốc kháng sinh')
        m9 = Medicine(name='Azithromycin', unit='Viên', price=3000, usage='Thuốc kháng sinh')
        m10 = Medicine(name='Doxycycline', unit='Vỹ', price=50000, usage='Thuốc kháng sinh')

        m11 = Medicine(name='Omeprazole', unit='Viên', price=1000, usage='Thuốc điều trị tiêu hóa')
        m12 = Medicine(name='Lansoprazole', unit='Chai', price=30000, usage='Thuốc điều trị tiêu hóa')
        m13 = Medicine(name='Ranitidine', unit='Chai', price=35000, usage='Thuốc điều trị tiêu hóa')
        m14 = Medicine(name='Metoclopramide', unit='Vỹ', price=10000, usage='Thuốc điều trị tiêu hóa')

        m15 = Medicine(name='Amlodipine', unit='Vỹ', price=40000, usage='Thuốc điều trị tim mạch')
        m16 = Medicine(name='Atenolol', unit='Vỹ', price=40000, usage='Thuốc điều trị tim mạch')
        m17 = Medicine(name='Enalapril', unit='Viên', price=4000, usage='Thuốc điều trị tim mạch')
        m18 = Medicine(name='Simvastatin', unit='Chai', price=120000, usage='Thuốc điều trị tim mạch')

        m19 = Medicine(name='Metformin', unit='Viên', price=1000, usage='Thuốc điều trị tiểu đường')
        m20 = Medicine(name='Gliclazide', unit='Viên', price=3000, usage='Thuốc điều trị tiểu đường')
        m21 = Medicine(name='Insulin', unit='Chai', price=30000, usage='Thuốc điều trị tiểu đường')

        m22 = Medicine(name='Loratadine', unit='Chai', price=45000, usage='Thuốc chống dị ứng')
        m23 = Medicine(name='Cetirizine', unit='Vỹ', price=15000, usage='Thuốc chống dị ứng')
        m24 = Medicine(name='Fexofenadine', unit='Chai', price=50000, usage='Thuốc chống dị ứng')

        m25 = Medicine(name='Diazepam', unit='Viên', price=2000, usage='Thuốc điều trị bệnh thần kinh')
        m26 = Medicine(name='Gabapentin', unit='Vỹ', price=20000, usage='Thuốc điều trị bệnh thần kinh')
        m27 = Medicine(name='Amitriptyline', unit='Viên', price=3000, usage='Thuốc điều trị bệnh thần kinh')

        m28 = Medicine(name='Salbutamol', unit='Chai', price=200000, usage='Thuốc điều trị bệnh hô hấp')
        m29 = Medicine(name='Budesonide', unit='Chai', price=210000, usage='Thuốc điều trị bệnh hô hấp')
        m30 = Medicine(name='Montelukast', unit='Viên', price=7000, usage='Thuốc điều trị bệnh hô hấp')

        medicines = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10,
                     m11, m12, m13, m14, m15, m16, m17, m18, m19, m20,
                     m21, m22, m23, m24, m25, m26, m27, m28, m29, m30]

        for medicine in medicines:
            db.session.add(medicine)



        re1 = Regulations(name='Số lượng bệnh nhân tối đa', value=40, admin_id=1)
        re2 = Regulations(name='Giá tiền khám', value=100000, admin_id=1)

        db.session.add(re1)
        db.session.add(re2)
        db.session.commit()


