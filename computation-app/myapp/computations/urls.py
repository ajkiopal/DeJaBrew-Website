from django.urls import path
from . import views

urlpatterns = [
    path('adjustments/<int:employee_id>/', views.adjustments_view, name='adjustments'),
    path('test-payslip/', views.adjustments_view, name='test_payslip'),
]