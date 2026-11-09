from django.urls import reverse

from django.views.generic import UpdateView

from payroll.models import FamilyMember


class FamilyMemberUpdateView(
    UpdateView
):

    model = FamilyMember

    fields = [
        "first_name",
        "last_name",
        "dni",
        "birth_date",
        "relationship",
        "dependent",
        "disabled",
        "family_allowance_until",
        "notes",
    ]

    template_name = (
        "family/family_member_form.html"
    )

    context_object_name = (
        "family_member"
    )

    def get_success_url(
        self,
    ):

        return reverse(
            "payroll:employee_detail",
            kwargs={
                "pk": self.object.employee.pk,
            },
        )