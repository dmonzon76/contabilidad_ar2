from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from fiscal.models import FiscalService
from fiscal.forms import FiscalServiceForm


@login_required
def fiscal_service_list(request):
    services = FiscalService.objects.all().order_by("name")
    return render(request, "fiscal/fiscal_service_list.html", {
        "services": services,
    })


@login_required
def fiscal_service_create(request):
    if request.method == "POST":
        form = FiscalServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("fiscal:fiscal_service_list")
    else:
        form = FiscalServiceForm()

    return render(request, "fiscal/fiscal_service_form.html", {
        "form": form,
        "mode": "create",
    })


@login_required
def fiscal_service_edit(request, pk):
    service = get_object_or_404(FiscalService, pk=pk)

    if request.method == "POST":
        form = FiscalServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect("fiscal:fiscal_service_list")
    else:
        form = FiscalServiceForm(instance=service)

    return render(request, "fiscal/fiscal_service_form.html", {
        "form": form,
        "mode": "edit",
        "service": service,
    })
