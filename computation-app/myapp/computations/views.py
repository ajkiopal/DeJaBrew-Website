from django.shortcuts import render
from datetime import datetime
from .payroll_models import PlaceholderEmployee, PlaceholderAttendanceSummary, PayrollAdjustment
from .calculator import generate_payroll
from .adjustments import apply_adjustment

# --- TEMPORARY MEMORY FOR TESTING ---
# This list will act as our fake database and remember adjustments between clicks!
fake_adjustments_db = []
# ------------------------------------

def adjustments_view(request, employee_id=None):
    # 1. Define all employees (placeholder or real)
    employees = [
        PlaceholderEmployee(
            employee_id=1,
            full_name="Juan Dela Cruz",
            employment_type="Barista",
            base_hourly_rate=120.0,
            overtime_hourly_rate=150.0,
            allowances=50.0
        ),
        PlaceholderEmployee(
            employee_id=2,
            full_name="Maria Clara",
            employment_type="Barista",
            base_hourly_rate=130.0,
            overtime_hourly_rate=160.0,
            allowances=60.0
        )
    ]

    # Define placeholder attendance summaries so both employees have data
    attendance_summaries = [
        PlaceholderAttendanceSummary(
            employee_id=1,
            payroll_period_start="2026-02-01",
            payroll_period_end="2026-02-15",
            total_regular_hours=80,
            total_overtime_hours=6,
            total_late_hours=2,
            total_undertime_hours=1
        ),
        PlaceholderAttendanceSummary(
            employee_id=2,
            payroll_period_start="2026-02-01",
            payroll_period_end="2026-02-15",
            total_regular_hours=75,
            total_overtime_hours=2,
            total_late_hours=0,
            total_undertime_hours=0
        )
    ]

    # 2. Determine which employee is selected
    if request.method == "POST":
        # If they submit the form, grab the hidden employee_id from the POST data
        emp_id_str = request.POST.get("employee_id")
        active_id = int(emp_id_str) if emp_id_str else employees[0].employee_id
    else:
        # We now grab the ID directly from the clean URL path!
        active_id = employee_id if employee_id else employees[0].employee_id

    # Find the matching employee and attendance, defaulting to the first one if not found
    selected_employee = next((e for e in employees if e.employee_id == active_id), employees[0])
    selected_attendance = next((a for a in attendance_summaries if a.employee_id == selected_employee.employee_id), attendance_summaries[0])

    # 3. Generate a FRESH base payroll for selected employee
    payroll = generate_payroll(selected_employee, selected_attendance)

    # 4. Process the NEW adjustment if the form was submitted
    audit_log = None
    if request.method == "POST" and "amount" in request.POST:
        amount_str = request.POST.get("amount")
        if amount_str:
            amount = float(amount_str)
            justification = request.POST.get("justification")
            
            adj = PayrollAdjustment(
                adjustment_id=len(fake_adjustments_db) + 1, 
                employee_id=selected_employee.employee_id,
                payroll_period_start=payroll.payroll_period_start,
                payroll_period_end=payroll.payroll_period_end,
                amount=amount,
                adjustment_type="Manual",
                justification=justification,
                admin_id="admin001",
                timestamp=datetime.now()
            )
            
            # Create the audit log message
            audit_log = apply_adjustment(payroll, adj)
            
            # SAVE the adjustment to our temporary memory!
            fake_adjustments_db.append(adj)

    # 5. RE-APPLY ALL PAST ADJUSTMENTS FOR THIS EMPLOYEE
    # We grab all the saved adjustments from our fake DB for the selected employee
    employee_past_adjustments = [a for a in fake_adjustments_db if a.employee_id == selected_employee.employee_id]
    
    # Calculate the total of all adjustments ever made to this person
    total_adj_amount = sum(a.amount for a in employee_past_adjustments)
    
    # Overwrite the fresh payroll with the actual running totals so the HTML shows the correct math!
    payroll.total_adjustments = total_adj_amount
    payroll.net_pay = payroll.gross_pay + total_adj_amount

    return render(request, "computations/adjustments.html", {
        "employees": employees,
        "selected_employee": selected_employee,
        "payroll": payroll,
        "audit_log": audit_log,
        "past_adjustments": employee_past_adjustments # Passing this so we can see the history!
    })