from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy

from sales.models.sale import Sale
from sales.models.sale_item import SaleItem

from sales.forms.sale import SaleForm
from sales.forms.sale_item import SaleItemForm

from django.shortcuts import get_object_or_404, redirect, render


class SaleListView(ListView):
    model = Sale
    template_name = "sales/sale_list.html"
    context_object_name = "sales"

    def get_queryset(self):
        return Sale.objects.filter(company_id=self.request.session.get("active_company_id"))


class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = "sales/sale_create.html"

    def form_valid(self, form):
        form.instance.company_id = self.request.session.get("active_company_id")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("sales:sale_list")


class SaleDetailView(DetailView):
    model = Sale
    template_name = "sales/sale_detail.html"
    context_object_name = "sale"


def sale_item_add(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)

    if request.method == "POST":
        form = SaleItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.sale = sale
            item.save()

            sale.recalc_totals()

            return redirect("sales:sale_detail", pk=sale.id)
    else:
        form = SaleItemForm()

    return render(request, "sales/sale_item_add.html", {"form": form, "sale": sale})
