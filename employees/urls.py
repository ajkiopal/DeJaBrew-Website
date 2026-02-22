from django.urls import path
from . import views

urlpatterns = [
    path("employees/", views.employees_home, name="employees_home"),
    path("employees/<int:employee_id>/reset-password/", views.employee_reset_password, name="employee_reset_password"),
]