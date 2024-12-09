# Generated by Django 4.2.9 on 2024-10-23 20:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AccommodationType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "verbose_name_plural": "Accommodation Types",
                "db_table": "accommodation_types",
            },
        ),
        migrations.CreateModel(
            name="AdditionalServices",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("service_id", models.CharField(max_length=100, unique=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "payment_model",
                    models.CharField(
                        choices=[
                            ("per_person", "Per Person"),
                            ("daily", "Daily"),
                            ("round", "Round"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "cost_use_case",
                    models.CharField(
                        choices=[("person", "Person"), ("hunter", "Hunter")],
                        max_length=100,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Additional Services",
                "db_table": "additional_services",
            },
        ),
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, null=True, unique=True)),
                ("code", models.CharField(max_length=10, null=True)),
            ],
            options={
                "verbose_name_plural": "Countries",
                "db_table": "countries",
            },
        ),
        migrations.CreateModel(
            name="Currency",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("symbol", models.CharField(max_length=10)),
                (
                    "create_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("updated_date", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "Currencies",
                "db_table": "currencies",
            },
        ),
        migrations.CreateModel(
            name="GeoLocationCoordinates",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "coordinates_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Point", "Point"),
                            ("LineString", "LineString"),
                            ("Polygon", "Polygon"),
                            ("MultiPoint", "MultiPoint"),
                            ("MultiLineString", "MultiLineString"),
                            ("MultiPolygon", "MultiPolygon"),
                        ],
                        default="Point",
                        max_length=100,
                        null=True,
                    ),
                ),
                ("coordinates", models.JSONField(default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                "verbose_name_plural": "Geo Location Coordinates",
                "db_table": "geo_location_coordinates",
            },
        ),
        migrations.CreateModel(
            name="HuntingArea",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField()),
                ("adress", models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                "verbose_name_plural": "Hunting Area",
                "db_table": "hunting_areas",
            },
        ),
        migrations.CreateModel(
            name="HuntingPriceList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("is_active", models.BooleanField(default=True)),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now, null=True),
                ),
                ("updated_date", models.DateTimeField(auto_now=True, null=True)),
                (
                    "area",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hunting_price_list",
                        to="bm_hunting_settings.huntingarea",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_hunting_price_list",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Hunting Price List",
                "db_table": "hunting_price_list",
            },
        ),
        migrations.CreateModel(
            name="HuntingPriceListType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("is_active", models.BooleanField(default=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("duration", models.IntegerField(blank=True, default=0, null=True)),
                (
                    "currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hunting_price_list_type",
                        to="bm_hunting_settings.currency",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Hunting Price List Type",
                "db_table": "hunting_price_list_type",
            },
        ),
        migrations.CreateModel(
            name="HuntingType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
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
                        ],
                        max_length=100,
                        unique=True,
                    ),
                ),
                ("description", models.TextField()),
            ],
            options={
                "verbose_name_plural": "Hunting Types",
                "db_table": "hunting_types",
            },
        ),
        migrations.CreateModel(
            name="IdentityType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
            ],
            options={
                "verbose_name_plural": "Identity Types",
                "db_table": "identity_types",
            },
        ),
        migrations.CreateModel(
            name="Items",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("count", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name_plural": "Items",
                "db_table": "items",
            },
        ),
        migrations.CreateModel(
            name="LocationType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField()),
            ],
            options={
                "verbose_name_plural": "Location Types",
                "db_table": "location_types",
            },
        ),
        migrations.CreateModel(
            name="Nationalities",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "verbose_name_plural": "Nationalities",
                "db_table": "nationalities",
            },
        ),
        migrations.CreateModel(
            name="OperationType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "verbose_name_plural": "Operation Types",
                "db_table": "operation_types",
            },
        ),
        migrations.CreateModel(
            name="Quota",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("create_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("update_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_quotas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Quotas",
                "db_table": "hunting_quotas",
            },
        ),
        migrations.CreateModel(
            name="RegulatoryHuntingpackage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("Regular", "Regular Safari"),
                            ("Premium", "Premium Safari"),
                            ("Major", "Major Safari"),
                        ],
                        max_length=100,
                    ),
                ),
                ("duration", models.IntegerField(default=0)),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now, null=True),
                ),
                ("updated_date", models.DateTimeField(auto_now=True, null=True)),
                (
                    "quota",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="regulatory_hunting_packages",
                        to="bm_hunting_settings.quota",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_regulatory_hunting_packages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Safari Package Types",
                "db_table": "regulatory_hunting_packages",
                "unique_together": {("quota", "name")},
            },
        ),
        migrations.CreateModel(
            name="SalesPackages",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "sales_quota",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sales_packages",
                        to="bm_hunting_settings.quota",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_sales_packages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Seasons",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField()),
            ],
            options={
                "verbose_name_plural": "Seasons",
                "db_table": "seasons",
            },
        ),
        migrations.CreateModel(
            name="Species",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "scientific_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "verbose_name_plural": "Species",
                "db_table": "species",
            },
        ),
        migrations.CreateModel(
            name="SpeciesUnits",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "species",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="species_unis",
                        to="bm_hunting_settings.species",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Species Unis",
                "db_table": "species_units",
            },
        ),
        migrations.CreateModel(
            name="RegulatoryHuntingPackageSpecies",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField(default=0)),
                (
                    "r_hunting_package",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="regulatory_hunting_package_species",
                        to="bm_hunting_settings.regulatoryhuntingpackage",
                    ),
                ),
                (
                    "species",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="regulatory_hunting_package_species",
                        to="bm_hunting_settings.species",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Regulatory Hunting Package Species",
                "db_table": "regulatory_hunting_package_species",
            },
        ),
        migrations.CreateModel(
            name="Locations",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("is_disabled", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "geo_coordinates",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="geo_coordinates",
                        to="bm_hunting_settings.geolocationcoordinates",
                    ),
                ),
                (
                    "location_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="location_type",
                        to="bm_hunting_settings.locationtype",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Locations",
                "db_table": "locations",
            },
        ),
        migrations.CreateModel(
            name="HuntingPriceTypePackage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "create_date",
                    models.DateTimeField(default=django.utils.timezone.now, null=True),
                ),
                ("updated_date", models.DateTimeField(auto_now=True, null=True)),
                (
                    "price_list_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hunting_price_type_package",
                        to="bm_hunting_settings.huntingpricelisttype",
                    ),
                ),
                (
                    "sales_package",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hunting_price_type_package",
                        to="bm_hunting_settings.salespackages",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Hunting Price Type Package",
                "db_table": "hunting_price_type_package",
                "unique_together": {("price_list_type", "sales_package")},
            },
        ),
        migrations.AddField(
            model_name="huntingpricelisttype",
            name="hunting_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="hunting_price_list_type",
                to="bm_hunting_settings.huntingtype",
            ),
        ),
        migrations.AddField(
            model_name="huntingpricelisttype",
            name="price_list",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="hunting_price_list_type",
                to="bm_hunting_settings.huntingpricelist",
            ),
        ),
        migrations.CreateModel(
            name="HuntingPackageUpgradeFees",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("description", models.TextField()),
                (
                    "currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hunting_package_upgrade_fees",
                        to="bm_hunting_settings.currency",
                    ),
                ),
                (
                    "huting_price_list_type_package",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hunting_package_upgrade_fees",
                        to="bm_hunting_settings.huntingpricetypepackage",
                    ),
                ),
                (
                    "species",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hunting_package_upgrade_fees",
                        to="bm_hunting_settings.species",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Hunting Package Upgrade Fees",
                "db_table": "hunting_package_upgrade_fees",
            },
        ),
        migrations.CreateModel(
            name="HuntingPackageCompanionsHunter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("days", models.IntegerField(default=0)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "hunting_price_list_type_package",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hunting_package_companions_hunter",
                        to="bm_hunting_settings.huntingpricetypepackage",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Hunting Package Companions Hunter",
                "db_table": "hunting_package_companions_hunter",
            },
        ),
        migrations.AddField(
            model_name="huntingarea",
            name="location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="hunting_areas",
                to="bm_hunting_settings.locations",
            ),
        ),
        migrations.CreateModel(
            name="SalesPackageSpecies",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField(default=0)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "sales_package",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sales_package_species",
                        to="bm_hunting_settings.salespackages",
                    ),
                ),
                (
                    "species",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sales_package_species",
                        to="bm_hunting_settings.species",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Sales Package Species",
                "db_table": "sales_package_species",
                "unique_together": {("sales_package", "species")},
            },
        ),
        migrations.CreateModel(
            name="QuotaHuntingAreaSpecies",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField(default=0)),
                (
                    "area",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quota_hunting_species",
                        to="bm_hunting_settings.huntingarea",
                    ),
                ),
                (
                    "quota",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quota_hunting_species",
                        to="bm_hunting_settings.quota",
                    ),
                ),
                (
                    "species",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quota_hunting_species",
                        to="bm_hunting_settings.species",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Quota Hunting Species",
                "db_table": "quota_hunting_area_species",
                "unique_together": {("species", "area", "quota")},
            },
        ),
        migrations.CreateModel(
            name="HuntingQuatasArea",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "area",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hunting_quatas_area",
                        to="bm_hunting_settings.huntingarea",
                    ),
                ),
                (
                    "quota",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hunting_quatas_area",
                        to="bm_hunting_settings.quota",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Hunting Quatas Area",
                "db_table": "hunting_quatas_area",
                "unique_together": {("area", "quota")},
            },
        ),
        migrations.AlterUniqueTogether(
            name="huntingpricelisttype",
            unique_together={("price_list", "hunting_type")},
        ),
    ]
