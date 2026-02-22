from django.db import models

class Attendance(models.Model):
    # We use an IntegerField for EmployeeID for now until the Employee app is built
    employee_id = models.IntegerField() 
    
    # The merged date/time fields from your EERD
    start_date_time = models.DateTimeField() 
    end_date_time = models.DateTimeField()   
    
    # Source system (e.g., UTAK)
    source_system = models.CharField(max_length=50, default='UTAK', null=True, blank=True) 

    def __str__(self):
        return f"Employee {self.employee_id} - {self.start_date_time.date()}"