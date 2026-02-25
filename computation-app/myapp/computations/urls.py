from django.urls import path
from . import views

urlpatterns = [
    path('adjustments/', views.adjustments_view, name='adjustments'),
    path('adjustments/<int:employee_id>/', views.adjustments_view, name='adjustments'),
]