from fiscal.models import (
    TaxRegistryRate,
)


class TaxRateResolver:

    @staticmethod
    def resolve(
        supplier,
        rule,
        period,
    ):

        if (
            rule.calculation_method
            == "FIXED"
        ):
            return (
                rule.effective_rate()
            )

        if (
            rule.calculation_method
            == "REGISTRY"
        ):

            registry_rate = (
                TaxRegistryRate.objects
                .filter(
                    cuit=supplier.tax_id,
                    registry__period=period,
                    registry__is_active=True,
                )
                .first()
            )

            if not registry_rate:
                return None

            if (
                registry_rate.perception_rate
                is not None
            ):
                return (
                    registry_rate.perception_rate
                )

            return (
                registry_rate.retention_rate
            )

        return None