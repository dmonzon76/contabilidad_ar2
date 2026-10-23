from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from fiscal.forms.thirdparty_tax_profile import ThirdPartyTaxProfileForm
from fiscal.models import ThirdPartyTaxProfile


@login_required
def thirdparty_tax_list(request):

    profiles = (
        ThirdPartyTaxProfile.objects
        .select_related("company")
        .order_by("name")
    )

    return render(
        request,
        "fiscal/thirdparty_tax_list.html",
        {
            "profiles": profiles,
        },
    )


@login_required
def thirdparty_tax_create(request):

    active_company_id = request.session.get(
        "active_company_id"
    )

    if not active_company_id:
        return redirect("company:company_select")

    if request.method == "POST":

        form = ThirdPartyTaxProfileForm(
            request.POST
        )

        if form.is_valid():

            profile = form.save(
                commit=False
            )

            profile.company_id = active_company_id

            profile.save()

            return redirect(
                "fiscal:thirdparty_tax_list"
            )

    else:

        form = ThirdPartyTaxProfileForm()

    return render(
        request,
        "fiscal/thirdparty_tax_form.html",
        {
            "form": form,
            "profile": None,
        },
    )


@login_required
def thirdparty_tax_edit(request, pk):

    profile = get_object_or_404(
        ThirdPartyTaxProfile.objects.prefetch_related(
            "rules",
            "rules__regime",
            "rules__regime__jurisdiction",
        ),
        pk=pk,
    )

    if request.method == "POST":

        form = ThirdPartyTaxProfileForm(
            request.POST,
            instance=profile,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "fiscal:thirdparty_tax_edit",
                pk=profile.pk,
            )

    else:

        form = ThirdPartyTaxProfileForm(
            instance=profile,
        )

    rules = (
        profile.rules
        .select_related(
            "regime",
            "regime__jurisdiction",
        )
        .order_by(
            "regime__name"
        )
    )

    return render(
        request,
        "fiscal/thirdparty_tax_form.html",
        {
            "form": form,
            "profile": profile,
            "rules": rules,
        },
    )



@login_required
def thirdparty_tax_detail(request, pk):

    profile = get_object_or_404(
        ThirdPartyTaxProfile.objects.prefetch_related(
            "rules",
            "rules__regime",
            "rules__regime__jurisdiction",
        ),
        pk=pk,
    )

    return render(
        request,
        "fiscal/thirdparty_tax_detail.html",
        {
            "profile": profile,
        },
    )


@login_required
def thirdparty_tax_delete(request, pk):

    active_company_id = request.session.get(
        "active_company_id"
    )

    profile = get_object_or_404(
        ThirdPartyTaxProfile,
        pk=pk,
        company_id=active_company_id,
    )

    if request.method == "POST":

        profile.delete()

        return redirect(
            "fiscal:thirdparty_tax_list"
        )

    return render(
        request,
        "fiscal/thirdparty_tax_confirm_delete.html",
        {
            "profile": profile,
        },
    )