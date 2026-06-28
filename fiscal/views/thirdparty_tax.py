from django.shortcuts import render, redirect, get_object_or_404
from fiscal.models import ThirdPartyTaxProfile
from fiscal.forms import ThirdPartyTaxProfileForm
from company.models import Company


def thirdparty_tax_list(request):
    profiles = ThirdPartyTaxProfile.objects.select_related("company").order_by("company__name")
    return render(request, "fiscal/thirdparty_tax_list.html", {"profiles": profiles})


def thirdparty_tax_create(request):
    if request.method == "POST":
        form = ThirdPartyTaxProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("thirdparty_tax_list")
    else:
        form = ThirdPartyTaxProfileForm()

    return render(request, "fiscal/thirdparty_tax_form.html", {"form": form})


def thirdparty_tax_edit(request, profile_id):
    profile = get_object_or_404(ThirdPartyTaxProfile, id=profile_id)

    if request.method == "POST":
        form = ThirdPartyTaxProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("thirdparty_tax_list")
    else:
        form = ThirdPartyTaxProfileForm(instance=profile)

    return render(request, "fiscal/thirdparty_tax_form.html", {"form": form})


def thirdparty_tax_delete(request, profile_id):
    profile = get_object_or_404(ThirdPartyTaxProfile, id=profile_id)
    profile.delete()
    return redirect("thirdparty_tax_list")
