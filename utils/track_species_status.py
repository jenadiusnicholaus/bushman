from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from bm_hunting_settings.models import QuotaHutingAreaSpecies
from sales.models import SalesInquiry
from sales_confirmation.models import SalesQuotaSpeciesStatus
from sales_confirmation.serializers import UpdateSalesQuotaSpeciesStatusSerializer


class TrackSpeciesStatus:
    @staticmethod
    def track_species_status(sales_confirmation_proposal_id, status, quota_id, area_id):
        """
        This function updates the available quantity of species in the QuotaHutingAreaSpecies
        based on the sold species quantity from the sales inquiry, depending on the status.
        """
        try:
            sales_inquiry = SalesInquiry.objects.get(
                sales_confirmation_proposal__id=sales_confirmation_proposal_id
            )
        except ObjectDoesNotExist:
            raise ValueError("SalesInquiry not found.")

        sold_species = (
            sales_inquiry.sales_confirmation_proposal.sales_confirmation_package.package.sales_package_species.all()
        )

        for species in sold_species:
            quota_species = QuotaHutingAreaSpecies.objects.filter(
                species__id=species.species.id,
                # Uncomment and add filters for area and quota if needed
                area_id=area_id,
                quota_id=quota_id,
            )

            if quota_species.exists():
                current_quantity = quota_species.first().quantity

                # Handle 'provision_sales' status
                if status == "provision_sales":
                    if current_quantity >= species.quantity:
                        quota_species.update(quantity=F("quantity") - species.quantity)

                        species_status, created = (
                            SalesQuotaSpeciesStatus.objects.get_or_create(
                                sales_proposal_id=sales_confirmation_proposal_id,
                                species_id=species.species.id,
                                quota_id=quota_id,
                                area_id=area_id,
                            )
                        )

                        update_data = {
                            "status": status,
                            "quantity": species.quantity,
                        }
                        update_status_serializer = (
                            UpdateSalesQuotaSpeciesStatusSerializer(
                                instance=species_status,
                                data=update_data,
                                partial=True,
                            )
                        )
                        if update_status_serializer.is_valid():
                            update_status_serializer.save()
                        else:
                            raise ValueError(
                                f"Failed to update species status: {update_status_serializer.errors}"
                            )
                    else:
                        print(
                            f"Not enough quantity to reduce for species {species.species.name}. "
                            f"Current: {current_quantity}, Attempted: {species.quantity}"
                        )

                # Handle 'confirmed' and 'completed' statuses
                elif status in ["confirmed", "completed"]:
                    print()
                    species_status, created = (
                        SalesQuotaSpeciesStatus.objects.get_or_create(
                            sales_proposal_id=sales_confirmation_proposal_id,
                            species_id=species.species.id,
                            quota_id=quota_id,
                            area_id=area_id,
                        )
                    )
                    update_data = {
                        "status": status,
                        "quantity": species.quantity,
                    }
                    update_status_serializer = UpdateSalesQuotaSpeciesStatusSerializer(
                        instance=species_status,
                        data=update_data,
                        partial=True,
                    )
                    if update_status_serializer.is_valid():
                        update_status_serializer.save()
                    else:
                        raise ValueError(
                            f"Failed to update species status: {update_status_serializer.errors}"
                        )

                # Handle cancellation or decline
                elif status in ["declined", "cancelled"]:
                    quota_species.update(
                        quantity=F("quantity") + species.quantity
                    )  # Uncomment if it's relevant
                    print(
                        f"Increased quantity for species {species.species.name} by {species.quantity}."
                    )

                else:
                    print("No valid status provided. No change in quantity.")
            else:
                print(f"No quota found for species: {species.species.name}")
