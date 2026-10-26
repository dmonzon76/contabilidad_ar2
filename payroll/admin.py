from django.contrib import admin

from payroll.models import (
    Employee,
    JobCategory,
    LaborAgreement,
    PayrollPeriod,
    PayrollReceipt,
    PayrollReceiptLine,
    SalaryConcept,
)

from payroll.models import (
    EmployeePosition,
)

# Register your models here.





@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "employee_number",
        "last_name",
        "first_name",
        "cuil",
        "is_active",
    )

    search_fields = (
        "employee_number",
        "last_name",
        "first_name",
        "cuil",
    )

    list_filter = (
        "is_active",
    )

@admin.register(LaborAgreement)
class LaborAgreementAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "union_name",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
        "union_name",
    )

    list_filter = (
        "is_active",
    )

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "agreement",
        "base_salary",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )

    list_filter = (
        "agreement",
        "is_active",
    )  
    
@admin.register(SalaryConcept)
class SalaryConceptAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "concept_type",
        "calculation_type",
        "is_remunerative",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )

    list_filter = (
        "concept_type",
        "calculation_type",
        "is_remunerative",
        "is_active",
    )    

@admin.register(PayrollPeriod)
class PayrollPeriodAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "year",
        "month",
        "status",
        "liquidation_date",
    )

    list_filter = (
        "status",
        "year",
    )

    search_fields = (
        "code",
    ) 

@admin.register(PayrollReceipt)
class PayrollReceiptAdmin(admin.ModelAdmin):

    list_display = (
        "employee",
        "period",
        "net_amount",
        "status",
    )

    list_filter = (
        "status",
        "period",
    )

    search_fields = (
        "employee__last_name",
        "employee__first_name",
    )       

@admin.register(PayrollReceiptLine)
class PayrollReceiptLineAdmin(admin.ModelAdmin):

    list_display = (
        "receipt",
        "concept",
        "quantity",
        "unit_amount",
        "amount",
    )

    search_fields = (
        "receipt__employee__last_name",
        "concept__name",
    )

    list_filter = (
        "concept",
    )

@admin.register(EmployeePosition)
class EmployeePositionAdmin(admin.ModelAdmin):

    list_display = (
        "employee",
        "agreement",
        "category",
        "basic_salary",
        "start_date",
        "end_date",
        "is_active",
    )

    search_fields = (
        "employee__last_name",
        "employee__first_name",
    )

    list_filter = (
        "agreement",
        "category",
        "is_active",
    )
