from django.db import models
# user
from django.contrib.auth.models import User

# hunting settings  
class Quota(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    class Meta:
        verbose_name_plural = 'Quotas'
        db_table = 'quotas'

    def __str__(self):  

        return self.name
    
# hunting settings  
class Species(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()    

    class Meta:
        verbose_name_plural = 'Species'
        db_table = 'species'

    def __str__(self):
        return self.name
    
# hunting settings  
class HuntingBlock(models.Model):
    qouta = models.ForeignKey(Quota, on_delete=models.CASCADE, related_name='hunting_blocks', null=True)
    species = models.ManyToManyField(Species)
    name = models.CharField(max_length=100)
    description = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField( null=True, blank=True)
    adress = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        verbose_name_plural = 'Hunting Blocks'
        db_table = 'hunting_blocks'

    def __str__(self):
        return self.name
    
# hunting settings  
class BlockHuntingSpeciesLimit(models.Model):
    hunting_block = models.ForeignKey(HuntingBlock, on_delete=models.CASCADE, related_name='limits_species')
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='limits_species')
    hunting_limit = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Safari Package Hunting Species Limits'
        db_table = 'block_hunting_species_limits'


    def __str__(self):
        return self.hunting_block.name + " - " + self.species.name + " - " + str(self.hunting_limit)


# hunting settings  
class SafariPackageType(models.Model):
    TYPES_CHOICES = (
        ('Regular', 'Regular Safari'),
        ('Premium', 'Premium Safari'),
        ('Major', 'Major Safari'),
    )
    
    name = models.CharField(max_length=100, choices=TYPES_CHOICES)
    safari_duration = models.IntegerField(default=0)
    Species = models.ManyToManyField(Species, related_name='safari_species')
    hunting_limit = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Safari Package Types'
        db_table = 'safari_package_types'


    def __str__(self):
        return self.name  
    


# hunting settings  
class HuntingType(models.Model):
    TYPE_CHOICES = (
        ('1x1', '1x1'),
        ('2x1', '2x1'),
        ('3x1', '3x1'),
        ('4x1', '4x1'),
        ('5x1', '5x1'),
        ('6x1', '6x1'),
        ('7x1', '7x1'),
        ('8x1', '8x1'),
        ('9x1', '9x1'),
        ('10x1', '10x1'),
    )
    name = models.CharField(max_length=100, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)    
    description = models.TextField()

    class Meta:
     
        verbose_name_plural = 'Hunting Types'
        db_table = 'hunting_types'

    def __str__(self):
        return self.name
    


# Bushman Safari Trackers Limited – Pre-defined Sales Packages .
# 
# 1. 10 Days Buffalo & Plains Game (Low Season)
# Area: Maswa North Game Reserve (MS)
# Safari Model: 1x1
# Cost: $400
# Upgrade Fees: +$5000 for 4th Buffalo (plus trophy fees)
# Species to be Hunted: Buffalo & Plains Game
# Number SP to be hunted: 1
# Companion Hunter Cost: $1900 (for 10 days)
# Safari Extras:
# Observer: $50 per person/day
# Change of Area Fees: $200
# Baiting Vehicle: $900
# Firearm Hire: $10 per day
# WIFI Charges: $3 per day
# Trophy Fees:
# 1st Buffalo: $100
# 2nd Buffalo: $300
# 3rd Buffalo: $500


class TrophyFees(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Trophy Fees'
        db_table = 'trophy_fees'

class PackageType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    class Meta:
        verbose_name_plural = 'Package Types'
        db_table = 'package_types'
    def __str__(self):
        return self.name
    


class CompanionHunterCost(models.Model):
    days = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        verbose_name_plural = 'Companion Hunter Cost'
        db_table = 'companion_hunter_cost'  
    def __str__(self):
        return str(self.days) + " days - " + str(self.price)
    
class SpeciesAvailabilityAndCost(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='species_availability_and_cost')
    availability = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    hunting_block = models.ForeignKey(HuntingBlock, on_delete=models.CASCADE, related_name='species_availability_and_cost')
    class Meta:
        verbose_name_plural = 'Species Availability and Cost'
        db_table = 'package_species_availability_and_cost'
    def __str__(self):
        return self.species.name + " - " + str(self.availability) + " - " + str(self.price)
        

class Package(models.Model):
    publication_status = (
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    package_type = models.ForeignKey(SafariPackageType, on_delete=models.CASCADE, related_name='package_type')
    hunting_type = models.ForeignKey(HuntingType, on_delete=models.CASCADE, related_name='hunting_type')
    hunting_block = models.ForeignKey(HuntingBlock, on_delete=models.CASCADE, related_name='hunting_block')
    number_of_hunters = models.IntegerField(default=0)
    upgrade_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    number_of_days = models.IntegerField(default=0)
    companion_hunter_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Safari Extras
    observer_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    change_of_area_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    baiting_vehicle_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    firearm_hire_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    wifi_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=100, choices=publication_status, default='Draft')
    species = models.ManyToManyField(SpeciesAvailabilityAndCost, related_name='package_species_list')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    baiting_vehicle_with_PH_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    trophy_fees_list = models.ManyToManyField(TrophyFees, related_name='trophy_fees_list')


    class Meta:
        verbose_name_plural = 'Pre-defined Sales Packages'
        db_table = 'pre_defined_sales_packages'

    def __str__(self):
        # packe name total cost
        return self.name + " - " + str(self.total_cost)
    
    def save(self, *args, **kwargs):
        self.total_cost = self.get_total_cost()
        super(Package, self).save(*args, **kwargs)

    def extra_fees(self):
        return self.observer_cost + self.change_of_area_fees + self.baiting_vehicle_cost + self.firearm_hire_cost + self.wifi_charges
    
    def trophy_fees(self):  
        return sum([trophy.price for trophy in self.trophy_fees_list.all()])

    def get_total_cost(self):
        return self.upgrade_fees + self.companion_hunter_cost + self.extra_fees() + self.trophy_fees() + self.professional_hunter_cost
    



    

