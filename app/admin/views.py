from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.mongoengine import ModelView
from app.models.enrollments import EnrolledSubject

from app.models.students import Student
from app.models.subjects import Subject
from app.models.users import User

# Definir la vista para la página de inicio
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return super(MyAdminIndexView, self).index()

# Crear una instancia de Flask-Admin con la vista predeterminada
admin = Admin(index_view=MyAdminIndexView())

# Crear una vista para el modelo Student
class StudentView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False

class SubjectView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False

class EnrroledSubjectView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False

class UserView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False

# Agregar vista del modelo
admin.add_view(StudentView(Student))
admin.add_view(SubjectView(Subject))
admin.add_view(EnrroledSubjectView(EnrolledSubject))
admin.add_view(UserView(User))