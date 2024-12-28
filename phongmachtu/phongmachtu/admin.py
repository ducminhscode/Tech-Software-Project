from calendar import month
import hashlib
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Widget
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired

from models import *
from phongmachtu import app, db, dao
from flask_login import current_user, logout_user
from flask import request, redirect

admin = Admin(app, name="Phòng Mạch Tư", template_mode="bootstrap4")


class AuthenticatedAdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'administrator'

    def on_model_change(self, form, model, is_created):
        # Kiểm tra nếu có mật khẩu mới trong form
        if 'password' in form and form.password.data:
            # Băm mật khẩu trước khi lưu
            model.password = str(hashlib.md5(model.password.encode('utf-8')).hexdigest())
        super().on_model_change(form, model, is_created)


class AuthenticatedAdminBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'administrator'


class AdministratorView(AuthenticatedAdminModelView):
    column_list = ['id', 'name', 'username', 'joined_date']
    column_labels = {'id': 'STT', 'name': 'Tên', 'username': 'Tên đăng nhập', 'password': 'Mật khẩu',
                     'joined_date': 'Ngày tham gia', 'type': 'Vai trò'}
    column_searchable_list = ['name']
    column_filters = ['name']
    column_sortable_list = ['name', 'joined_date']
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    page_size = 10

    form_columns = ['name', 'username', 'password', 'type']

    form_extra_fields = {
        'password': PasswordField('Mật khẩu',validators=[DataRequired()])
    }

    form_overrides = {
        'type': SelectField
    }

    form_args = {
        'type': {
            'choices': [('administrator', 'Quản trị viên')],
            'widget': Select2Widget()
        }
    }


class DoctorView(AuthenticatedAdminModelView):
    column_list = ['id', 'name', 'username', 'license', 'joined_date']
    column_labels = {'id': 'STT', 'name': 'Tên', 'username': 'Tên đăng nhập', 'license': 'Chứng chỉ',
                     'joined_date': 'Ngày tham gia', 'type': 'Vai trò'}
    column_searchable_list = ['name']
    column_filters = ['name']
    column_sortable_list = ['name', 'joined_date']
    can_view_details = True
    edit_modal = True
    details_modal = True
    can_export = True
    page_size = 10

    form_columns = ['name', 'username', 'password', 'type', 'license']

    form_extra_fields = {
        'password': PasswordField('Mật khẩu',validators=[DataRequired()])
    }

    form_overrides = {
        'type': SelectField
    }

    form_args = {
        'type': {
            'choices': [('doctor', 'Bác sĩ')],
            'widget': Select2Widget()
        }
    }


class NurseView(AuthenticatedAdminModelView):
    column_list = ['id', 'name', 'username', 'phuTrachKhoa', 'joined_date']
    column_labels = {'id': 'STT', 'name': 'Tên', 'username': 'Tên đăng nhập', 'phuTrachKhoa': 'Khoa phụ trách',
                     'joined_date': 'Ngày tham gia', 'type': 'Vai trò'}
    column_searchable_list = ['name', 'phuTrachKhoa']
    column_filters = ['name', 'phuTrachKhoa']
    column_sortable_list = ['name', 'phuTrachKhoa', 'joined_date']
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    page_size = 10

    form_columns = ['name', 'username', 'password', 'type', 'phuTrachKhoa']

    form_extra_fields = {
        'password': PasswordField('Mật khẩu',validators=[DataRequired()])
    }

    form_overrides = {
        'type': SelectField
    }

    form_args = {
        'type': {
            'choices': [('nurse', 'Y tá')],
            'widget': Select2Widget()
        }
    }


class CashierView(AuthenticatedAdminModelView):
    column_list = ['id', 'name', 'username', 'license', 'joined_date']
    column_labels = {'id': 'STT', 'name': 'Tên', 'username': 'Tên đăng nhập', 'license': 'Chứng chỉ',
                     'joined_date': 'Ngày tham gia', 'type': 'Vai trò'}
    column_searchable_list = ['name']
    column_filters = ['name']
    column_sortable_list = ['name', 'joined_date']
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    page_size = 10

    form_columns = ['name', 'username', 'password', 'type', 'license']

    form_extra_fields = {
        'password': PasswordField('Mật khẩu',validators=[DataRequired()])
    }

    form_overrides = {
        'type': SelectField
    }

    form_args = {
        'type': {
            'choices': [('cashier', 'Thu ngân')],
            'widget': Select2Widget()
        }
    }


