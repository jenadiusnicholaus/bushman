from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from bm_hunting_settings.models import Quota, QuotaHuntingAreaSpecies
from sales.models import SalesInquiry
from sales_confirmation.models import (
    GameActivity,
    SalesConfirmationProposalStatus,
    SalesQuotaSpeciesStatus,
)
from sales_confirmation.serializers import UpdateSalesQuotaSpeciesStatusSerializer
from django.utils import timezone

from utils.utitlities import currentQuuta


class TrackSpeciesStatus:

    @staticmethod
    def track(sales_confirmation_proposal_id, status, area_id, status_obj):
        """
        This function updates the available quantity of species in the QuotaHuntingAreaSpecies
        based on the sold species quantity from the sales inquiry, depending on the status.
        """
        current_quota = currentQuuta.current_quota

        try:
            sales_inquiry = SalesInquiry.objects.get(
                sales_confirmation_proposal__id=sales_confirmation_proposal_id
            )
        except ObjectDoesNotExist:
            raise ValueError("SalesInquiry not found.")

        sold_species = (
            sales_inquiry.sales_inquiry_species_set.all()
            # from the package
            # sales_inquiry.sales_confirmation_proposal.sales_confirmation_package.package.sales_package_species.all()
        )

        for species in sold_species:
            quota_species = QuotaHuntingAreaSpecies.objects.filter(
                species__id=species.species.id,
                # Uncomment and add filters for area and quota if needed
                area_id=area_id,
                quota_id=current_quota.id,
            )

            if quota_species.exists():
                current_quantity = quota_species.first().quantity
                current_status = status_obj.status

                # Handle 'provision_sales' status
                if status == "provision_sales":
                    if current_quantity >= species.quantity:
                        quota_species.update(quantity=F("quantity") - species.quantity)

                        species_status, created = (
                            SalesQuotaSpeciesStatus.objects.get_or_create(
                                sales_proposal_id=sales_confirmation_proposal_id,
                                species_id=species.species.id,
                                quota_id=current_quota.id,
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
                        #    delete all the species status for this proposal and species, bacause we got an error
                        #    delete all the species status for this proposal and species, bacause we got an error
                        sales_q = SalesQuotaSpeciesStatus.objects.filter(
                            sales_proposal_id=sales_confirmation_proposal_id,
                            quota_id=current_quota.id,
                            area_id=area_id,
                        )
                        for q in sales_q:
                            q.delete()

                        raise ValueError(
                            f"Not enough quantity to reduce for species {species.species.name}. "
                            f"Current: {current_quantity}"
                        )

                # Handle 'confirmed' and 'completed' statuses
                elif status in ["confirmed", "completed"]:
                    if current_status == "pending":
                        if current_quantity >= species.quantity:
                            quota_species.update(
                                quantity=F("quantity") - species.quantity
                            )
                        else:

                            #    delete all the species status for this proposal and species, bacause we got an error
                            sales_q = SalesQuotaSpeciesStatus.objects.filter(
                                sales_proposal_id=sales_confirmation_proposal_id,
                                species_id=species.species.id,
                                quota_id=current_quota.id,
                                area_id=area_id,
                            )
                            for q in sales_q:
                                q.delete()
                            raise ValueError(
                                f"Not enough quantity to sale for species {species.species.name}. "
                                f"Current: {current_quantity}, Attempted: {species.quantity}"
                            )

                    species_status, created = (
                        SalesQuotaSpeciesStatus.objects.get_or_create(
                            sales_proposal_id=sales_confirmation_proposal_id,
                            species_id=species.species.id,
                            quota_id=current_quota.id,
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
                    species_status = SalesQuotaSpeciesStatus.objects.filter(
                        sales_proposal_id=sales_confirmation_proposal_id,
                        species_id=species.species.id,
                        quota_id=current_quota.id,
                        area_id=area_id,
                    )

                    if species_status.exists():
                        species_status.update(
                            status=status,  # Update status field
                            quantity=species.quantity,  # Update quantity field
                        )
                    else:
                        raise ValueError("Species status not found.")

                    quota_species.update(quantity=F("quantity") + species.quantity)

                else:
                    print("No valid status provided. No change in quantity.")

                    raise ValueError(f"Invalid status: {status}")
            else:
                print(f"No quota found for species: {species.species.name}")
                raise ValueError("Quota not found.")

    @staticmethod
    def trackTakenOrSoldSpecies(
        sales_confirmation_proposal_id,
        species_id,
        status,
        area_id,
        teken_quantity,
        game_state,
        game,
    ):
        """
        This function updates the available quantity of species in the QuotaHuntingAreaSpecies
        based on the sold species quantity from the sales inquiry, depending on the status.
        """
        current_year = timezone.now().year

        current_quota = Quota.objects.filter(start_date__year=current_year).first()

        try:
            species_status = SalesQuotaSpeciesStatus.objects.get(
                sales_proposal_id=sales_confirmation_proposal_id,
                species_id=species_id,
                status="confirmed",
                quota_id=current_quota.id,
                area_id=area_id,
            )
        except ObjectDoesNotExist as e:
            raise ValueError(f"No such a species in confirmed sales")

        if status == "completed" and species_status.quantity > 0 and teken_quantity > 0:

            # reduce_quantity = quantity

            species_status.quantity -= teken_quantity
            species_status.save()
            # create new status for reduced quantity to completed

            result, created = SalesQuotaSpeciesStatus.objects.get_or_create(
                sales_proposal_id=sales_confirmation_proposal_id,
                species_id=species_id,
                status="completed",
                quota_id=current_quota.id,
                area_id=area_id,
                defaults={"quantity": teken_quantity},
            )
            if not created:
                result.quantity += teken_quantity
                result.save()
                # update the status if the sales proposal is completed if quantity is 0, then delete the status
                if result.quantity == 0:
                    sales_status = SalesConfirmationProposalStatus.objects.filter(
                        sales_confirmation_proposal=sales_confirmation_proposal_id,
                    )
                    # update the status now
                    sales_status.update(status="completed")

            try:
                TrackSpeciesStatus.takeSpeciesQuantityBackToQuota(
                    sales_confirmation_proposal_id,
                    species_id,
                    area_id,
                    game_state,
                    game,
                )
            except ValueError as e:
                print(e)
                raise ValueError(f"Failed to take back species quantity to quota: {e}")

        else:
            raise ValueError(
                f"Error, This may be reasons, 1. Species status is not confirmed, 2. Species quantity is not enough, 3. Game is  closed, 4. Teken quantity is not enough"
            )

    @staticmethod
    def updateSalesProposalStatus(sales_confirmation_proposal_id, status):
        """
        This function updates the status of sales proposal based on the sold species quantity from the sales inquiry, depending on the status.
        """
        sales_status = SalesConfirmationProposalStatus.objects.filter(
            sales_confirmation_proposal=sales_confirmation_proposal_id,
        )
        # update the status now
        sales_status.update(status=status)

    @staticmethod
    def takeSpeciesQuantityBackToQuota(
        sales_confirmation_proposal_id, species_id, area_id, game_state, game
    ):
        """
        This function returns the remaining quantity of species in the QuotaHuntingAreaSpecies
        based on the sold species quantity from the sales inquiry, depending on the status.
        """
        current_quota = currentQuuta.current_quota

        # if game_state == "completed":
        # then check for all remaing comfirmed quantity and return it for specific sales proposal, quota and area
        #  and return them  to the spesific [QuotaHuntingAreaSpecies], because hunting is done and we need to return the remaining quantity

        species_status = SalesQuotaSpeciesStatus.objects.filter(
            sales_proposal_id=sales_confirmation_proposal_id,
            status="confirmed",
            quota_id=current_quota.id,
            area_id=area_id,
        )
        if game_state == "CLOSED":
            # if game is closed, then update the status of sales proposal to completed and return the remaining quantity to the QuotaHuntingAreaSpecies
            for status in species_status:
                quota_species = QuotaHuntingAreaSpecies.objects.get(
                    species_id=status.species.id,
                    area_id=area_id,
                    quota_id=current_quota.id,
                )
                if status.quantity > 0:
                    # get  QuotaHuntingAreaSpecies for specific sales proposal   , quota and area and specific species the update the quantity
                    #  with remaining quantity

                    quota_species.quantity += status.quantity
                    status.quantity = 0
                    status.save()
                    quota_species.save()
                    TrackSpeciesStatus.updateSalesProposalStatus(
                        sales_confirmation_proposal_id, "completed"
                    )
                else:
                    TrackSpeciesStatus.updateSalesProposalStatus(
                        sales_confirmation_proposal_id, "completed"
                    )

        else:
            # if there still remained quantity in the quota in  with confirmed status the game my be in progress, we need not do anything on confirmed species,
            # imagine we have a list of quantity for each species in the QuotaHuntingAreaSpecies, and we need to check if there is any remaining quantity
            # if there is no remaining quantity, then update the status of sales proposal to completed

            #  we ca count all quanting for given area, quota and and sales proposal, and check if there is any remaining quantity, if there is no remaining quantity, then update the status of sales proposal to completed and return the remaining quantity to the QuotaHuntingAreaSpecies
            # sum of quantity remained
            _sum = sum(status.quantity for status in species_status)
            if _sum == 0:
                # if there is no remaining quantity, then update the status of sales proposal to completed and return the remaining quantity to the QuotaHuntingAreaSpecies

                TrackSpeciesStatus.updateSalesProposalStatus(
                    sales_confirmation_proposal_id, "completed"
                )
                print("Game is completed")
                # update the game status to closed
                print(game.id)
                try:
                    _game = GameActivity.objects.get(id=game.id)
                    _game.status = "CLOSED"
                    _game.save()
                except ObjectDoesNotExist:
                    print("Game not found")
