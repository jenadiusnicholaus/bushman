from django.db import models

from bm_hunting_settings.models import SalesPackage
from sales.models import Entity, SalesInquiry
from django.core.validators import MaxLengthValidator


class SalesConfirmationProposal(models.Model):
    sales_inquiry = models.OneToOneField(
        SalesInquiry,
        on_delete=models.CASCADE,
        related_name="sales_confirmation_proposal",
        null=True,
        blank=True,
    )
    client = models.OneToOneField(
        Entity,
        on_delete=models.CASCADE,
        related_name="sales_confirmation_proposal_client",
        null=True,
        blank=True,
    )

    confirmation_date = models.DateField(auto_now=True, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sales Confirmation Proposals"
        db_table = "sales_confirmation_proposal"
        unique_together = ("sales_inquiry", "id")

    def __str__(self):
        return f"{self.client} - {self.sales_inquiry}"


class SalesConfirmationProposalPackage(models.Model):
    sales_confirmation_proposal = models.OneToOneField(
        SalesConfirmationProposal,
        on_delete=models.CASCADE,
        related_name="sales_confirmation_package",
    )
    package = models.ForeignKey(
        SalesPackage,
        on_delete=models.CASCADE,
        related_name="sales_confirmation_package_package",
        null=True,
        blank=True,
    )

    hunting_license = models.CharField(max_length=255, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sales Confirmation Packages"
        db_table = "sales_confirmation_package"

    def __str__(self):
        return f"{self.sales_confirmation_proposal} - {self.hunting_license}"


class SalesConfirmationProposalItinerary(models.Model):
    sales_confirmation_proposal = models.OneToOneField(
        SalesConfirmationProposal,
        on_delete=models.CASCADE,
        related_name="itineraries",
    )
    airport_name = models.CharField(
        max_length=255, null=True, blank=True, validators=[MaxLengthValidator(255)]
    )
    arrival = models.DateTimeField(null=True, blank=True)
    charter_in = models.DateTimeField(null=True, blank=True)
    charter_out = models.DateTimeField(null=True, blank=True)
    hotel_booking = models.CharField(
        max_length=255, null=True, blank=True, validators=[MaxLengthValidator(255)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sales Confirmation Itineraries"
        db_table = "sales_confirmation_itinerary"

    def __str__(self):
        return (
            f"{self.sales_confirmation_proposal} - {self.airport_name or 'No Airport'}"
        )


class SalesConfirmationProposalAdditionalService(models.Model):
    sales_confirmation_proposal = models.ForeignKey(
        SalesConfirmationProposal,
        on_delete=models.CASCADE,
        related_name="additional_services",
    )
    service = models.CharField(
        max_length=255, null=True, blank=True, validators=[MaxLengthValidator(255)]
    )
    quantity = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sales Confirmation Additional Services"
        db_table = "sales_confirmation_additional_service"

    def __str__(self):
        return f"{self.sales_confirmation_proposal} - {self.service or 'No Service'}"


# FOOD
# ALLGERGIES
# BEVERAGES
# ALCOHOL
# SHIRT
# SPECIAL REQUESTS


#  food = models.CharField(
#         max_length=255, null=True, blank=True, validators=[MaxLengthValidator(255)]
#     )
#     allergies = models.CharField(
#         max_length=255, null=True, blank=True, validators=[MaxLengthValidator(255)]
#     )
#     beverages = models.CharField(
#         max_length=255, null=True, blank=True, validators=[MaxLengthValidator(255)]
#     )
#     alcohol = models.CharField(
#         max_length=255, null=True, blank=True, validators=[MaxLengthValidator(255)]
#     )
#     shirt = models.CharField(
#         max_length=255, null=True, blank=True, validators=[MaxLengthValidator(255)]
#     )
class SalesConfirmationProposalClientPreference(models.Model):
    sales_confirmation_proposal = models.ForeignKey(
        SalesConfirmationProposal,
        on_delete=models.CASCADE,
        related_name="client_preferences",
    )
    preference_name = models.CharField(
        max_length=255, null=True, blank=True, validators=[MaxLengthValidator(255)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sales Confirmation Client Preferences"
        db_table = "sales_confirmation_client_preference"

    def __str__(self):
        return f"{self.sales_confirmation_proposal}"


class Installment(models.Model):
    sales_confirmation_proposal = models.ForeignKey(
        SalesConfirmationProposal,
        on_delete=models.CASCADE,
        related_name="installments",
    )
    description = models.CharField(max_length=255)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()

    class Meta:
        verbose_name_plural = "Installments"
        db_table = "sales_confirmation_installment"

    def __str__(self):
        return f"Installment for {self.sales_confirmation.client.name} - Due: {self.due_date}"
