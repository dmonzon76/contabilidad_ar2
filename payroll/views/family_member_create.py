from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView

from payroll.models import (
    Employee,
    FamilyMember,
)


class FamilyMemberCreateView(CreateView):

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

    def dispatch(
        self,
        request,
        *args,
        **kwargs,
    ):

        self.employee = get_object_or_404(
            Employee,
            pk=self.kwargs["employee_id"],
        )

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )

    def form_valid(
        self,
        form,
    ):

        form.instance.employee = (
            self.employee
        )

        return super().form_valid(
            form
        )

    def get_success_url(
        self,
    ):

        return reverse(
            "payroll:employee_detail",
            kwargs={
                "pk": self.employee.pk,
            },
        )