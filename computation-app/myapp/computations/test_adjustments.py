from payroll_models import PayrollComputation, PayrollAdjustment
from adjustments import apply_adjustment

import datetime

"""
USED FOR TESTING ADJUSTMENTS.PY
"""

# Example payroll
payroll = PayrollComputation(
    employee_id=1,
    payroll_period_start="2026-02-01",
    payroll_period_end="2026-02-15",
    regular_pay=9600,
    overtime_pay=900,
    late_deduction=240,
    undertime_deduction=120,
    gross_pay=10140,
    total_adjustments=0,
    net_pay=10140
)

# Example adjustment (bonus)
adjustment = PayrollAdjustment(
    adjustment_id=1,
    employee_id=1,
    payroll_period_start="2026-02-01",
    payroll_period_end="2026-02-15",
    amount=500,                 # +500 bonus
    adjustment_type="Bonus",
    justification="Outstanding performance",
    admin_id="admin001",
    timestamp=datetime.datetime.now()
)

# Apply adjustment
audit_log = apply_adjustment(payroll, adjustment)

# Print results
print("Updated Payroll:")
print(f"Net Pay: {payroll.net_pay}")
print(f"Total Adjustments: {payroll.total_adjustments}")

print("Audit Log:")
print(audit_log)