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


cloudinary.config(
    cloud_name= 'dp9b0dkkt',
    api_key= '785552982855161',
    api_secret= 'v4laZXdEttJZYUUr3sSJFRzGV30'
)

# account_sid = 'ACe58c46baa657f47308ae947d3b2a23da'
# auth_token = '[AuthToken]'
# client = Client(account_sid, auth_token)
#
# message = client.messages.create(
#   from_='+12314488348',
#   to='+84938563416'
# )

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USERNAME'] = '2251012095minh@ou.edu.vn'
# app.config['MAIL_PASSWORD'] = os.getenv('password_email')
# app.config['MAIL_DEFAULT_SENDER'] = '2251012095minh@ou.edu.vn'
#
# mail = Mail(app)