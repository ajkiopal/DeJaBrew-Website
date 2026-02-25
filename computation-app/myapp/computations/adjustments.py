"""
adjustments.py

Handles payroll adjustments:
- Validates admin input
- Applies adjustments to PayrollComputation
- Generates audit logs for each adjustment
"""

from payroll_models import PayrollComputation, PayrollAdjustment, PayrollAuditLog


def apply_adjustment(payroll: PayrollComputation, adjustment: PayrollAdjustment) -> PayrollAuditLog:
    """
    Applies a single adjustment to a PayrollComputation object.

    payroll: PayrollComputation object (current payroll)
    adjustment: PayrollAdjustment object (admin input)
    return: PayrollAuditLog object recording the change
    """

    #Validate adjustment
    if adjustment.amount == 0:
        raise ValueError("Adjustment amount cannot be zero.")
    if not adjustment.justification:
        raise ValueError("Justification is required for adjustment.")

    # Record old payroll values
    old_values = {
        "gross_pay": payroll.gross_pay,
        "net_pay": payroll.net_pay,
        "total_adjustments": payroll.total_adjustments
    }

    #Apply adjustment
    payroll.total_adjustments += adjustment.amount
    payroll.net_pay = payroll.gross_pay + payroll.total_adjustments

    #Record new payroll values
    new_values = {
        "gross_pay": payroll.gross_pay,
        "net_pay": payroll.net_pay,
        "total_adjustments": payroll.total_adjustments
    }

    # Generate audit log
    audit_log = PayrollAuditLog(
        log_id=None,  # To be generated when saving to DB
        employee_id=payroll.employee_id,
        payroll_period_start=payroll.payroll_period_start,
        payroll_period_end=payroll.payroll_period_end,
        admin_id=adjustment.admin_id,
        timestamp=adjustment.timestamp,
        old_values=old_values,
        new_values=new_values,
        justification=adjustment.justification
    )

    return audit_log