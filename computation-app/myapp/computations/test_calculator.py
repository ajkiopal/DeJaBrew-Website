from payroll_models import PlaceholderEmployee, PlaceholderAttendanceSummary
from calculator import generate_payroll

"""
USED FOR TESTING CALCULATOR.PY
"""

# Fake employee
emp = PlaceholderEmployee(
    employee_id=1,
    full_name="Juan Dela Cruz",
    employment_type="Barista",
    base_hourly_rate=120.0,
    overtime_hourly_rate=150.0,
    allowances=0.0
)

# Fake attendance
att = PlaceholderAttendanceSummary(
    employee_id=1,
    payroll_period_start="2026-02-01",
    payroll_period_end="2026-02-15",
    total_regular_hours=80,
    total_overtime_hours=6,
    total_late_hours=2,
    total_undertime_hours=1
)

payroll = generate_payroll(emp, att)

print("Regular Pay:", payroll.regular_pay)
print("Overtime Pay:", payroll.overtime_pay)
print("Late Deduction:", payroll.late_deduction)
print("Undertime Deduction:", payroll.undertime_deduction)
print("Gross Pay:", payroll.gross_pay)
print("Net Pay:", payroll.net_pay)