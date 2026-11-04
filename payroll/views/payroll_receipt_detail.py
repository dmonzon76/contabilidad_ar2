# payroll/views/payroll_receipt_detail.py

from django.views.generic import DetailView

from payroll.models import PayrollReceipt


class PayrollReceiptDetailView(
    DetailView,
):

    model = PayrollReceipt

    template_name = (
        "payroll/payroll_receipt_detail.html"
    )

    context_object_name = "receipt"

    def get_context_data(
        self,
        **kwargs,
    ):

        context = super().get_context_data(
            **kwargs
        )

        receipt = self.object

        remunerative_lines = []
        non_remunerative_lines = []
        deduction_lines = []

        for line in (
            receipt.lines
            .select_related("concept")
            .all()
        ):

            if line.is_remunerative:

                remunerative_lines.append(
                    line
                )

            elif line.is_non_remunerative:

                non_remunerative_lines.append(
                    line
                )

            elif line.is_deduction:

                deduction_lines.append(
                    line
                )

        context[
            "remunerative_lines"
        ] = remunerative_lines

        context[
            "non_remunerative_lines"
        ] = non_remunerative_lines

        context[
            "deduction_lines"
        ] = deduction_lines

        return context