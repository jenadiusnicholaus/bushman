from django.db import models
from django.utils import timezone
from bm_hunting_settings.models import (
    AccommodationType,
    Country,
    Currency,
    # HuntingBlock,
    HuntingType,
    IdentityType,
    Nationalities,
    # Package,
    SafariPackageType,
    Species,
)
from django_countries.fields import CountryField
from django.contrib.auth.models import User
import random
import string


class PaymentMethod(models.Model):
    PAYMENT_METHOD_TYPE = (
        ("bank_transfer", "Bank Transfer"),
        ("credit_card", "Credit Card"),
        ("cash", "Cash"),
    )
    type = models.CharField(
        max_length=100, choices=PAYMENT_METHOD_TYPE, default="bank_transfer"
    )  # bank transfer, credit card, cash

    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Payment Methods"
        db_table = "payment_methods"

    def __str__(self):
        return self.type


class EntityCategories(models.Model):
    name = models.CharField(max_length=100)
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Entity Categories"
        db_table = "entity_categories"

    def __str__(self):
        return self.name


class Entity(models.Model):
    full_name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="entity_user_set", null=True
    )
    # email = models.EmailField(max_length=100, unique=True)
    # phone_number = models.CharField(max_length=100, unique=True)
    # address = models.CharField(max_length=200)
    nick_name = models.CharField(max_length=100, null=True, blank=True)
    nationality = models.ForeignKey(Nationalities, on_delete=models.CASCADE, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    # nationality = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Entities"
        db_table = "entities"

    def __str__(self):
        return self.full_name


class SalesInquiry(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sales_inquiry_user_set"
    )
    entity = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="sales_inquiry_entity_set"
    )

    create_date = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    remarks = models.TextField(max_length=500, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Sales Inquiries"
        db_table = "sales_inquiries"

    def __str__(self):
        if self.entity:
            return self.entity.full_name + " - " + self.code
        else:
            return self.user.username + " - " + self.code

    def save(self, *args, **kwargs):
        self.generate_code()
        super(SalesInquiry, self).save(*args, **kwargs)

    def generate_code(self):
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        self.code = code


class SalesInquirySpecies(models.Model):
    sales_inquiry = models.ForeignKey(
        SalesInquiry, on_delete=models.CASCADE, related_name="sales_inquiry_species_set"
    )
    species = models.ForeignKey(
        Species, on_delete=models.CASCADE, related_name="species_sales_inquiry_set"
    )

    class Meta:
        verbose_name_plural = "Sales Inquiry Species"
        db_table = "sales_inquiry_species"

    def __str__(self):
        return self.sales_inquiry.entity.full_name + " - " + self.species.name


class EntityCategory(models.Model):
    entity = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="entity_category"
    )
    category = models.ForeignKey(
        EntityCategories, on_delete=models.CASCADE, related_name="entity_category"
    )
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Entity Categories"
        db_table = "entity_category"

    def __str__(self):
        return self.entity.full_name + " - " + self.category.name


class BankDetails(models.Model):
    entity = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="bank_details_entity_set"
    )
    bank_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    account_holder_name = models.CharField(max_length=100)
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Bank Details"
        db_table = "bank_details"

    def __str__(self):
        return (
            self.entity.full_name + " - " + self.bank_name + " - " + self.account_number
        )


class SalesPayment(models.Model):
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="sales_payment_currency_set",
        null=True,
    )

    entity = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="sales_payment_entity_set"
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method_type = models.ForeignKey(
        PaymentMethod, on_delete=models.CASCADE, related_name="sales_payment_method_set"
    )
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sales Payments"
        db_table = "sales_payments"

    def __str__(self):
        return self.entity.full_name + " - " + str(self.total_amount)


class SalesIquiryPreference(models.Model):

    sales_inquiry = models.ForeignKey(
        SalesInquiry,
        on_delete=models.CASCADE,
        related_name="sales_inquiry_preference_set",
    )
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.CASCADE,
        related_name="sales_inquiry_payment_method_set",
        null=True,
        blank=True,
    )
    prev_experience = models.TextField(max_length=500, null=True, blank=True)

    preffered_date = models.DateTimeField(default=timezone.now)
    no_of_hunters = models.IntegerField(default=1)
    no_of_observers = models.IntegerField(default=0)
    no_of_days = models.IntegerField(default=0)
    no_of_companions = models.IntegerField(default=0)
    special_requests = models.CharField(max_length=100, null=True, blank=True)
    budget_estimation = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    accommodation_type = models.ForeignKey(
        AccommodationType, on_delete=models.CASCADE, null=True, blank=True
    )
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sales Inquiry Preferences"
        db_table = "sales_inquiry_preferences"

    def __str__(self):
        return (
            self.sales_inquiry.entity.full_name
            + " - "
            + str(self.no_of_hunters)
            + " - "
            + str(self.no_of_days)
        )


class ContractType(models.Model):
    name = models.CharField(max_length=100)
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Contract Types"
        db_table = "contract_types"

    def __str__(self):
        return self.name


class Document(models.Model):
    DocType = (
        ("Passport_Copy", "Travel Packet(Passport Copy)"),
        ("Passport_Photo", "Travel Packet(Passport  Photo"),
        ("Visa", "Visa"),
        ("Gun Permits", "Gun Permits"),
        ("CITES Documentation", "CITES Documentation"),
    )
    forWho = models.CharField(max_length=100, null=True)
    document_type = models.CharField(max_length=100, choices=DocType)
    client = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="entity_document_set"
    )
    document = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "Client Documents"
        db_table = "documents"
        unique_together = ("forWho", "document_type")

    def __str__(self):
        return (
            self.client.user.username
            + " - "
            + self.document_type
            + " - "
            + self.document.name
        )


class ContactType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Contact Types"
        db_table = "contact_types"

    def __str__(self):
        return self.name


class Contacts(models.Model):
    entity = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="entity_contacts_set"
    )
    contact_type = models.ForeignKey(
        ContactType, on_delete=models.CASCADE, related_name="contact_type_set"
    )
    contact = models.CharField(max_length=100)
    contactable = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Contacts"
        db_table = "contacts"

    def __str__(self):
        return (
            self.entity.full_name
            + " - "
            + self.contact_type.name
            + " - "
            + self.contact
        )


class Identity(models.Model):
    entity_user = models.OneToOneField(
        Entity, on_delete=models.CASCADE, related_name="identity"
    )
    identity_type = models.ForeignKey(
        IdentityType, on_delete=models.CASCADE, related_name="identity_type"
    )
    identity_number = models.CharField(max_length=100)
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Identities"
        db_table = "identities"

    def __str__(self):
        return (
            self.user.username
            + " - "
            + self.identity_type.name
            + " - "
            + self.identity_number
        )
