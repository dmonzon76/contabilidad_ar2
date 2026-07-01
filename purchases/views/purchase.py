from decimal import Decimal
from django.http import HttpResponse
from django.template.loader import render_to_string

from purchases.forms.purchase import (
    PurchaseForm,
    PurchaseLineFormSet,
    PurchaseTaxFormSet,
    PurchasePerceptionFormSet,
    PurchaseRetentionFormSet,
)
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from core.middleware.active_company import get_active_company_from_request
from purchases.models.purchase import Purchase
from purchases.forms.purchase import PurchaseForm

def purchase_recalculate(request):
    """
    Vista HTMX que recalcula totales sin guardar la compra.
    """

    form = PurchaseForm(request.POST)
    line_formset = PurchaseLineFormSet(request.POST)
    tax_formset = PurchaseTaxFormSet(request.POST)
    perception_formset = PurchasePerceptionFormSet(request.POST)
    retention_formset = PurchaseRetentionFormSet(request.POST)

    # NETO
    net = Decimal("0")
    for lf in line_formset:
        if lf.is_valid():
            qty = lf.cleaned_data.get("quantity") or Decimal("0")
            price = lf.cleaned_data.get("unit_price") or Decimal("0")
            net += qty * price

    # IVA
    iva = Decimal("0")
    for tf in tax_formset:
        if tf.is_valid():
            base = tf.cleaned_data.get("base_amount") or Decimal("0")
            vat = tf.cleaned_data.get("vat_type")
            if vat == "21":
                iva += base * Decimal("0.21")
            elif vat == "105":
                iva += base * Decimal("0.105")
            elif vat == "27":
                iva += base * Decimal("0.27")

    # PERCEPCIONES
    perceptions = Decimal("0")
    for pf in perception_formset:
        if pf.is_valid():
            perceptions += pf.cleaned_data.get("amount") or Decimal("0")

    # RETENCIONES
    retentions = Decimal("0")
    for rf in retention_formset:
        if rf.is_valid():
            retentions += rf.cleaned_data.get("amount") or Decimal("0")

    # TOTAL
    total = net + iva + perceptions - retentions

    html = render_to_string(
        "purchases/purchases/partials/totals.html",
        {
            "net": net,
            "iva": iva,
            "perceptions": perceptions,
            "retentions": retentions,
            "total": total,
        }
    )

    return HttpResponse(html)








class PurchaseListView(ListView):
    model = Purchase
    template_name = "purchases/purchases/list.html"

    def get_queryset(self):
        company = get_active_company_from_request(self.request)
        return Purchase.objects.filter(company=company, is_active=True)


class PurchaseDetailView(DetailView):
    model = Purchase
    template_name = "purchases/purchases/detail.html"


class PurchaseCreateView(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "purchases/purchases/form.html"
    success_url = reverse_lazy("purchases:purchase_list")

    def form_valid(self, form):
        company = get_active_company_from_request(self.request)
        form.instance.company = company
        return super().form_valid(form)


class PurchaseUpdateView(UpdateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "purchases/purchases/form.html"
    success_url = reverse_lazy("purchases:purchase_list")


class PurchaseDeleteView(DeleteView):
    model = Purchase
    template_name = "purchases/purchases/detail.html"
    success_url = reverse_lazy("purchases:purchase_list")
