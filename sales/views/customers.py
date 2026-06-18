from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from fiscal.models import ThirdPartyTaxProfile
from sales.models import Customer
from company.middleware import get_active_company

class CustomerListView(ListView):
    model = Customer
    template_name = "sales/customers/list.html"

    def get_queryset(self):
        company = get_active_company(self.request)
        return Customer.objects.filter(company=company, is_active=True)


class CustomerCreateView(CreateView):
    model = Customer
    fields = ["name", "tax_id", "email", "phone", "address"]
    template_name = "sales/customers/form.html"
    success_url = reverse_lazy("sales:customer_list")

    def form_valid(self, form):
        form.instance.company = get_active_company(self.request)
        return super().form_valid(form)

def form_valid(self, form):
    company = get_active_company(self.request)

    # Crear perfil fiscal por defecto
    tax_profile = ThirdPartyTaxProfile.objects.create(
        company=company,
        afip_category="CF",  # Consumidor Final por defecto
    )

    form.instance.company = company
    form.instance.tax_profile = tax_profile

    return super().form_valid(form)


class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ["name", "tax_id", "email", "phone", "address", "is_active"]
    template_name = "sales/customers/form.html"
    success_url = reverse_lazy("sales:customer_list")


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = "sales/customers/delete.html"
    success_url = reverse_lazy("sales:customer_list")
