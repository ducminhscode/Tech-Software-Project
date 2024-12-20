from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import *
from phongmachtu import app, db


admin = Admin(app, name="Quan Ly Account", template_mode="bootstrap4")


class MyAccountView(ModelView):
    column_list = ['id', 'name', 'username', 'active']
    column_searchable_list = ['id', 'name']


class MyEmployeeView(ModelView):
    column_searchable_list = ['id', 'name', 'start_date']
    column_filters = ['id', 'name']


admin.add_view(MyAccountView(Account, db.session))
admin.add_view(MyEmployeeView(Doctor, Nurse, db.session))