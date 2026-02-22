from decimal import Decimal

def compute_payroll(hours_worked, hourly_rate, deductions):
    gross_pay = Decimal(hours_worked) * Decimal(hourly_rate)
    net_pay = gross_pay - Decimal(deductions)

    return {
        "gross_pay": gross_pay,
        "net_pay": net_pay
    }

def apply_adjustment(payroll_record, bonus=0, deduction=0):
    bonus = Decimal(bonus)
    deduction = Decimal(deduction)

    new_gross = payroll_record.gross_pay + bonus
    new_deductions = payroll_record.deductions + deduction
    new_net = new_gross - new_deductions

    return {
        "adjusted_gross": new_gross,
        "adjusted_deductions": new_deductions,
        "adjusted_net": new_net
    }