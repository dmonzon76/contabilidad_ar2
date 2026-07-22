from django import forms

from fiscal.models.AFIPactivities import AFIPActivity


class AFIPActivityForm(forms.ModelForm):
    class Meta:
        model = AFIPActivity
        fields = [
            "code",
            "description",
        ]
