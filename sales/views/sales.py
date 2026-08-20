from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy

from sales.models.sale import Sale
from sales.models.sale_item import SaleItem

from sales.forms.sale import SaleForm
from sales.forms.sale_item import SaleItemForm

from django.shortcuts import get_object_or_404, redirect, render
from inventory.integration import update_inventory_from_sale

class SaleListView(ListView):
    model = Sale
    template_name = "sales/sale_list.html"
    context_object_name = "sales"

    def get_queryset(self):
        return Sale.objects.filter(
            company_id=self.request.session.get("active_company_id")
        )


class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = "sales/sale_create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["company_id"] = self.request.session.get("active_company_id")
        return kwargs

    def form_valid(self, form):
        form.instance.company_id = self.request.session.get("active_company_id")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("sales:sale_list")


class SaleDetailView(DetailView):
    model = Sale
    template_name = "sales/sale_detail.html"
    context_object_name = "sale"

    def get_queryset(self):
        return Sale.objects.filter(
            company_id=self.request.session.get("active_company_id")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sale = context["sale"]

        # Nueva integración fiscal moderna:
        # Si existe factura fiscal, se agrega al contexto
        fiscal_invoice = getattr(sale, "fiscal_invoice", None)
        context["fiscal_invoice"] = fiscal_invoice

        return context

def sale_item_add(request, sale_id):
    sale = get_object_or_404(
        Sale,
        id=sale_id,
        company_id=request.session.get("active_company_id"),
    )

    if request.method == "POST":
        form = SaleItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.sale = sale
            item.save()

            # Actualizar totales
            sale.recalc_totals()

            # INTEGRACIÓN INVENTORY (SALIDAS DE STOCK)
            from inventory.integration import update_inventory_from_sale
            update_inventory_from_sale(sale)

            return redirect("sales:sale_detail", pk=sale.id)
    else:
        form = SaleItemForm()

    return render(request, "sales/sale_item_add.html", {"form": form, "sale": sale})



















def sale_create(request):
    ...
    sale.recalc_totals()
    update_inventory_from_sale(sale)
    ...
