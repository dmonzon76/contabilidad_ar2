from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST, require_http_methods
from django.http import HttpResponseForbidden

from fiscal.models import ElectronicVoucherBook
from fiscal.forms import ElectronicVoucherBookForm

from core.utils.company_active import get_active_company
from core.utils.company_access import user_has_access


@login_required
@permission_required("fiscal.view_electronicvoucherbook", raise_exception=True)
def electronic_voucher_book_list(request):
    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    if not user_has_access(request, company):
        return HttpResponseForbidden("Access denied")

    books = ElectronicVoucherBook.objects.filter(company=company)
    return render(request, 'fiscal/electronic_voucher_book_list.html', {'books': books})


@login_required
@permission_required("fiscal.add_electronicvoucherbook", raise_exception=True)
@require_http_methods(["GET", "POST"])
def electronic_voucher_book_create(request):
    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    if not user_has_access(request, company):
        return HttpResponseForbidden("Access denied")

    if request.method == "POST":
        form = ElectronicVoucherBookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.company = company
            book.save()
            return redirect('fiscal:electronic_voucher_book_list')
    else:
        form = ElectronicVoucherBookForm()

    return render(request, 'fiscal/electronic_voucher_book_form.html', {'form': form})


@login_required
@permission_required("fiscal.change_electronicvoucherbook", raise_exception=True)
@require_http_methods(["GET", "POST"])
def electronic_voucher_book_edit(request, book_id):
    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    if not user_has_access(request, company):
        return HttpResponseForbidden("Access denied")

    book = get_object_or_404(ElectronicVoucherBook, id=book_id, company=company)

    if request.method == "POST":
        form = ElectronicVoucherBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('fiscal:electronic_voucher_book_list')
    else:
        form = ElectronicVoucherBookForm(instance=book)

    return render(request, 'fiscal/electronic_voucher_book_form.html', {'form': form})


@login_required
@permission_required("fiscal.delete_electronicvoucherbook", raise_exception=True)
@require_POST
def electronic_voucher_book_delete(request, book_id):
    company = get_active_company(request)
    if not company:
        return HttpResponseForbidden("No active company")

    if not user_has_access(request, company):
        return HttpResponseForbidden("Access denied")

    book = get_object_or_404(ElectronicVoucherBook, id=book_id, company=company)
    book.delete()
    return redirect('fiscal:electronic_voucher_book_list')
