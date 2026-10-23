from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from fiscal.forms.tax_regime import TaxRegimeForm
from fiscal.models import TaxRegime

@login_required
def tax_regime_list(request):

    regimes = (
        TaxRegime.objects
        .select_related(
            "tax",
            "jurisdiction",
        )
        .order_by(
            "tax_type",
            "application_type",
            "name",
        )
    )

    return render(
        request,
        "fiscal/tax_regime_list.html",
        {
            "regimes": regimes,
        },
    )

@login_required
def tax_regime_create(request):

    if request.method == "POST":

        form = TaxRegimeForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                "fiscal:tax_regime_list"
            )

    else:

        form = TaxRegimeForm()

    return render(
        request,
        "fiscal/tax_regime_form.html",
        {
            "form": form,
            "regime": None,
        },
    )
@login_required
def tax_regime_edit(request, pk):

    regime = get_object_or_404(
        TaxRegime,
        pk=pk,
    )

    if request.method == "POST":

        form = TaxRegimeForm(
            request.POST,
            instance=regime,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "fiscal:tax_regime_list"
            )

    else:

        form = TaxRegimeForm(
            instance=regime,
        )

    return render(
        request,
        "fiscal/tax_regime_form.html",
        {
            "form": form,
            "regime": regime,
        },
    )

@login_required
def tax_regime_delete(request, pk):

    regime = get_object_or_404(
        TaxRegime,
        pk=pk,
    )

    if request.method == "POST":

        regime.delete()

        return redirect(
            "fiscal:tax_regime_list"
        )

    return render(
        request,
        "fiscal/tax_regime_confirm_delete.html",
        {
            "regime": regime,
        },
    )