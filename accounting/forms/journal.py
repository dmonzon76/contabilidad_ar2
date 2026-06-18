from django import forms
from django.forms import inlineformset_factory

from accounting.models import JournalEntry, JournalEntryLine


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ["date", "description"]


class JournalEntryLineForm(forms.ModelForm):
    class Meta:
        model = JournalEntryLine
        fields = ["account", "description", "debit", "credit"]


JournalEntryLineFormSet = inlineformset_factory(
    JournalEntry,
    JournalEntryLine,
    form=JournalEntryLineForm,
    extra=4,
    can_delete=True,
)
