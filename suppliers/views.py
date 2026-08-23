# suppliers/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from suppliers.models import Supplier
from suppliers.forms.supplier import SupplierForm


@login_required
def supplier_list(request):
    """Lista de proveedores de la empresa activa."""
    company_id = request.session.get("active_company_id")
    suppliers = Supplier.objects.filter(company_id=company_id).order_by("name")
    return render(request, "suppliers/supplier_list.html", {"suppliers": suppliers})


@login_required
def supplier_detail(request, pk):
    """Detalle de un proveedor."""
    company_id = request.session.get("active_company_id")
    supplier = get_object_or_404(Supplier, pk=pk, company_id=company_id)
    return render(request, "suppliers/supplier_detail.html", {"supplier": supplier})


@login_required
def supplier_add(request):
    """Crear un nuevo proveedor. Usa supplier_form.html con mode='add'."""
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.company_id = request.session.get("active_company_id")
            s.save()
            messages.success(request, "Supplier created")
            return redirect("suppliers:supplier_detail", s.pk)
    else:
        form = SupplierForm()
    return render(request, "suppliers/supplier_form.html", {"form": form, "mode": "add"})


@login_required
def supplier_edit(request, pk):
    """Editar proveedor existente. Usa supplier_form.html con mode='edit'."""
    company_id = request.session.get("active_company_id")
    supplier = get_object_or_404(Supplier, pk=pk, company_id=company_id)

    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier updated")
            return redirect("suppliers:supplier_detail", supplier.pk)
    else:
        form = SupplierForm(instance=supplier)

    context = {
        "form": form,
        "mode": "edit",
        "supplier": supplier,  # usado por el template para mostrar Delete o datos
    }
    return render(request, "suppliers/supplier_form.html", context)


@login_required
def supplier_delete(request, pk):
    """Confirmación y borrado de proveedor. Usa supplier_confirm_delete.html."""
    company_id = request.session.get("active_company_id")
    supplier = get_object_or_404(Supplier, pk=pk, company_id=company_id)

    if request.method == "POST":
        supplier.delete()
        messages.success(request, "Supplier deleted")
        return redirect("suppliers:supplier_list")

    return render(request, "suppliers/supplier_confirm_delete.html", {"supplier": supplier})


@login_required
def supplier_autocomplete(request):
    """
    Endpoint JSON para autocompletar proveedores.
    Parámetro GET: q
    Respuesta: {"results": [{"id": pk, "text": name, "tax_id": "...", "email": "..."}]}
    """
    q = request.GET.get("q", "").strip()
    company_id = request.session.get("active_company_id")
    qs = Supplier.objects.filter(company_id=company_id, name__icontains=q).order_by("name")[:10]
    results = [
        {"id": s.pk, "text": s.name, "tax_id": s.tax_id or "", "email": s.email or ""}
        for s in qs
    ]
    return JsonResponse({"results": results})
