from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from authentication.models import UserProfile
from bm_hunting_settings.models import (
    # HuntingBlock,
    HuntingType,
    IdentityType,
    # Package,
    SafariPackageType,
    Species,
)
import uuid
from django_countries.fields import CountryField


gender_choices = (
    ("Male", "Male"),
    ("Female", "Female"),
)


#  Model to deleted
class Client(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="main_client",
        null=True,
        blank=True,
    )
    # passport_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "clients"

    def __str__(self):

        return self.user.username


class Observer(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="observer_main_client",
        null=True,
        blank=True,
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="observer", null=True, blank=True
    )
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "observers"


class Companion(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="companion_main_client",
        null=True,
        blank=True,
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="companion", null=True, blank=True
    )
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "companions"


class Weapontype(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Weapon Types"
        db_table = "weapon_type"


class Weapon(models.Model):
    weapon_type = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    caliber = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    ammo_quantity = models.IntegerField(default=0)
    maker_number = models.CharField(max_length=100)
    weapon_owner = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Weapons"
        db_table = "weapons"

    def __str__(self):
        return (
            self.owner
            + " - "
            + self.brand
            + " - "
            + self.caliber
            + " - "
            + self.serial_number
            + " - "
            + str(self.ammo_quantity)
            + " - "
            + self.maker_number
            + " - "
            + self.weapon_owner
        )


class clientItinerary(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="client_itinerary"
    )
    airport_arrival = models.CharField(max_length=100)
    airport_departure = models.CharField(max_length=100)
    charter_flight_arrangements = models.TextField()
    hotel_bookings = models.TextField(help_text="Number of rooms and types required")
    arrival_date = models.DateField()
    departure_date = models.DateField()

    class Meta:
        verbose_name_plural = "client Itineraries"
        # db_table = 'client_itineraries'

    def __str__(self):
        return (
            self.hunter.user.username
            + " - "
            + self.airport_arrival
            + " - "
            + self.airport_departure
            + " - "
            + self.charter_flight_arrangements
            + " - "
            + self.hotel_bookings
            + " - "
            + str(self.arrival_date)
            + " - "
            + str(self.departure_date)
        )


class ClientPreferences(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="client_preferences"
    )
    food_preferences = models.TextField()
    beverage_preferences = models.TextField()
    allergies = models.TextField()
    alcohol_preferences = models.TextField()
    clothing_gear_needs = models.TextField()
    special_requests = models.TextField()

    class Meta:
        verbose_name_plural = "Client Preferences"
        db_table = "client_preferences"

    def __str__(self):
        return (
            self.client.first_name
            + " - "
            + self.food_preferences
            + " - "
            + self.beverage_preferences
            + " - "
            + self.allergies
            + " - "
            + self.alcohol_preferences
            + " - "
            + self.clothing_gear_needs
            + " - "
            + self.special_requests
        )


# class ClientCustomizablePackage(models.Model):
#     package_type = models.ForeignKey(
#         SafariPackageType,
#         on_delete=models.CASCADE,
#         related_name="customizable_packages",
#         null=True,
#         blank=True,
#     )
#     hunting_type = models.ForeignKey(
#         HuntingType,
#         on_delete=models.CASCADE,
#         related_name="customizable_packages",
#         null=True,
#     )
#     hunting_block = models.ForeignKey(
#         HuntingBlock,
#         on_delete=models.CASCADE,
#         related_name="customizable_packages",
#         null=True,
#     )
#     number_of_hunters = models.IntegerField(
#         default=0,
#         null=True,
#     )
#     number_of_days = models.IntegerField(
#         default=0,
#         null=True,
#     )
#     create_date = models.DateTimeField(
#         default=timezone.now,
#         null=True,
#     )
#     updated_date = models.DateTimeField(
#         auto_now=True,
#         null=True,
#     )

#     class Meta:
#         verbose_name_plural = "Client Customizable Packages"
#         db_table = "client_customizable_packages"

#     def __str__(self):
#         return (
#             self.package_type.package_name
#             + " - "
#             + self.hunting_type.hunting_type_name
#             + " - "
#             + self.hunting_block.block_name
#             + " - "
#             + str(self.number_of_hunters)
#             + " - "
#             + str(self.number_of_days)
#             + " - "
#             + str(self.create_date)
#             + " - "
#             + str(self.updated_date)
#         )


# class ClientSalesOrder(models.Model):
#     ORDER_STATUS = (
#         ("Pending", "Pending"),
#         ("Confirmed", "Confirmed"),
#         ("Completed", "Completed"),
#     )
#     order_number = models.UUIDField(
#         primary_key=True, default=uuid.uuid4, editable=False
#     )
#     client = models.ForeignKey(
#         Client,
#         on_delete=models.CASCADE,
#         related_name="main_client_sales_orders",
#         null=True,
#         blank=True,
#     )

#     order_date = models.DateField(null=True)  # Removed auto_created
#     pre_def_package = models.ManyToManyField(Package)
#     package_customized = models.BooleanField(default=False)
#     customizable_package = models.ForeignKey(
#         ClientCustomizablePackage, on_delete=models.CASCADE, null=True, blank=True
#     )
#     confirm_date = models.DateField(null=True)
#     status = models.CharField(max_length=10, choices=ORDER_STATUS, default="Pending")
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
#     payment_status = models.CharField(max_length=100, null=True)
#     payment_date = models.DateField(null=True)
#     payment_document = models.FileField(upload_to="documents/", null=True, blank=True)

#     class Meta:
#         verbose_name_plural = "Client Sales Orders"
#         db_table = "client_sales_orders"

#     def __str__(self):
#         return f"{self.client.first_name} - {self.order_number} - {self.order_date}"

#     class Meta:
#         verbose_name_plural = "Sales Orders"
#         db_table = "client_sales_orders"

#     def __str__(self):
#         return f"{self.client.first_name} - {self.order_number} - {self.order_date}"


# # hunting settings
# class HuntingClientLicense(models.Model):
#     client = models.ForeignKey(
#         Client, on_delete=models.CASCADE, related_name="hunting_license"
#     )
#     license_number = models.CharField(max_length=100)
#     issue_date = models.DateField()
#     expiry_date = models.DateField()
#     licence_document = models.FileField(upload_to="documents/")

#     class Meta:
#         verbose_name_plural = "Hunting Licenses"
#         db_table = "client_hunting_licenses"

#     def __str__(self):
#         return (
#             self.client.first_name
#             + " - "
#             + self.license_number
#             + " - "
#             + str(self.issue_date)
#             + " - "
#             + str(self.expiry_date)
#             + " - "
#             + self.licence_document.name
#         )
