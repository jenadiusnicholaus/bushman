from django.db import models

from bm_hunting_settings.models import (
    HuntingArea,
    Locations,
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
import random
import string


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

    AMOUNT_DUE_TYPE_CHOICES = (
        ("PERCENT", "PERCENT"),
        ("LAPS", "LAPS"),
    )

    DUE_DAYS_TYPE = (
        ("UPON_SALES_CONFIRMATION", "Upon Sales Confirmation"),
        ("PRIOR_SAFARI", "Prior to Safari"),
    )

    sales_confirmation_proposal = models.ForeignKey(
        SalesConfirmationProposal,
        on_delete=models.CASCADE,
        related_name="installments",
    )

    narration = models.CharField(max_length=255)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_due_type = models.CharField(
        max_length=255, null=True, blank=True, choices=AMOUNT_DUE_TYPE_CHOICES
    )
    due_days = models.IntegerField(null=True, blank=True)
    due_days_type = models.CharField(
        max_length=255, null=True, blank=True, choices=DUE_DAYS_TYPE
    )

    class Meta:
        verbose_name_plural = "Installments"
        db_table = "installment_setups"

    def __str__(self):
        return f"{self.sales_confirmation_proposal}"


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
        Quota,
        on_delete=models.CASCADE,
        related_name="species_sales_quota_status_set",
        null=True,
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


class SalesConfirmationContract(models.Model):
    sales_confirmation_proposal = models.OneToOneField(
        SalesConfirmationProposal,
        on_delete=models.CASCADE,
        related_name="sales_confirmation_contract_set",
    )
    entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name="contracts",
        related_query_name="enity_contract_set",
        null=True,
        blank=True,
    )
    contract_number = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Sales Confirmation Contracts"
        db_table = "enity_contract"

    def __str__(self):
        return f'{self.sales_confirmation_proposal} - {self.contract_number or "No Contract Number"}'

    def save(self, *args, **kwargs):
        if not self.contract_number:
            self.contract_number = self.generate_contract_number()

        super(SalesConfirmationContract, self).save(*args, **kwargs)

    def generate_contract_number(self):
        # use random 6 digit number with char
        contract_number = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        return contract_number

    class Meta:
        verbose_name_plural = "Sales Confirmation Contracts"
        db_table = "enity_contract"
        unique_together = ("sales_confirmation_proposal", "entity")

    def __str__(self):
        return f'{self.sales_confirmation_proposal} - {self.contract_number or "No Contract Number"}'


class EntityContractPermit(models.Model):
    entity_contract = models.OneToOneField(
        SalesConfirmationContract,
        on_delete=models.CASCADE,
        related_name="permits",
    )
    permit_number = models.CharField(max_length=255, null=True, blank=True)
    issued_date = models.DateField(null=True, blank=True)
    package_type = models.ForeignKey(
        RegulatoryHuntingpackage,
        on_delete=models.CASCADE,
        related_name="entity_contract_permit_package_type_set",
        null=True,
        blank=True,
    )

    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Entity Contract Permits"
        db_table = "entity_contract_permit"

    def __str__(self):
        return f'{self.entity_contract} - {self.permit_number or "No Permit Number"}'


class EntityContractPermitDates(models.Model):
    entity_contract_permit = models.ForeignKey(
        EntityContractPermit,
        on_delete=models.CASCADE,
        related_name="contract_dates_set",
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    amendment = models.ForeignKey(
        "self",  # Reference to the same model
        on_delete=models.SET_NULL,  # If the amended instance is deleted, keep this instance
        null=True,
        blank=True,
        related_name="amendments",  # Optional: to access all amendments related to a record
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Enity Contact Dates"
        db_table = "enity_contract_permit_dates"

    def __str__(self):
        return f'{self.entity_contract_permit} - {self.start_date or "No Start Date"}'


class GameActivity(models.Model):
    entity_contract_permit = models.ForeignKey(
        EntityContractPermit,
        on_delete=models.CASCADE,
        related_name="game_activity_set",
    )
    client = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name="game_activity_client_set",
        null=True,
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Game Activities"
        db_table = "game_activity"
        unique_together = ("entity_contract_permit", "client")

    def __str__(self):
        return f'{self.entity_contract_permit} - {self.start_date or "No Start Date"}'


class GameKilledActivity(models.Model):
    GENDER = (
        ("M", "Male"),
        ("F", "Female"),
    )

    STATUS = (
        ("KILLED", "Killed"),
        ("WOUNDED", "Wounded"),
    )
    game_killed_registration = models.ForeignKey(
        GameActivity,
        on_delete=models.CASCADE,
        related_name="game_killed_activity_set",
    )
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="game_killed_activity_species_set",
    )
    quantity = models.IntegerField(default=1)
    location = models.ForeignKey(
        Locations,
        on_delete=models.CASCADE,
        related_name="game_killed_activity_location_set",
        null=True,
        blank=True,
    )
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="game_killed_activity_Created_by_user_set",
    )
    spacies_gender = models.CharField(
        max_length=255, null=True, blank=True, choices=GENDER
    )

    status = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=STATUS,
    )
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    area = models.ForeignKey(
        HuntingArea,
        on_delete=models.CASCADE,
        related_name="game_killed_activity_area_set",
        null=True,
        blank=True,
    )
    weapon_used = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Game Killed Activities"
        db_table = "game_killed_activity"

    def __str__(self):
        return f'{self.game_killed_registration} - {self.species.name or "No Species"}'


class GameActivityProfessionalHunter(models.Model):
    game_activity = models.ForeignKey(
        GameActivity,
        on_delete=models.CASCADE,
        related_name="professional_hunter_set",
    )
    ph = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name="game_activity_professional_hunter_set",
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Game Activity Professional Hunters"
        db_table = "game_activity_professional_hunter"

    def __str__(self):
        return f'{self.game_activity} - {self.ph or "No Hunter"}'


class SalesConfirmationCompanions(models.Model):
    sales_confirmation_proposal = models.ForeignKey(
        SalesConfirmationProposal,
        on_delete=models.CASCADE,
        related_name="companions",
    )
    regulatory_package = models.ForeignKey(
        RegulatoryHuntingpackage,
        on_delete=models.CASCADE,
        related_name="sales_confirmation_companions_set",
        null=True,
        blank=True,
    )
    companion = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name="companions_set",
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sales Confirmation Companions"
        db_table = "sales_confirmation_companions"

    def __str__(self):
        return (
            f'{self.sales_confirmation_proposal} - {self.companion or "No Companion"}'
        )


class SalesConfirmationProposalObserver(models.Model):
    sales_confirmation_proposal = models.ForeignKey(
        SalesConfirmationProposal,
        on_delete=models.CASCADE,
        related_name="observers",
    )

    observer = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name="sales_confirmation_proposal_observer_set",
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sales Confirmation Proposal Observers"
        db_table = "sales_confirmation_proposal_observer"

    def __str__(self):
        return f'{self.sales_confirmation_proposal} - {self.observer or "No Observer"}'


class SalesConfirmationProposalCompanionItinerary(models.Model):
    itinarary = models.ForeignKey(
        SalesConfirmationProposalItinerary,
        on_delete=models.CASCADE,
        related_name="companion_itineraries",
        null=True,
        blank=True,
    )
    entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name="companion_itineraries_set",
        null=True,
    )

    class Meta:
        verbose_name_plural = "Sales Confirmation Companion Itineraries"
        db_table = "sales_confirmation_companion_itinerary"

    def __str__(self):
        return f'{self.itinarary} - {self.companion or "No Companion"}'
