from django import forms

from accounting.models import FiscalYear


class FiscalYearForm(forms.ModelForm):
    def __init__(self, *args, company=None, **kwargs):
        self.company = company
        super().__init__(*args, **kwargs)

    class Meta:
        model = FiscalYear
        fields = ["year", "start_date", "end_date"]
        widgets = {
            "year": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        year = cleaned_data.get("year")

        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("The end date must be after the start date.")

        if year and start_date and end_date:
            if start_date.year != year or end_date.year != year:
                raise forms.ValidationError(
                    "The fiscal year dates must belong to the selected year."
                )
            if start_date.month != 1 or start_date.day != 1:
                raise forms.ValidationError(
                    "The fiscal year must start on January 1."
                )
            if end_date.month != 12 or end_date.day != 31:
                raise forms.ValidationError(
                    "The fiscal year must end on December 31."
                )

            if self.company and FiscalYear.objects.filter(
                company=self.company, year=year
            ).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    "A fiscal year for this company and year already exists."
                )

        return cleaned_data
