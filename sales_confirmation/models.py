from django.db import models

from bm_hunting_settings.models import (
    HuntingArea,
    Quota,
    RegulatoryHuntingpackage,
    SalesPackages,
    Species,
)
from sales.models import Document, Entity, SalesInquiry
from django.core.validators import MaxLengthValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# timezone
from django.utils import timezone


class SalesConfirmationProposal(models.Model):
    sales_inquiry = models.OneToOneField(
        SalesInquiry,
        on_delete=models.CASCADE,
        related_name="sales_confirmation_proposal",
        null=True,
        blank=True,
    )
    regulatory_package = models.ForeignKey(
        RegulatoryHuntingpackage,
        on_delete=models.CASCADE,
        related_name="sales_confirmation_proposal_regulatory_package",
        null=True,
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
        # db_table = "sales_confirmation_proposals"
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
        SalesPackages,
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


class SalesConfirmationProposalStatus(models.Model):
    STATUS = (
        ("pending", "Pending"),
        ("provision_sales", "Provision Sales"),
        ("confirmed", "Confirmed"),
        ("declined", "Declined"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    )
    sales_confirmation_proposal = models.OneToOneField(
        SalesConfirmationProposal,
        on_delete=models.CASCADE,
        related_name="status",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sales_confirmation_status_user",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[MaxLengthValidator(255)],
        choices=STATUS,
        default="pending",
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        related_name="sales_confirmation_status_documents",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sales Confirmation Status"
        db_table = "sales_confirmation"

    def __str__(self):
        return f"{self.sales_confirmation_proposal} - {self.status}"


@receiver(post_save, sender=SalesConfirmationProposal)
def create_or_update_sales_confirmation_status(sender, instance, created, **kwargs):
    if created:
        status, created = SalesConfirmationProposalStatus.objects.get_or_create(
            sales_confirmation_proposal=instance
        )
    # instance.status.save()


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
    DUE_LIMIT_CHOICES = (
        ("prior", "Due Before the Due Date"),
        ("after", "Due After the Due Date"),
        ("none", "No Due Date"),
    )
    sales_confirmation_proposal = models.ForeignKey(
        SalesConfirmationProposal,
        on_delete=models.CASCADE,
        related_name="installments",
    )
    description = models.CharField(max_length=255)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    days = models.IntegerField(null=True, blank=True)
    due_limit = models.CharField(
        max_length=255, choices=DUE_LIMIT_CHOICES, default="none"
    )

    class Meta:
        verbose_name_plural = "Installments"
        db_table = "sales_confirmation_installment"

    def __str__(self):
        return f"{self.sales_confirmation_proposal} - {self.description}"


class SalesQuotaSpeciesStatus(models.Model):
    # from sales.models import SalesEnquiry

    STATUS = (
        ("pending", "Pending"),
        ("provision_sales", "Provision Sales"),
        ("confirmed", "Confirmed"),
        ("declined", "Declined"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    )
    sales_proposal = models.ForeignKey(
        SalesConfirmationProposal,
        on_delete=models.CASCADE,
        related_name="species_sales_inquiry_status_set",
    )
    quota = models.ForeignKey(
        Quota, on_delete=models.CASCADE, related_name="species_sales_quota_status_set"
    )
    area = models.ForeignKey(
        HuntingArea,
        on_delete=models.CASCADE,
        related_name="species_sales_area_status_set",
    )

    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="species_sales_species_status_set",
    )
    status = models.CharField(max_length=100, choices=STATUS, default="pending")
    quantity = models.IntegerField(default=0)
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sales Quota Species Status"
        db_table = "sales_quota_species_status"

    def __str__(self):
        return self.species.name + " - " + self.status
