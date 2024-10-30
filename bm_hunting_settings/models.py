from django.db import models

# user
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django_countries.fields import CountryField


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
    name = models.CharField(max_length=100, unique=True)
    scientific_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

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
    POINTYPE = (
        ("Point", "Point"),
        ("LineString", "LineString"),
        ("Polygon", "Polygon"),
        ("MultiPoint", "MultiPoint"),
        ("MultiLineString", "MultiLineString"),
        ("MultiPolygon", "MultiPolygon"),
    )

    coordinates_type = models.CharField(
        max_length=100, null=True, blank=True, choices=POINTYPE, default="Point"
    )
    coordinates = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "Geo Location Coordinates"
        db_table = "geo_location_coordinates"


class Locations(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    location_type = models.ForeignKey(
        LocationType, on_delete=models.CASCADE, related_name="location_type", null=True
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

    # def __str__(self):
    #     return self.name


# # hunting settings
class HuntingArea(models.Model):
    # qouta = models.ForeignKey(
    #     Quota, on_delete=models.CASCADE, related_name="hunting_blocks", null=True
    # )
    # species = models.ManyToManyField(Species)
    name = models.CharField(max_length=100, unique=True)
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

    # def __str__(self):
    #     return str(self.name)


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
class RegulatoryHuntingpackage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_regulatory_hunting_packages",
        null=True,
    )
    # quota = models.ForeignKey(
    #     Quota,
    #     on_delete=models.CASCADE,
    #     related_name="regulatory_hunting_packages",
    #     null=True,
    # )

    TYPES_CHOICES = (
        ("Regular", "Regular Safari"),
        ("Premium", "Premium Safari"),
        ("Major", "Major Safari"),
    )

    name = models.CharField(max_length=100, choices=TYPES_CHOICES, unique=True)
    duration = models.IntegerField(default=0)

    created_date = models.DateTimeField(default=timezone.now, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "Safari Package"
        db_table = "regulatory_hunting_packages"

    def __str__(self):
        return self.name


class RegulatoryHuntingPackageSpecies(models.Model):
    r_hunting_package = models.ForeignKey(
        RegulatoryHuntingpackage,
        on_delete=models.CASCADE,
        related_name="regulatory_hunting_package_set",
    )
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="regulatory_hunting_package_species_set",
    )
    quantity = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Regulatory Hunting Package Species"
        db_table = "regulatory_hunting_package_species"

    def __str__(self):
        return self.r_hunting_package.name + " - " + self.species.name


# -----------------------Sales Package------------------------------------------#


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
    description = models.TextField()

    class Meta:

        verbose_name_plural = "Hunting Types"
        db_table = "hunting_types"

    def __str__(self):
        return self.name


class SalesPackages(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_sales_packages",
        null=True,
    )
    sales_quota = models.ForeignKey(
        Quota,
        on_delete=models.CASCADE,
        related_name="sales_packages",
        null=True,
    )
    name = models.CharField(max_length=100)
    description = models.TextField()

    class meta:
        verbose_name_plural = "Sales Packages"

    def __str__(self):
        return self.name


class HuntingPriceList(models.Model):
    area = models.ForeignKey(
        HuntingArea, on_delete=models.CASCADE, related_name="hunting_price_list"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_hunting_price_list",
        null=True,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "Hunting Price List"
        db_table = "hunting_price_list"


class HuntingPriceListType(models.Model):
    price_list = models.ForeignKey(
        HuntingPriceList,
        on_delete=models.CASCADE,
        related_name="hunting_price_list_type",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="hunting_price_list_type"
    )
    hunting_type = models.ForeignKey(
        HuntingType, on_delete=models.CASCADE, related_name="hunting_price_list_type"
    )
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    duration = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Hunting Price List Type"
        db_table = "hunting_price_list_type"
        unique_together = (
            "price_list",
            "hunting_type",
        )

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.hunting_type.name


class HuntingPriceTypePackage(models.Model):
    price_list_type = models.ForeignKey(
        HuntingPriceListType,
        on_delete=models.CASCADE,
        related_name="hunting_price_list_type_package",
    )
    sales_package = models.ForeignKey(
        SalesPackages,
        on_delete=models.CASCADE,
        related_name="hunting_price_type_package",
    )
    create_date = models.DateTimeField(default=timezone.now, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "Hunting Price Type Package"
        db_table = "hunting_price_type_package"
        unique_together = (
            "price_list_type",
            "sales_package",
        )


class Seasons(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Seasons"
        db_table = "seasons"

    def __str__(self):
        return self.name


class SalesPackageSpecies(models.Model):
    sales_package = models.ForeignKey(
        SalesPackages,
        on_delete=models.CASCADE,
        related_name="sales_package_species",
    )
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="sales_package_species",
    )
    quantity = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # currency = models.ForeignKey(
    #     Currency, on_delete=models.CASCADE, related_name="sales_package_species"
    # )

    class Meta:
        verbose_name_plural = "Sales Package Species"
        db_table = "sales_package_species"
        unique_together = (
            "sales_package",
            "species",
        )

    def __str__(self):
        return self.sales_package.name + " - " + self.species.name


class HuntingPackageUpgradeFees(models.Model):
    huting_price_list_type_package = models.ForeignKey(
        HuntingPriceTypePackage,
        on_delete=models.CASCADE,
        related_name="hunting_package_upgrade_fees",
    )
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="hunting_package_upgrade_fees",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="hunting_package_upgrade_fees"
    )
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Hunting Package Upgrade Fees"
        db_table = "hunting_package_upgrade_fees"

    def __str__(self):
        return (
            self.huting_price_list_type_package.price_list_type.name
            + " - "
            + self.species.name
        )


class HuntingPackageCustomization(models.Model):
    hunting_price_list_type_package = models.ForeignKey(
        HuntingPriceTypePackage,
        on_delete=models.CASCADE,
        related_name="hunting_package_customization",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    hunting_type = models.ForeignKey(
        HuntingType,
        on_delete=models.CASCADE,
        related_name="hunting_package_customized_hunting_type_set",
    )
    area = models.ForeignKey(
        HuntingArea,
        on_delete=models.CASCADE,
        related_name="hunting_package_customized_area_set",
        null=True,
        blank=True,
    )
    season = models.ForeignKey(
        Seasons,
        on_delete=models.CASCADE,
        related_name="hunting_package_customized_season_set",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Hunting Package Customization"
        db_table = "sales_package_customization"

    def __str__(self):
        return self.hunting_price_list_type_package.price_list_type.name


class HuntingPackageCustomizedSpecies(models.Model):
    hunting_package_customization = models.ForeignKey(
        HuntingPackageCustomization,
        on_delete=models.CASCADE,
        related_name="hunting_package_customized_set",
    )
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="hunting_package_customized_species_set",
    )
    quantity = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    description = models.TextField()

    class Meta:
        verbose_name_plural = "Hunting Package Customized Species"
        db_table = "hunting_package_customized_species"

    def __str__(self):
        return self.hunting_package_customization.name + " - " + self.species.name


class HuntingPackageCompanionsHunter(models.Model):
    hunting_price_list_type_package = models.ForeignKey(
        HuntingPriceTypePackage,
        on_delete=models.CASCADE,
        related_name="hunting_package_companions_hunter",
    )
    days = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Hunting Package Companions Hunter"
        db_table = "hunting_package_companions_hunter_cost"

    def __str__(self):
        return (
            self.hunting_price_list_type_package.price_list_type.name
            + " - "
            + str(self.days)
        )


class HuntingPackageOberverHunter(models.Model):
    hunting_price_list_type_package = models.ForeignKey(
        HuntingPriceTypePackage,
        on_delete=models.CASCADE,
        related_name="hunting_package_oberver_hunter",
    )
    days = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Hunting Package Oberver Hunter"
        db_table = "hunting_package_oberver_hunter_cost"


class AdditionalServices(models.Model):
    PAYMENT_MODEL = (
        ("per_person", "Per Person"),
        ("daily", "Daily"),
        ("round", "Round"),
    )
    COST_USER_CASE = (
        ("person", "Person"),
        ("hunter", "Hunter"),
    )

    service_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_model = models.CharField(max_length=100, choices=PAYMENT_MODEL)
    cost_use_case = models.CharField(max_length=100, choices=COST_USER_CASE)

    class Meta:
        verbose_name_plural = "Additional Services"
        db_table = "additional_services"

    def __str__(self):
        return self.service_id


# ------------------------ end of Sales Package-#---------------------------#


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
