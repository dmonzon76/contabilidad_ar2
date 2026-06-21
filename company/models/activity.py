from django.db import models
from company.models import Company
from fiscal.models import AFIPActivity


class CompanyActivity(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    activity = models.ForeignKey(
        AFIPActivity,
        on_delete=models.PROTECT,
        null=True,      # ← agregar
        blank=True,     # ← agregar


        related_name="company_activities"
    )

    is_primary = models.BooleanField(default=False)

    jurisdiction = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional: CABA, BsAs, Córdoba, etc."
    )

    def __str__(self):
        return f"{self.activity.code} - {self.company.name}"

    def save(self, *args, **kwargs):

        # 1) Primera actividad → primaria automática
        if not self.pk:
            if not CompanyActivity.objects.filter(company=self.company).exists():
                self.is_primary = True

        # 2) Si se marca como primaria → desmarcar otras
        if self.is_primary:
            CompanyActivity.objects.filter(
                company=self.company,
                is_primary=True
            ).exclude(id=self.id).update(is_primary=False)

        super().save(*args, **kwargs)
