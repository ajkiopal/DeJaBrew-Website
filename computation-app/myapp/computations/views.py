from django.shortcuts import render, redirect
from datetime import datetime
from .payroll_models import PlaceholderEmployee, PlaceholderAttendanceSummary, PayrollAdjustment
from .calculator import generate_payroll
from .adjustments import apply_adjustment


# 1. Replace PlaceholderEmployee & PlaceholderAttendanceSummary
#    with actual data from the employee import (Gelo) and attendance import (Fraulene).
#    Example:
#       emp = get_employee(employee_id)
#       att = get_attendance(employee_id, period_start, period_end)
#
# 2. Ensure that generate_payroll() can accept the real models instead of placeholders.
# 3. apply_adjustment() expects a PayrollComputation object and a PayrollAdjustment object.
# 4. The template adjustments.html expects:
#       'employee' -> Employee object
#       'payroll' -> PayrollComputation object
#       'adjustments' -> list of applied adjustments (Audit Logs)


def adjustments_view(request, employee_id=1):
    """
    Displays payroll computation for a given employee and payroll period
    and allows an admin to apply adjustments.
    """

 # placeholders for testing
    emp = PlaceholderEmployee(
        employee_id=employee_id,
        full_name="Juan Dela Cruz",
        employment_type="Barista",
        base_hourly_rate=120.0,
        overtime_hourly_rate=150.0,
        allowances=50.0
    )
    att = PlaceholderAttendanceSummary(
        employee_id=employee_id,
        payroll_period_start="2026-02-01",
        payroll_period_end="2026-02-15",
        total_regular_hours=80,
        total_overtime_hours=6,
        total_late_hours=2,
        total_undertime_hours=1
    )
   # end of placeholders

    # Generate payroll computation
    payroll = generate_payroll(emp, att)

    # Keep a list of adjustments applied (in a real app, fetch from DB)
    adjustments_list = []

    # Handle form submission
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        adjustment_type = request.POST.get("adjustment_type")
        justification = request.POST.get("justification")
        timestamp = datetime.now()

        # Create adjustment object
        adj = PayrollAdjustment(
            adjustment_id=1,  # In real integration, generate unique ID
            employee_id=employee_id,
            payroll_period_start=att.payroll_period_start,
            payroll_period_end=att.payroll_period_end,
            amount=amount,
            adjustment_type=adjustment_type,
            justification=justification,
            admin_id="admin001",  # Replace with logged-in admin ID
            timestamp=timestamp
        )

        # Apply adjustment and get audit log
        audit_log = apply_adjustment(payroll, adj)
        adjustments_list.append(audit_log)

        # After applying, reload the page (POST-Redirect-GET pattern recommended)
        return redirect('adjustments', employee_id=employee_id)

    # Render adjustments page
    return render(request, 'computations/adjustments.html', {
        'employee': emp,
        'payroll': payroll,
        'adjustments': adjustments_list
    })
