from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import *
from phongmachtu import app, db


admin = Admin(app, name="Quan Ly Account", template_mode="bootstrap4")


class MyAccountView(ModelView):
    column_list = ['name', 'username', 'active']
    column_searchable_list = ['name']


class MyEmployeeView(ModelView):
    column_searchable_list = ['name', 'start_date']
    column_filters = ['name']


admin.add_view(MyAccountView(Account, db.session))
admin.add_view(MyEmployeeView(Doctor, db.session))
admin.add_view(MyEmployeeView(Nurse, db.session))