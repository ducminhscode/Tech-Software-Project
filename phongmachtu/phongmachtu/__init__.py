from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)

app.secret_key = "%^$DSD^%^%^%^%^DSSD"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/phongmachdb?charset=utf8mb4" % quote('Admin@123') # 021020
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
login = LoginManager(app)


cloudinary.config(
    cloud_name= 'dp9b0dkkt',
    api_key= '785552982855161',
    api_secret= 'v4laZXdEttJZYUUr3sSJFRzGV30'
)