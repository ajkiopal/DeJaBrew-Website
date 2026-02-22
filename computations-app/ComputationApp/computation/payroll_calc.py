from decimal import Decimal

def compute_payroll(hours_worked, hourly_rate, deductions):
    gross_pay = Decimal(hours_worked) * Decimal(hourly_rate)
    net_pay = gross_pay - Decimal(deductions)

    return {
        "gross_pay": gross_pay,
        "net_pay": net_pay
    }
