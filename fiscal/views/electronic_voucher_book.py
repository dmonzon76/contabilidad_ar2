from django.shortcuts import render, redirect, get_object_or_404
from fiscal.models import ElectronicVoucherBook
from fiscal.forms import ElectronicVoucherBookForm

def electronic_voucher_book_list(request):
    books = ElectronicVoucherBook.objects.all()
    return render(request, 'fiscal/electronic_voucher_book_list.html', {'books': books})

def electronic_voucher_book_create(request):
    if request.method == 'POST':
        form = ElectronicVoucherBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('electronic_voucher_book_list')
    else:
        form = ElectronicVoucherBookForm()
    return render(request, 'fiscal/electronic_voucher_book_form.html', {'form': form})

def electronic_voucher_book_edit(request, book_id):
    book = get_object_or_404(ElectronicVoucherBook, id=book_id)
    if request.method == 'POST':
        form = ElectronicVoucherBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('electronic_voucher_book_list')
    else:
        form = ElectronicVoucherBookForm(instance=book)
    return render(request, 'fiscal/electronic_voucher_book_form.html', {'form': form})

def electronic_voucher_book_delete(request, book_id):
    book = get_object_or_404(ElectronicVoucherBook, id=book_id)
    book.delete()
    return redirect('electronic_voucher_book_list')
