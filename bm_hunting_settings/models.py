from django.db import models

# user
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django_countries.fields import CountryField


# hunting settings
class Quota(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_quotas", null=True
    )
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    update_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "Quotas"
        db_table = "hunting_quotas"

    def __str__(self):

        return self.name


class AccommodationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Accommodation Types"
        db_table = "accommodation_types"

    def __str__(self):
        return self.name


# hunting settings
class Species(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Species"
        db_table = "species"

    def __str__(self):
        return self.name


class SpeciesUnits(models.Model):
    species = models.ForeignKey(
        Species, on_delete=models.CASCADE, related_name="species_unis"
    )
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Species Unis"
        db_table = "species_units"

    def __str__(self):
        return self.name


class OperationType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Operation Types"
        db_table = "operation_types"

    def __str__(self):
        return self.name


class LocationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Location Types"
        db_table = "location_types"

    def __str__(self):
        return self.name


class GeoLocationCoordinates(models.Model):
    point_type = (
        ("Point", "Point"),
        ("LineString", "LineString"),
        ("Polygon", "Polygon"),
        ("MultiPoint", "MultiPoint"),
        ("MultiLineString", "MultiLineString"),
        ("MultiPolygon", "MultiPolygon"),
    )

    point_type = models.CharField(max_length=100, null=True, blank=True)
    coordinates = models.JSONField(default=list)
    altitude = models.FloatField(null=True, blank=True)
    satilate = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "Geo Location Coordinates"
        db_table = "geo_location_coordinates"

        def __str__(self):
            return str(self.coordinates)


class Locations(models.Model):
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location_type = models.ForeignKey(
        LocationType, on_delete=models.CASCADE, related_name="location_type"
    )
    is_disabled = models.BooleanField(default=False)
    geo_coordinates = models.ForeignKey(
        GeoLocationCoordinates,
        on_delete=models.CASCADE,
        related_name="geo_coordinates",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "Locations"
        db_table = "locations"

    def __str__(self):
        return self.name


# # hunting settings
class HuntingArea(models.Model):
    # qouta = models.ForeignKey(
    #     Quota, on_delete=models.CASCADE, related_name="hunting_blocks", null=True
    # )
    # species = models.ManyToManyField(Species)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.ForeignKey(
        Locations,
        on_delete=models.CASCADE,
        related_name="hunting_areas",
        null=True,
        blank=True,
    )
    adress = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Hunting Area"
        db_table = "hunting_areas"

    def __str__(self):
        return self.name


class HuntingQuatasArea(models.Model):
    area = models.ForeignKey(
        HuntingArea, on_delete=models.CASCADE, related_name="hunting_quatas_area"
    )
    quota = models.ForeignKey(
        Quota, on_delete=models.CASCADE, related_name="hunting_quatas_area"
    )

    class Meta:
        verbose_name_plural = "Hunting Quatas Area"
        db_table = "hunting_quatas_area"
        unique_together = ("area", "quota")

    def __str__(self):
        return self.area.name + " - " + self.quota.name


class QuotaHutingAreaSpecies(models.Model):
    species = models.ForeignKey(
        Species, on_delete=models.CASCADE, related_name="quota_hunting_species"
    )
    quota = models.ForeignKey(
        Quota, on_delete=models.CASCADE, related_name="quota_hunting_species"
    )
    area = models.ForeignKey(
        HuntingArea,
        on_delete=models.CASCADE,
        related_name="quota_hunting_species",
        null=True,
        blank=True,
    )
    quantity = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Quota Hunting Species"
        db_table = "quota_hunting_area_species"
        unique_together = ("species", "area", "quota")

    def __str__(self):
        return self.species.name + " - " + self.quota.name


# hunting settings
class SafariPackageType(models.Model):
    TYPES_CHOICES = (
        ("Regular", "Regular Safari"),
        ("Premium", "Premium Safari"),
        ("Major", "Major Safari"),
    )

    name = models.CharField(max_length=100, choices=TYPES_CHOICES, unique=True)
    safari_duration = models.IntegerField(default=0)
    species = models.ManyToManyField(Species, related_name="safari_species")
    hunting_limit = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Safari Package Types"
        db_table = "safari_package_types"

    def __str__(self):
        return self.name


# hunting settings
class HuntingType(models.Model):
    TYPE_CHOICES = (
        ("1x1", "1x1"),
        ("2x1", "2x1"),
        ("3x1", "3x1"),
        ("4x1", "4x1"),
        ("5x1", "5x1"),
        ("6x1", "6x1"),
        ("7x1", "7x1"),
        ("8x1", "8x1"),
        ("9x1", "9x1"),
        ("10x1", "10x1"),
    )
    name = models.CharField(max_length=100, choices=TYPE_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField()

    class Meta:

        verbose_name_plural = "Hunting Types"
        db_table = "hunting_types"

    def __str__(self):
        return self.name


class TrophyFees(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Trophy Fees"
        db_table = "trophy_fees"


class PackageType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Package Types"
        db_table = "package_types"

    def __str__(self):
        return self.name


class CompanionHunterCost(models.Model):
    days = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Companion Hunter Cost"
        db_table = "companion_hunter_cost"

    def __str__(self):
        return str(self.days) + " days - " + str(self.price)


# class Package(models.Model):

#     publication_status = (
#         ("Draft", "Draft"),
#         ("Published", "Published"),
#     )

#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     package_type = models.ForeignKey(
#         SafariPackageType, on_delete=models.CASCADE, related_name="package_type"
#     )
#     hunting_type = models.ForeignKey(
#         HuntingType, on_delete=models.CASCADE, related_name="hunting_type"
#     )
#     hunting_block = models.ForeignKey(
#         HuntingBlock, on_delete=models.CASCADE, related_name="hunting_block"
#     )
#     number_of_hunters = models.IntegerField(default=0)
#     upgrade_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     number_of_days = models.IntegerField(default=0)
#     companion_hunter_cost = models.DecimalField(
#         max_digits=10, decimal_places=2, default=0
#     )
#     # Safari Extras
#     observer_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     change_of_area_fees = models.DecimalField(
#         max_digits=10, decimal_places=2, default=0
#     )
#     baiting_vehicle_cost = models.DecimalField(
#         max_digits=10, decimal_places=2, default=0
#     )
#     firearm_hire_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     wifi_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     is_active = models.BooleanField(default=True)
#     status = models.CharField(
#         max_length=100, choices=publication_status, default="Draft"
#     )
#     species = models.ManyToManyField(
#         SpeciesAvailabilityAndCost, related_name="package_species_list"
#     )
#     created_by = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="created_by"
#     )
#     baiting_vehicle_with_PH_cost = models.DecimalField(
#         max_digits=10, decimal_places=2, default=0
#     )
#     total_cost = models.DecimalField(
#         max_digits=10, decimal_places=2, default=0, editable=False
#     )
#     # trophy_fees_list = models.ManyToManyField(TrophyFees, related_name='trophy_fees_list')

#     class Meta:
#         verbose_name_plural = "Pre-defined Sales Packages"
#         db_table = "pre_defined_sales_packages"

#     def __str__(self):
#         # packe name total cost
#         return self.name + " - " + str(self.total_cost)

#     def save(self, *args, **kwargs):
#         self.total_cost = self.get_total_cost()
#         super(Package, self).save(*args, **kwargs)

#     def extra_fees(self):
#         pass

#     def get_total_cost(self):
#         pass


class Currency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    create_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Currencies"
        db_table = "currencies"

    def __str__(self):
        return self.name


class IdentityType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Identity Types"
        db_table = "identity_types"

    def __str__(self):
        return self.name


class Items(models.Model):
    name = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Items"
        db_table = "items"

    def __str__(self) -> str:
        return self.name


class Nationalities(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Nationalities"
        db_table = "nationalities"

    def __str__(self) -> str:
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True)
    code = models.CharField(max_length=10, null=True)

    class Meta:
        verbose_name_plural = "Countries"
        db_table = "countries"

    def __str__(self) -> str:
        return self.name
