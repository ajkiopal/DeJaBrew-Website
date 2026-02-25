from django.shortcuts import render
from datetime import datetime
from .payroll_models import PlaceholderEmployee, PlaceholderAttendanceSummary, PayrollAdjustment
from calculator import generate_payroll
from adjustments import apply_adjustment

def test_payslip_view(request):
    # Create placeholder employee & attendance
    emp = PlaceholderEmployee(
        employee_id=1,
        full_name="Juan Dela Cruz",
        employment_type="Barista",
        base_hourly_rate=120.0,
        overtime_hourly_rate=150.0,
        allowances=50.0
    )
    att = PlaceholderAttendanceSummary(
        employee_id=1,
        payroll_period_start="2026-02-01",
        payroll_period_end="2026-02-15",
        total_regular_hours=80,
        total_overtime_hours=6,
        total_late_hours=2,
        total_undertime_hours=1
    )

    # Generate payroll
    payroll = generate_payroll(emp, att)

    #Apply a sample adjustment
    adj = PayrollAdjustment(
        adjustment_id=1,
        employee_id=1,
        payroll_period_start=att.payroll_period_start,
        payroll_period_end=att.payroll_period_end,
        amount=500,
        adjustment_type="Bonus",
        justification="Outstanding performance",
        admin_id="admin001",
        timestamp=datetime.now()
    )
    audit_log = apply_adjustment(payroll, adj)

    #Pass data to template
    return render(request, 'myapp/payslip.html', {
        'employee_name': emp.full_name,
        'payroll_period_start': payroll.payroll_period_start,
        'payroll_period_end': payroll.payroll_period_end,
        'regular_pay': payroll.regular_pay,
        'overtime_pay': payroll.overtime_pay,
        'late_deduction': payroll.late_deduction,
        'undertime_deduction': payroll.undertime_deduction,
        'gross_pay': payroll.gross_pay,
        'total_adjustments': payroll.total_adjustments,
        'net_pay': payroll.net_pay,
        'adjustments': [audit_log]
    })
