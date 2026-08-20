from decimal import Decimal
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from core.middleware.active_company import get_active_company_from_request

from purchases.models.purchase import Purchase
from purchases.forms.purchase import (
    PurchaseForm,
    PurchaseLineFormSet,
    PurchaseTaxFormSet,
    PurchasePerceptionFormSet,
    PurchaseRetentionFormSet,
)


# ---------------------------------------------------------
# HTMX: Recalcular totales sin guardar
# ---------------------------------------------------------
def purchase_recalculate(request):
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
        },
    )

    return HttpResponse(html)


# ---------------------------------------------------------
# LIST / DETAIL
# ---------------------------------------------------------
class PurchaseListView(ListView):
    model = Purchase
    template_name = "purchases/purchases/list.html"

    def get_queryset(self):
        company = get_active_company_from_request(self.request)
        return Purchase.objects.filter(company=company, is_active=True)


class PurchaseDetailView(DetailView):
    model = Purchase
    template_name = "purchases/purchases/detail.html"

    def get_queryset(self):
        company = get_active_company_from_request(self.request)
        return Purchase.objects.filter(company=company, is_active=True)


# ---------------------------------------------------------
# CREATE (CON FORMSETS)
# ---------------------------------------------------------
class PurchaseCreateView(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "purchases/purchases/form.html"
    success_url = reverse_lazy("purchases:purchase_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        company = get_active_company_from_request(self.request)
        kwargs["company_id"] = company.id if company else None
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["line_formset"] = PurchaseLineFormSet(self.request.POST)
            context["tax_formset"] = PurchaseTaxFormSet(self.request.POST)
            context["perception_formset"] = PurchasePerceptionFormSet(self.request.POST)
            context["retention_formset"] = PurchaseRetentionFormSet(self.request.POST)
        else:
            context["line_formset"] = PurchaseLineFormSet()
            context["tax_formset"] = PurchaseTaxFormSet()
            context["perception_formset"] = PurchasePerceptionFormSet()
            context["retention_formset"] = PurchaseRetentionFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        line_formset = context["line_formset"]
        tax_formset = context["tax_formset"]
        perception_formset = context["perception_formset"]
        retention_formset = context["retention_formset"]

        if (
            line_formset.is_valid()
            and tax_formset.is_valid()
            and perception_formset.is_valid()
            and retention_formset.is_valid()
        ):
            company = get_active_company_from_request(self.request)
            form.instance.company = company
            self.object = form.save()

            line_formset.instance = self.object
            tax_formset.instance = self.object
            perception_formset.instance = self.object
            retention_formset.instance = self.object

            line_formset.save()
            tax_formset.save()
            perception_formset.save()
            retention_formset.save()

            return super().form_valid(form)

        return self.form_invalid(form)


# ---------------------------------------------------------
# UPDATE (CON FORMSETS)
# ---------------------------------------------------------
class PurchaseUpdateView(UpdateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "purchases/purchases/form.html"
    success_url = reverse_lazy("purchases:purchase_list")

    def get_queryset(self):
        company = get_active_company_from_request(self.request)
        return Purchase.objects.filter(company=company, is_active=True)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        company = get_active_company_from_request(self.request)
        kwargs["company_id"] = company.id if company else None
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["line_formset"] = PurchaseLineFormSet(
                self.request.POST, instance=self.object
            )
            context["tax_formset"] = PurchaseTaxFormSet(
                self.request.POST, instance=self.object
            )
            context["perception_formset"] = PurchasePerceptionFormSet(
                self.request.POST, instance=self.object
            )
            context["retention_formset"] = PurchaseRetentionFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["line_formset"] = PurchaseLineFormSet(instance=self.object)
            context["tax_formset"] = PurchaseTaxFormSet(instance=self.object)
            context["perception_formset"] = PurchasePerceptionFormSet(
                instance=self.object
            )
            context["retention_formset"] = PurchaseRetentionFormSet(
                instance=self.object
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        line_formset = context["line_formset"]
        tax_formset = context["tax_formset"]
        perception_formset = context["perception_formset"]
        retention_formset = context["retention_formset"]

        if (
            line_formset.is_valid()
            and tax_formset.is_valid()
            and perception_formset.is_valid()
            and retention_formset.is_valid()
        ):
            self.object = form.save()

            line_formset.instance = self.object
            tax_formset.instance = self.object
            perception_formset.instance = self.object
            retention_formset.instance = self.object

            line_formset.save()
            tax_formset.save()
            perception_formset.save()
            retention_formset.save()

            return super().form_valid(form)

        return self.form_invalid(form)


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------
class PurchaseDeleteView(DeleteView):
    model = Purchase
    template_name = "purchases/purchases/detail.html"
    success_url = reverse_lazy("purchases:purchase_list")

    def get_queryset(self):
        company = get_active_company_from_request(self.request)
        return Purchase.objects.filter(company=company, is_active=True)
