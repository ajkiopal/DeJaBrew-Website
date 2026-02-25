from django.db import models

class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=50)
    base_hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    overtime_hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class AttendanceSummary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    payroll_period_start = models.DateField()
    payroll_period_end = models.DateField()
    total_regular_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_overtime_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_late_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_undertime_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class PayrollRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    payroll_period_start = models.DateField()
    payroll_period_end = models.DateField()
    gross_pay = models.DecimalField(max_digits=12, decimal_places=2)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2)
    is_finalized = models.BooleanField(default=False)


class AdjustmentRecord(models.Model):
    payroll_record = models.ForeignKey(PayrollRecord, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    adjustment_type = models.CharField(max_length=50)
    justification = models.TextField()
    admin_id = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)