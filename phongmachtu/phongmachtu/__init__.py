from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary
import os



app = Flask(__name__)
app.secret_key = "%^$DSD^%^%^%^%^DSSD"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/phongmachdb?charset=utf8mb4" % quote('021020') # 021020
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
login = LoginManager(app)

# Tạo file .env trong package phongmachtu và điền các thông tin sau để upload ảnh lên cloudinary và gửi email:
# cloud_name=
# api_key=
# api_secret=
# email=
# password_email=
# Chú ý: cần có email đã được xác thực 2 bước và đã có App Password


cloudinary.config(
    cloud_name= os.getenv('cloud_name'),
    api_key= os.getenv('api_key'),
    api_secret= os.getenv('api_secret')
)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('email')
app.config['MAIL_PASSWORD'] = os.getenv('password_email')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('email')

mail = Mail(app)