class PatientView(AuthenticatedAdminModelView):
    column_list = ['id', 'name', 'username', 'address', 'day_of_birth', 'gender', 'phone', 'email', 'joined_date']
    column_labels = {'id': 'STT', 'name': 'Tên', 'username': 'Tên đăng nhập', 'address': 'Địa chỉ',
                     'day_of_birth': 'Ngày sinh', 'email': 'Email',
                     'gender': 'Giới tính', 'phone': 'Số điện thoại', 'joined_date': 'Ngày tham gia', 'type': 'Vai trò'}
    column_searchable_list = ['name', 'phone', 'email']
    column_filters = ['name', 'address', 'phone', 'day_of_birth']
    column_sortable_list = ['name', 'joined_date', 'day_of_birth']
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    page_size = 10

    form_columns = ['name', 'username', 'password', 'type', 'address', 'day_of_birth', 'gender', 'phone', 'email']

    form_extra_fields = {
        'password': PasswordField('Mật khẩu',validators=[DataRequired()])
    }

    form_overrides = {
        'type': SelectField
    }

    form_args = {
        'type': {
            'choices': [('patient', 'Bệnh nhân')],
            'widget': Select2Widget()
        }
    }


class MedicineView(AuthenticatedAdminModelView):
    column_display_pk = True
    column_labels = {'id': 'STT', 'name': 'Tên', 'unit': 'Đơn vị', 'price': 'Giá', 'usage': 'Cách sử dụng'}
    column_searchable_list = ['name']
    column_filters = ['name', 'unit', 'price']
    column_sortable_list = ['name', 'price']
    column_editable_list = ['usage']
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    page_size = 10


class TimesView(AuthenticatedAdminModelView):
    column_display_pk = True
    column_labels = {'id': 'STT', 'period': 'Giờ'}
    column_searchable_list = ['period']
    column_filters = ['period']
    column_editable_list = ['period']
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    page_size = 10


class RegulationsView(AuthenticatedAdminModelView):
    column_list = ['id', 'change_date', 'name', 'value', 'administrator']
    column_labels = {'id': 'STT', 'change_date': 'Ngày thay đổi', 'name': 'Tên quy định', 'value': 'Trị số',
                     'administrator': 'Quản trị viên'}
    column_searchable_list = ['name']
    column_filters = ['change_date']
    column_sortable_list = ['change_date']
    column_editable_list = ['name', 'value']
    form_columns = ['name', 'value']

    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    page_size = 10

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.admin_id = current_user.id
        return super().on_model_change(form, model, is_created)


class ReceiptView(AuthenticatedAdminModelView):
    column_display_pk = True
    column_list = ['id', 'patient', 'created_date', 'examines_price', 'medicines_price', 'total_price', 'cashier']
    column_labels = {'id': 'STT', 'patient': 'Bệnh nhân', 'created_date': 'Ngày tạo', 'examines_price': 'Tiền khám',
                     'total_price': 'Tổng tiền', 'cashier': 'Thu ngân', 'medicines_price': 'Tiền thuốc'}
    column_searchable_list = ['created_date']
    column_sortable_list = ['created_date', 'total_price']
    can_view_details = True
    can_export = True
    can_edit = False
    can_create = False
    details_modal = True
    page_size = 10

    def display_medicine_prices(view, context, model, name):
        return ', '.join(str(detail.medicines_price) for detail in model.receipt_details)

    column_formatters = {
        'medicines_price': display_medicine_prices
    }


admin.add_view(AdministratorView(Administrator, db.session, name="Quản trị viên"))
admin.add_view(DoctorView(Doctor, db.session, name="Bác sĩ"))
admin.add_view(NurseView(Nurse, db.session, name="Y tá"))
admin.add_view(CashierView(Cashier, db.session, name="Thu ngân"))
admin.add_view(PatientView(Patient, db.session, name="Bệnh nhân"))
admin.add_view(MedicineView(Medicine, db.session, name="Thuốc"))
admin.add_view(TimesView(Times, db.session, name="Khung giờ"))
admin.add_view(RegulationsView(Regulations, db.session, name="Quy định"))
admin.add_view(ReceiptView(Receipt, db.session, name="Hóa đơn"))


class StatsRevenueView(AuthenticatedAdminBaseView):

    @expose('/')
    def index(self):
        rev = dao.stats_revenue(month=request.args.get('month'))
        return self.render('admin/stats_revenue.html', rev=rev)


class StatsFrequencyView(AuthenticatedAdminBaseView):
    @expose('/')
    def index(self):
        fre = dao.stats_frequency(month=request.args.get('month'))
        return self.render('admin/stats_frequency.html', fre=fre)


class StatsMedicineView(AuthenticatedAdminBaseView):
    @expose('/')
    def index(self):
        med = dao.stats_medicine(kw=request.args.get('kw'),
                                 from_date=request.args.get('from_date'), to_date=request.args.get('to_date'))
        return self.render('admin/stats_medicine.html', med=med)


admin.add_view(StatsRevenueView(name='Doanh thu'))
admin.add_view(StatsFrequencyView(name="Tần suất khám"))
admin.add_view(StatsMedicineView(name="Tần suất sử dụng thuốc"))


class LogoutView(AuthenticatedAdminBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(LogoutView(name="Đăng xuất"))
