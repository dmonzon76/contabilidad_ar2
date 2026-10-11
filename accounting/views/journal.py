from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from accounting.forms import (
    JournalEntryForm,
    JournalEntryLineFormSet,
)
from accounting.models import (
    JournalEntry,
    Period,
)
from core.utils.company_access import user_has_access


@login_required
def journal_list(request):
    company = request.active_company

    if not company or not user_has_access(request, company):
        return render(
            request,
            "errors/403.html",
            status=403,
        )

    entries = (
        JournalEntry.objects
        .filter(company=company)
        .select_related("period")
        .order_by("-date", "-id")
    )

    return render(
        request,
        "accounting/journal/list.html",
        {
            "company": company,
            "entries": entries,
        },
    )


@login_required
def journal_create(request):
    company = request.active_company

    if not company or not user_has_access(request, company):
        return render(
            request,
            "errors/403.html",
            status=403,
        )

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
                form.add_error(
                    "date",
                    "No open accounting period covers this date.",
                )
            else:
                entry.period = period
                entry.save()

                formset.instance = entry
                formset.save()

                if not entry.is_balanced:
                    entry.delete()
                    raise ValidationError(
                        "Journal entry is not balanced (debit != credit)."
                    )

                return redirect(
                    "accounting:journal_list"
                )

    else:
        form = JournalEntryForm()
        formset = JournalEntryLineFormSet()

    return render(
        request,
        "accounting/journal/create.html",
        {
            "company": company,
            "form": form,
            "formset": formset,
        },
    )

@login_required
def journal_detail(request, entry_id):
    company = request.active_company

    if not company or not user_has_access(request, company):
        return render(
            request,
            "errors/403.html",
            status=403,
        )

    entry = get_object_or_404(
        JournalEntry.objects.select_related(
            "period",
            "created_by",
        ).prefetch_related(
            "lines",
            "lines__account",
        ),
        pk=entry_id,
        company=company,
    )

    return render(
        request,
        "accounting/journal/journal_detail.html",
        {
            "company": company,
            "entry": entry,
        },
    )

@login_required
def journal_edit(request, entry_id):
    company = request.active_company

    if not company or not user_has_access(request, company):
        return render(
            request,
            "errors/403.html",
            status=403,
        )

    entry = get_object_or_404(
        JournalEntry,
        pk=entry_id,
        company=company,
    )

    # No permitir editar asientos generados desde compras
    if entry.purchase_id:
        return render(
            request,
            "errors/403.html",
            {
                "message": (
                    "This journal entry was generated automatically "
                    "from a purchase and cannot be edited."
                )
            },
            status=403,
        )

    # No permitir modificaciones en períodos bloqueados
    if entry.period.is_locked:
        return render(
            request,
            "errors/403.html",
            {
                "message": (
                    "This accounting period is locked."
                )
            },
            status=403,
        )

    if request.method == "POST":
        form = JournalEntryForm(
            request.POST,
            instance=entry,
        )

        formset = JournalEntryLineFormSet(
            request.POST,
            instance=entry,
        )

        if form.is_valid() and formset.is_valid():

            entry = form.save()

            formset.instance = entry
            formset.save()

            if not entry.is_balanced:
                form.add_error(
                    None,
                    "Journal entry is not balanced."
                )
            else:
                return redirect(
                    "accounting:journal_list"
                )

    else:
        form = JournalEntryForm(
            instance=entry,
        )

        formset = JournalEntryLineFormSet(
            instance=entry,
        )

    return render(
        request,
        "accounting/journal/edit.html",
        {
            "company": company,
            "entry": entry,
            "form": form,
            "formset": formset,
        },
    )