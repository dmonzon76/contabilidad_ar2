from django.db import models
from django.utils import timezone


class FamilyMember(models.Model):

    RELATIONSHIP_CHOICES = [
        ("SPOUSE", "Spouse"),
        ("CHILD", "Child"),
        ("STEPCHILD", "Stepchild"),
        ("PARENT", "Parent"),
        ("OTHER", "Other"),
    ]

    employee = models.ForeignKey(
        "payroll.Employee",
        on_delete=models.CASCADE,
        related_name="family_members",
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    dni = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    birth_date = models.DateField()

    relationship = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_CHOICES,
    )

    dependent = models.BooleanField(
    default=True,
    help_text=(
        "Economically dependent on employee."
    ),
)

    disabled = models.BooleanField(
    default=False,
)

    family_allowance_until = models.DateField(
    blank=True,
    null=True,
    help_text=(
        "Date until the family allowance "
        "can be claimed."
    ),
)


    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "relationship",
            "last_name",
            "first_name",
        ]

        verbose_name = "Family Member"

        verbose_name_plural = "Family Members"

    def __str__(self):

        return (
            f"{self.last_name}, "
            f"{self.first_name}"
        )

@property
def receives_family_allowance(
    self,
):

    if not self.family_allowance_until:

        return True

    return (
        self.family_allowance_until
        >= timezone.now().date()
    )