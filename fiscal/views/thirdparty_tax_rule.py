from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

import fiscal.models
from fiscal.forms.thirdparty_tax_rule import (
    ThirdPartyTaxRuleForm,
)
from fiscal.models import (
    ThirdPartyTaxProfile,
    ThirdPartyTaxRule,
)


@login_required
def thirdparty_tax_rule_list(request):

    rules = (
        ThirdPartyTaxRule.objects
        .select_related(
            "tax_profile",
            "regime",
            "regime__jurisdiction",
        )
        .order_by(
            "tax_profile__name",
            "regime__name",
        )
    )

    return render(
        request,
        "fiscal/thirdparty_tax_rule_list.html",
        {
            "rules": rules,
        },
    )


@login_required
def thirdparty_tax_rule_create(
    request,
    profile_id,
):

    profile = get_object_or_404(
        ThirdPartyTaxProfile,
        pk=profile_id,
    )

    if request.method == "POST":

        form = ThirdPartyTaxRuleForm(
            request.POST
        )

        if form.is_valid():

            rule = form.save(
                commit=False
            )

            rule.tax_profile = profile

            rule.save()

            return redirect(
                "fiscal:thirdparty_tax_edit",
                pk=profile.pk,
            )

    else:

        form = ThirdPartyTaxRuleForm()

    return render(
        request,
        "fiscal/thirdparty_tax_rule_form.html",
        {
            "form": form,
            "profile": profile,
        },
    )

@login_required
def thirdparty_tax_rule_edit(request, pk):

    rule = get_object_or_404(
        ThirdPartyTaxRule,
        pk=pk,
    )

    if request.method == "POST":

        form = ThirdPartyTaxRuleForm(
            request.POST,
            instance=rule,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "fiscal:thirdparty_tax_rule_list"
            )

    else:

        form = ThirdPartyTaxRuleForm(
            instance=rule,
        )

    return render(
        request,
        "fiscal/thirdparty_tax_rule_form.html",
        {
            "form": form,
            "rule": rule,
        },
    )


@login_required
def thirdparty_tax_rule_delete(request, pk):

    rule = get_object_or_404(
        ThirdPartyTaxRule,
        pk=pk,
    )

    if request.method == "POST":

        rule.delete()

        return redirect(
            "fiscal:thirdparty_tax_rule_list"
        )

    return render(
        request,
        "fiscal/thirdparty_tax_rule_confirm_delete.html",
        {
            "rule": rule,
        },
    )