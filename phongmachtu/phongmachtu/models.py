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

        # p1 = Patient(name='Patient1', username="patient1",
        #              password=str(hashlib.md5("1".encode('utf-8')).hexdigest()), type="patient",
        #              address='GV, HCM', day_of_birth="2003", gender='Nam', phone="0123456789", )
        #
        # p2 = Patient(name='Patient2', username="patient2",
        #              password=str(hashlib.md5("1".encode('utf-8')).hexdigest()), type="patient",
        #              address='Nha Be, HCM', day_of_birth="2003", gender='Nữ', phone="0987654321")

        db.session.add(a)
        db.session.add(d)
        db.session.add(n)
        db.session.add(c)
        # db.session.add(p1)
        # db.session.add(p2)

        time_periods = ["Sáng: 7 giờ đến 11 giờ", "Chiều: 13 giờ đến 17 giờ"]

        for period in time_periods:
            time = Times(period=period)
            db.session.add(time)

        m1 = Medicine(name='Panadol', unit='Vỉ', price=25000, usage='Thuốc giảm đau, hạ sốt')
        m2 = Medicine(name='Becberin', unit='Lọ', price=20000, usage='Thuốc tiêu hóa')
        m3 = Medicine(name='Paracetamol', unit='Vỉ', price=30000, usage='Thuốc hạ sốt, cảm cúm')
        m4 = Medicine(name='Thuốc ho Prospan', unit='Chai', price=30000, usage='Thuốc giảm ho, trị ho dai ho có đờm')

        db.session.add(m1)
        db.session.add(m2)
        db.session.add(m3)
        db.session.add(m4)

        # b1 = RegistrationForm(patient_id=5, desc='Sốt, Ho', lenLichKham=False, isKham=False, time_id=2)
        # b2 = RegistrationForm(patient_id=6, desc='Cảm', lenLichKham=True, isKham=False, time_id=6)
        #
        # db.session.add(b1)
        # db.session.add(b2)
        #
        # r = Receipt(examines_price='20000', total_price='100000', cashier_id=4, patient_id=5)
        # r2 = Receipt(examines_price='30000', total_price='200000', cashier_id=4, patient_id=6)
        #
        # db.session.add(r)
        # db.session.add(r2)
        # db.session.commit()
        #
        # e = ExaminationForm(id=1, disease='Sốt nhẹ', doctor_id=2, patient_id=5)
        # e1 = ExaminationForm(id=2, disease='Say nắng', doctor_id=2, patient_id=6)
        #
        # db.session.add(e)
        # db.session.add(e1)
        #
        # p = Prescription(examinationForm_id=1)
        # p2 = Prescription(examinationForm_id=2)
        #
        # db.session.add(p)
        # db.session.add(p2)
        #
        # rd = ReceiptDetails(medicines_price='4000', receipt_id=1, prescription_id=1)
        # rd2 = ReceiptDetails(medicines_price='6000', receipt_id=2, prescription_id=2)
        #
        # db.session.add(rd)
        # db.session.add(rd2)
        #
        # ru = Regulations(name='minh', value='200000', admin_id=1)
        # ru2 = Regulations(name='zoen', value='900000', admin_id=1)
        #
        # db.session.add(ru)
        # db.session.add(ru2)
        #
        # r2 = Receipt(examines_price='90000', total_price='110000', cashier_id=4, patient_id=6)
        # db.session.add(r2)
        #
        # pm = PrescriptionMedicine(prescription_id=1, medicine_id=2,quantity=50,guide='3 viên/ngày, uống sau khi ăn')
        # pm2 = PrescriptionMedicine(prescription_id=2, medicine_id=4, quantity=100, guide='2 viên sáng/chiều, uống sau khi ăn')
        # db.session.add(pm)
        # db.session.add(pm2)

        re1 = Regulations(name='Số lượng bệnh nhân tối đa', value=40, admin_id=1)
        re2 = Regulations(name='Giá tiền khám', value=100000, admin_id=1)

        db.session.add(re1)
        db.session.add(re2)
        db.session.commit()


