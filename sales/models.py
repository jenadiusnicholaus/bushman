from django.db import models
from django.utils import timezone
from bm_hunting_settings.models import (
    Currency,
    HuntingBlock,
    HuntingType,
    IdentityType,
    Package,
    SafariPackageType,
    Species,
)
from django_countries.fields import CountryField
from django.contrib.auth.models import User


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
    nationality_id = models.IntegerField(null=True, blank=True)
    country = CountryField(null=True)
    nationality = models.CharField(max_length=100)

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
        return self.entity.full_name + " - " + self.entity


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


class EntityHuntingInfos(models.Model):
    entity = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="entity_set"
    )
    hunting_area = models.ForeignKey(
        HuntingBlock, on_delete=models.CASCADE, related_name="entity_hunting_area_set"
    )
    hunting_type = models.ForeignKey(
        HuntingType, on_delete=models.CASCADE, related_name="entity_hunting_type_set"
    )
    number_of_hunters = models.IntegerField(default=0)
    number_of_days = models.IntegerField(default=0)

    number_companions = models.IntegerField(default=0)
    species_to_hunt = models.ManyToManyField(Species)
    safari_package_type = models.ForeignKey(
        SafariPackageType,
        on_delete=models.CASCADE,
        related_name="entity_safari_package_type_set",
        null=True,
    )

    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Entity Hunting Infos"
        db_table = "hunting_infos"

    def __str__(self):
        return (
            self.entity.full_name
            + " - "
            + str(self.number_of_hunters)
            + " - "
            + str(self.number_of_days)
        )

    # payment_method_type = models.CharField(


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
    PAYMENT_METHOD_TYPE = (
        ("bank_transfer", "Bank Transfer"),
        ("credit_card", "Credit Card"),
        ("cash", "Cash"),
    )
    entity = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="sales_payment_entity_set"
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method_type = models.CharField(
        max_length=100, choices=PAYMENT_METHOD_TYPE, default="bank_transfer"
    )  # bank transfer, credit card, cash

    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sales Payments"
        db_table = "sales_payments"

    def __str__(self):
        return self.entity.full_name + " - " + str(self.total_amount)


class ContractType(models.Model):
    name = models.CharField(max_length=100)
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Contract Types"
        db_table = "contract_types"

    def __str__(self):
        return self.name


class SalesConfirmation(models.Model):

    payment_id = models.ForeignKey(
        SalesPayment,
        on_delete=models.CASCADE,
        related_name="sales_confirmation_payment_set",
    )
    entity = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="sales_confirmation_entity_set"
    )
    hunting_info = models.ForeignKey(
        EntityHuntingInfos,
        on_delete=models.CASCADE,
        related_name="sales_confirmation_hunting_info_set",
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sales Confirmations"
        db_table = "sales_confirmations"

    def __str__(self):
        return self.entity.full_name + " - " + str(self.total_amount)


class Contract(models.Model):
    confirmed_sale_id = models.ForeignKey(
        SalesConfirmation,
        on_delete=models.CASCADE,
        related_name="contract_confirmed_sale_set",
    )

    contract_number = models.CharField(max_length=100, unique=True)
    contract_type = models.ForeignKey(
        ContractType, on_delete=models.CASCADE, related_name="contract_type_set"
    )
    entity = models.ForeignKey(
        Entity, on_delete=models.CASCADE, related_name="contract_entity_set"
    )
    hunting_info = models.ForeignKey(
        EntityHuntingInfos,
        on_delete=models.CASCADE,
        related_name="contract_hunting_info_set",
    )
    signed = models.DateTimeField(default=timezone.now)
    signed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Contracts"
        db_table = "contracts"

    def __str__(self):
        return self.entity.full_name + " - " + self.contract_number


class PackageCustomization(models.Model):
    entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name="package_customization_entity_set",
    )

    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="package_customization_package_type_set",
    )

    hunting_type = models.ForeignKey(
        HuntingType,
        on_delete=models.CASCADE,
        related_name="customizable_packages_set",
        null=True,
    )
    hunting_block = models.ForeignKey(
        HuntingBlock,
        on_delete=models.CASCADE,
        related_name="customizable_packages_set",
        null=True,
    )

    number_of_hunters = models.IntegerField(default=1)
    number_of_days = models.IntegerField(default=0)
    number_companions = models.IntegerField(default=0)
    species_to_hunt = models.ManyToManyField(Species)
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Package Customizations"
        db_table = "package_customizations"

    def __str__(self):
        return self.entity.full_name


class Document(models.Model):
    DocTYpe = (
        ("Passport_Copy", "Travel Packet(Passport Copy)"),
        ("Passport_Photo", "Travel Packet(Passport  Photo"),
        ("Visa", "Visa"),
        ("Gun Permits", "Gun Permits"),
        ("CITES Documentation", "CITES Documentation"),
    )
    forWho = models.CharField(max_length=100, null=True)
    document_type = models.CharField(max_length=100, choices=DocTYpe)
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


class PackageUpgrade(models.Model):
    entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name="package_upgrade_entity_set",
    )

    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="package_upgrade_package_type_set",
    )
    number_of_hunters = models.IntegerField(default=0)
    number_of_days = models.IntegerField(default=0)
    number_companions = models.IntegerField(default=0)
    species_to_hunt = models.ManyToManyField(Species)
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Package Upgrades"
        db_table = "package_upgrades"

    def __str__(self):
        return self.entity.full_name


class SalesCalender(models.Model):
    sale_id = models.ForeignKey(
        SalesConfirmation,
        on_delete=models.CASCADE,
        related_name="sales_calender_sale_set",
    )
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sales Calenders"
        db_table = "sales_calenders"

    def __str__(self):
        return self.sale_id.entity.full_name + " - " + str(self.created_at)


class ContactTyoe(models.Model):
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
        ContactTyoe, on_delete=models.CASCADE, related_name="contact_type_set"
    )
    contact = models.CharField(max_length=100)

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
