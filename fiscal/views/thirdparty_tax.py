from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from fiscal.models.thirdparty_tax import ThirdPartyTaxProfile
from fiscal.forms.thirdparty_tax_profile import ThirdPartyTaxProfileForm


@login_required
def thirdparty_tax_list(request):
    profiles = ThirdPartyTaxProfile.objects.select_related("customer", "company").order_by("customer__name")

    return render(request, "fiscal/thirdparty_tax_list.html", {
        "profiles": profiles,
    })


@login_required
def thirdparty_tax_edit(request, pk):
    profile = get_object_or_404(ThirdPartyTaxProfile, pk=pk)

    if request.method == "POST":
        form = ThirdPartyTaxProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("fiscal:thirdparty_tax_list")
    else:
        form = ThirdPartyTaxProfileForm(instance=profile)

    return render(request, "fiscal/thirdparty_tax_form.html", {
        "form": form,
        "profile": profile,
        "customer": profile.customer,
    })
