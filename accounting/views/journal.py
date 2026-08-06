from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from accounting.models import JournalEntry, Period
from accounting.forms import JournalEntryForm, JournalEntryLineFormSet
from core.utils.company_access import user_has_access


@login_required
def journal_list(request):
    company = request.active_company

    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    entries = (
        JournalEntry.objects
        .filter(company=company)
        .select_related("period")
        .order_by("-date", "-id")
    )

    return render(request, "accounting/journal/list.html", {
        "company": company,
        "entries": entries,
    })


@login_required
def journal_create(request):
    company = request.active_company

    if not company or not user_has_access(request, company):
        return render(request, "errors/403.html", status=403)

    if request.method == "POST":
        form = JournalEntryForm(request.POST)
        formset = JournalEntryLineFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            entry = form.save(commit=False)
            entry.company = company
            entry.created_by = request.user

            period = Period.objects.filter(
                company=company,
                start_date__lte=entry.date,
                end_date__gte=entry.date,
                status="OPEN",
            ).first()

            if not period:
                form.add_error("date", "No open accounting period covers this date.")
            else:
                entry.period = period
                entry.save()
                formset.instance = entry
                formset.save()

                if not entry.is_balanced:
                    entry.delete()
                    raise ValidationError("Journal entry is not balanced (debit != credit).")

                return redirect("accounting:journal_list")
    else:
        form = JournalEntryForm()
        formset = JournalEntryLineFormSet()

    return render(request, "accounting/journal/create.html", {
        "company": company,
        "form": form,
        "formset": formset,
    })
