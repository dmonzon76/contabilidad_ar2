from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from accounting.models import JournalEntry, Period
from accounting.forms import JournalEntryForm, JournalEntryLineFormSet
from company.models import Company


@login_required
def journal_list(request):
    company_id = request.session["active_company_id"]
    company = Company.objects.get(id=company_id)

    entries = JournalEntry.objects.filter(company=company).select_related("period")

    return render(request, "accounting/journal/list.html", {
        "company": company,
        "entries": entries,
    })


@login_required
def journal_create(request):
    company_id = request.session["active_company_id"]
    company = Company.objects.get(id=company_id)

    if request.method == "POST":
        form = JournalEntryForm(request.POST)
        formset = JournalEntryLineFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            entry = form.save(commit=False)
            entry.company = company
            entry.created_by = request.user

            # Buscar período contable que contenga la fecha
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
                lines = formset.save()

                if not entry.is_balanced:
                    # Si no cuadra, borrar y mostrar error
                    entry.delete()
                    raise ValidationError("Journal entry is not balanced (debit != credit).")

                return redirect("journal_list")
    else:
        form = JournalEntryForm()
        formset = JournalEntryLineFormSet()

    return render(request, "accounting/journal/create.html", {
        "company": company,
        "form": form,
        "formset": formset,
    })
