from django.db import models

from company.models import Company
from accounting.models import Account


class AccountingSettings(models.Model):

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="accounting_settings"
    )

    # ==========================
    # SALES
    # ==========================

    account_customers = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        verbose_name="Customers Account"
    )

    account_sales_goods = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        verbose_name="Sales Goods"
    )

    account_sales_services = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        verbose_name="Sales Services"
    )

    account_iva_debit = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        verbose_name="VAT Debit"
    )

    # ==========================
    # PURCHASES
    # ==========================

    account_suppliers = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        verbose_name="Suppliers"
    )

    account_inventory = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        verbose_name="Inventory"
    )

    account_expenses = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        verbose_name="Expenses"
    )

    account_iva_credit = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        verbose_name="VAT Credit"
    )

    # ==========================
    # COST OF SALES
    # ==========================

    account_cmv = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        verbose_name="Cost of Goods Sold"
    )

    # ==========================
    # CASH & BANKS
    # ==========================

    account_cash = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        verbose_name="Cash"
    )

    account_bank = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True,
        verbose_name="Bank"
    )

    # ==========================
    # PERCEPTIONS
    # ==========================

    account_iva_perception_payable = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True
    )

    account_iibb_perception_payable = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True
    )

    # ==========================
    # RETENTIONS
    # ==========================

    account_iva_retention_payable = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True
    )

    account_ganancias_retention_payable = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True
    )

    account_iibb_retention_payable = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True
    )

    # ==========================
    # RESULTS
    # ==========================

    account_current_year_result = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Accounting Settings"
        verbose_name_plural = "Accounting Settings"

    def __str__(self):
        return f"Accounting Settings - {self.company.name}"
