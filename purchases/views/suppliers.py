from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from sales.models import Supplier
from company.middleware import get_active_company

class SupplierListView(ListView):
    model = Supplier
    template_name = "purchases/suppliers/list.html"

    def get_queryset(self):
        company = get_active_company(self.request)
        return Supplier.objects.filter(company=company, is_active=True)


class SupplierCreateView(CreateView):
    model = Supplier
    fields = ["name", "tax_id", "email", "phone", "address"]
    template_name = "purchases/suppliers/form.html"
    success_url = reverse_lazy("purchases:supplier_list")

    def form_valid(self, form):
        form.instance.company = get_active_company(self.request)
        return super().form_valid(form)


class SupplierUpdateView(UpdateView):
    model = Supplier
    fields = ["name", "tax_id", "email", "phone", "address", "is_active"]
    template_name = "purchases/suppliers/form.html"
    success_url = reverse_lazy("purchases:supplier_list")


class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = "purchases/suppliers/delete.html"
    success_url = reverse_lazy("purchases:supplier_list")
