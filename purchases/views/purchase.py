from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

import inventory.integration
from accounting.integration import delete_journal_entries_for_purchase, delete_supplier_cc_from_purchase
from accounting.models import JournalEntry
from accounting.services import AccountingService

# VALIDACIÓN CONTABLE
from accounting.utils.period_validation import (
    NoOpenPeriodError,
    get_open_period_for_date,
)
from purchases.forms.purchase import (
    PurchaseForm,
    PurchaseLineFormSet,
    PurchasePerceptionFormSet,
    PurchaseRetentionFormSet,
    PurchaseTaxFormSet,
)
from purchases.models.purchase import Purchase

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
# DETALLE DE COMPRA
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

        context["lines"] = purchase.lines.all()
        context["inventory_movements"] = purchase.inventory_movements.all()
        context["journal_entries"] = purchase.journal_entries.all()
        context["cc_movements"] = purchase.accountmovement_set.all()

        return context


# ============================================================
# CREAR COMPRA (FUNCIÓN)
# ============================================================


def purchase_create(request):
    if request.method == "POST":
        form = PurchaseForm(request.POST)

        if form.is_valid():
            purchase = form.save(commit=False)

            # VALIDACIÓN CONTABLE
            try:
                period = get_open_period_for_date(purchase.date)
                purchase.period = period
            except NoOpenPeriodError as e:
                form.add_error(None, str(e))
                return render(request, "purchases/purchase_form.html", {"form": form})

            purchase.save()
            return redirect("purchases:purchase_list")

    else:
        form = PurchaseForm()

    return render(request, "purchases/purchase_form.html", {"form": form})


# ============================================================
# CREAR COMPRA (CLASS-BASED VIEW)
# ============================================================


class PurchaseCreateView(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "purchases/purchases/form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["company_id"] = self.request.session.get("active_company_id")
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase = self.object or Purchase(
            company_id=self.request.session.get("active_company_id")
        )
        for name, formset in self._get_formsets(purchase).items():
            context.setdefault(name, formset)
        return context

    def _get_formsets(self, purchase):
        data = self.request.POST if self.request.method == "POST" else None
        company_id = self.request.session.get("active_company_id")

        return {
            "line_formset": PurchaseLineFormSet(
                data=data,
                instance=purchase,
                form_kwargs={"company_id": company_id},
            ),
            "tax_formset": PurchaseTaxFormSet(
                data=data,
                instance=purchase,
                form_kwargs={"company_id": company_id},
            ),
            "perception_formset": PurchasePerceptionFormSet(data=data, instance=purchase),
            "retention_formset": PurchaseRetentionFormSet(data=data, instance=purchase),
        }

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()

        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.company_id = request.session.get("active_company_id")

            try:
                get_open_period_for_date(purchase.date)
            except NoOpenPeriodError as e:
                form.add_error(None, str(e))
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        **self._get_formsets(purchase),
                    )
                )

            formsets = self._get_formsets(purchase)
            formset_labels = {
                "line_formset": "renglones de la compra",
                "tax_formset": "impuestos",
                "perception_formset": "percepciones",
                "retention_formset": "retenciones",
            }
            formsets_valid = {
                name: formset.is_valid()
                for name, formset in formsets.items()
            }
            if all(formsets_valid.values()):
                with transaction.atomic():
                    purchase.save()
                    for formset in formsets.values():
                        formset.instance = purchase
                        formset.save()
                    purchase.calculate_totals()
                    AccountingService.post_purchase(purchase)

                self.object = purchase
                inventory.integration.update_inventory_from_purchase(purchase)
                return redirect("purchases:purchase_list")

            invalid_sections = [
                formset_labels[name]
                for name, is_valid in formsets_valid.items()
                if not is_valid
            ]
            form.add_error(
                None,
                "No se pudo guardar la compra. Revisá los errores en: "
                + ", ".join(invalid_sections)
                + ".",
            )
            return self.render_to_response(
                self.get_context_data(form=form, **formsets)
            )

        return self.render_to_response(
            self.get_context_data(
                form=form,
                **self._get_formsets(form.instance),
            )
        )

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._get_formsets(self.object))
        return context

    def _get_formsets(self, purchase):
        data = self.request.POST if self.request.method == "POST" else None
        company_id = self.request.session.get("active_company_id")
        return {
            "line_formset": PurchaseLineFormSet(
                data=data,
                instance=purchase,
                form_kwargs={"company_id": company_id},
            ),
            "tax_formset": PurchaseTaxFormSet(
                data=data,
                instance=purchase,
                form_kwargs={"company_id": company_id},
            ),
            "perception_formset": PurchasePerceptionFormSet(data=data, instance=purchase),
            "retention_formset": PurchaseRetentionFormSet(data=data, instance=purchase),
        }

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        purchase = form.instance

        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.company_id = request.session.get("active_company_id")
            purchase.supplier = form.cleaned_data["supplier"]

            # VALIDACIÓN CONTABLE
            try:
                period = get_open_period_for_date(purchase.date)
                purchase.period = period
            except NoOpenPeriodError as e:
                form.add_error(None, str(e))
                return self.render_to_response(
                    self.get_context_data(form=form, **self._get_formsets(purchase))
                )

            formsets = self._get_formsets(purchase)

            if all(formset.is_valid() for formset in formsets.values()):
                with transaction.atomic():
                    purchase.save()
                    for formset in formsets.values():
                        formset.instance = purchase
                        formset.save()
                    purchase.calculate_totals()

                self.object = purchase
                return redirect(self.get_success_url())

        return self.render_to_response(
            self.get_context_data(form=form, **self._get_formsets(purchase))
        )

    def get_success_url(self):
        return reverse_lazy("purchases:purchase_detail", kwargs={"pk": self.object.pk})


# ============================================================
# ELIMINAR COMPRA
# ============================================================


class PurchaseDeleteView(DetailView):
    model = Purchase
    template_name = "purchases/purchases/delete.html"

    def post(self, request, *args, **kwargs):
        purchase = self.get_object()
        JournalEntry.objects.filter(purchase=purchase).delete()
        inventory.integration.revert_inventory_from_purchase(purchase)

        delete_journal_entries_for_purchase(purchase)
        delete_supplier_cc_from_purchase(purchase)
        inventory.integration.revert_inventory_from_purchase(purchase)

        purchase.delete()

        return redirect("purchases:purchase_list")


# ============================================================
# RECALCULAR COMPRA
# ============================================================


def purchase_recalculate(request):
    return redirect("purchases:purchase_list")
