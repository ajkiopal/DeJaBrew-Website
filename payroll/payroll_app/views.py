from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from .models import PayPeriod, PayrollRun


@login_required
def payroll_run_create_page(request):
    periods = PayPeriod.objects.filter(status="OPEN").order_by("-start_date")

    if request.method == "POST":
        period_id = request.POST.get("period_id")
        if not period_id:
            messages.error(request, "Select a pay period.")
            return redirect("payroll_run_create")

        period = get_object_or_404(PayPeriod, pk=period_id)

        if period.status != "OPEN":
            messages.error(request, "This pay period is closed.")
            return redirect("payroll_run_create")

        try:
            with transaction.atomic():
                run = PayrollRun.objects.create(
                    period=period,
                    status="RUNNING",
                    created_by=request.user,
                )

                # Placeholder: Luiis will generate payslips here later.
                # For now, we immediately mark it completed to prove the flow works.
                run.status = "COMPLETED"
                run.completed_at = timezone.now()
                run.save()

            messages.success(request, f"Payroll run created for period {period.start_date} to {period.end_date}.")
            return redirect("payroll_run_detail", run_id=run.id)

        except IntegrityError:
            messages.error(request, "A payroll run already exists for that period.")
            return redirect("payroll_run_create")

    return render(request, "payroll_app/payroll_run_create.html", {"periods": periods})


@login_required
def payroll_run_detail(request, run_id):
    run = get_object_or_404(PayrollRun, pk=run_id)
    return render(request, "payroll_app/payroll_run_detail.html", {"run": run})


@login_required
def pay_period_list_create(request):
    periods = PayPeriod.objects.all().order_by("-start_date")

    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        label = request.POST.get("label", "")
        status = request.POST.get("status", "OPEN")

        period = PayPeriod(
            start_date=start_date,
            end_date=end_date,
            label=label,
            status=status,
        )

        try:
            period.full_clean()  # runs your clean() overlap checks
            period.save()
            messages.success(request, "Pay period created.")
            return redirect("pay_periods")
        except ValidationError as e:
            messages.error(request, " ".join(e.messages))

    return render(request, "payroll_app/pay_periods.html", {"periods": periods})


@login_required
def pay_period_close(request, period_id):
    if request.method != "POST":
        return redirect("pay_periods")

    period = get_object_or_404(PayPeriod, pk=period_id)
    period.status = "CLOSED"
    period.save()
    messages.success(request, "Pay period closed.")
    return redirect("pay_periods")