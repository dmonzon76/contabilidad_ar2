from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy

from purchases.models.purchase import Purchase
from purchases.forms.purchase import PurchaseForm

from inventory.integration import (
    update_inventory_from_purchase,
    revert_inventory_from_purchase
)

from accounting.integration import (
    create_purchase_journal_entry,
    delete_journal_entries_for_purchase,
    create_supplier_cc_from_purchase,
    delete_supplier_cc_from_purchase
)


# ============================================================
# LISTA DE COMPRAS
# ============================================================

class PurchaseListView(ListView):
    model = Purchase
    template_name = "purchases/purchases/list.html"
    context_object_name = "purchases"

    def get_queryset(self):
        return Purchase.objects.filter(
            company_id=self.request.session.get("active_company_id")
        )


# ============================================================
# DETALLE DE COMPRA (ALIMENTA purchase_detail.html)
# ============================================================

class PurchaseDetailView(DetailView):
    model = Purchase
    template_name = "purchases/purchases/detail.html"
    context_object_name = "purchase"

    def get_queryset(self):
        return Purchase.objects.filter(
            company_id=self.request.session.get("active_company_id")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase = context["purchase"]

        # Líneas de compra
        context["lines"] = purchase.lines.all()

        # Movimientos de inventario asociados
        context["inventory_movements"] = purchase.inventory_movements.all()

        # Asientos contables asociados
        context["journal_entries"] = purchase.journal_entries.all()

        # Movimientos de cuenta corriente proveedor
        context["cc_movements"] = purchase.accountmovement_set.all()

        return context


# ============================================================
# CREAR COMPRA
# ============================================================

class PurchaseCreateView(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "purchases/purchases/form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["company_id"] = self.request.session.get("active_company_id")
        return kwargs

    def form_valid(self, form):
        form.instance.company_id = self.request.session.get("active_company_id")
        purchase = form.save()

        # Integraciones automáticas
        update_inventory_from_purchase(purchase)
        create_purchase_journal_entry(purchase)
        create_supplier_cc_from_purchase(purchase)

        return redirect("purchases:purchase_list")


# ============================================================
# EDITAR COMPRA
# ============================================================

class PurchaseUpdateView(UpdateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "purchases/purchases/form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["company_id"] = self.request.session.get("active_company_id")
        return kwargs

    def get_success_url(self):
        return reverse_lazy("purchases:purchase_detail", kwargs={"pk": self.object.pk})


# ============================================================
# ELIMINAR COMPRA (REVERSIÓN COMPLETA)
# ============================================================

class PurchaseDeleteView(DetailView):
    model = Purchase
    template_name = "purchases/purchases/delete.html"

    def post(self, request, *args, **kwargs):
        purchase = self.get_object()

        # Reversión contable
        delete_journal_entries_for_purchase(purchase)

        # Reversión cuenta corriente proveedor
        delete_supplier_cc_from_purchase(purchase)

        # Reversión inventario
        revert_inventory_from_purchase(purchase)

        purchase.delete()

        return redirect("purchases:purchase_list")


# ============================================================
# RECALCULAR COMPRA (si lo usás)
# ============================================================

def purchase_recalculate(request):
    # Si tenés lógica de recálculo, va aquí
    return redirect("purchases:purchase_list")
