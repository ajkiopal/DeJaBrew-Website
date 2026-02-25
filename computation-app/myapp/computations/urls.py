from django.urls import path
from . import views

urlpatterns = [
    path('test-payslip/', views.test_payslip_view, name='test-payslip'),
]