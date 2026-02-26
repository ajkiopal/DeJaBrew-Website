from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PayPeriod, PayrollRun

admin.site.register(PayPeriod)
admin.site.register(PayrollRun)