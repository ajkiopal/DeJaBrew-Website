from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)

class PayrollPeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    is_finalized = models.BooleanField(default=False)

class PayrollRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE)

    hours_worked = models.DecimalField(max_digits=6, decimal_places=2)
    gross_pay = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)

    adjusted_gross = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    adjusted_deductions = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    adjusted_net = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class PayrollAdjustment(models.Model):
    payroll_record = models.ForeignKey(PayrollRecord, on_delete=models.CASCADE)

    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    justification = models.TextField()
    admin_id = models.IntegerField() 
    timestamp = models.DateTimeField(auto_now_add=True)

class AuditLog(models.Model):
    payroll_record = models.ForeignKey(PayrollRecord, on_delete=models.CASCADE)

    admin_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    old_gross = models.DecimalField(max_digits=10, decimal_places=2)
    old_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    old_net = models.DecimalField(max_digits=10, decimal_places=2)

    justification = models.TextField()

