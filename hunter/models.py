from django.db import models
from django.contrib.auth.models import User

# himting settings  
class Species(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()    

    class Meta:
        verbose_name_plural = 'Species'
        db_table = 'bm_species'

    def __str__(self):
        return self.name
    
# himting settings  
class HuntingBlock(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    class Meta:
        verbose_name_plural = 'Hunting Blocks'
        db_table = 'bm_hunting_blocks'

    def __str__(self):
        return self.name
# himting settings  
class Quota(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='quotas')
    hunting_limit = models.IntegerField(default=0)
    hunting_block = models.ForeignKey(HuntingBlock, on_delete=models.CASCADE, related_name='quotas')
    class Meta:
        verbose_name_plural = 'Quotas'
        db_table = 'bm_quotas'

    def __str__(self):  

        return self.name


# Hunter Information:
# Hunter Name
# Passport Number
# Passport Copy (attached)
# Passport Photo (attached)

class Hunter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hunter')
    passport_number = models.CharField(max_length=100)
    passport_copy = models.FileField(upload_to='passport_copy/')
    passport_photo = models.ImageField(upload_to='passport_photo/')

    class Meta:
        verbose_name_plural = 'Hunters'
        db_table = 'bm_hunters'    

    def __str__(self):
        return self.user.username   
    

# Observer Information:
# Observer Name
# Passport Number
# Observer’s Passport Copy (attached)

    
class Observer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='observer')
    observer_name = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=100)
    passport_copy = models.FileField(upload_to='passport_copy/')

    class Meta: 
        verbose_name_plural = 'Observers'
        db_table = 'bm_observers'



    def __str__(self):
        return self.user.username 
    

#  Hunting Safari package
# Regular Safari
# Premium Safari
# Major Safari

# himting settings  
class SafariPackageType(models.Model):
    TYPES_CHOICES = (
        ('Regular', 'Regular Safari'     ),
        ('Premium', 'Premium Safari'),
        ('Major', 'Major Safari'),
    )
    
    name = models.CharField(max_length=100, choices=TYPES_CHOICES)

    class Meta:
        verbose_name_plural = 'Safari Package Types'
        db_table = 'bm_safari_package_types'


    def __str__(self):
        return self.name  
    
# himting settings  
class SafariPackageHuntingSpeciesLimit(models.Model):
    package_type = models.ForeignKey(SafariPackageType, on_delete=models.CASCADE, related_name='limits_species')
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='limits_species')
    hunting_limit = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Safari Package Hunting Species Limits'
        db_table = 'bm_safari_package_hunting_species_limits'

    def __str__(self):
        return self.package_type.name + " - " + self.species.name + " - " + str(self.hunting_limit)


# himting settings  
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
    description = models.TextField()

    class Meta:
     
        verbose_name_plural = 'Hunting Types'
        db_table = 'bm_hunting_types'

    def __str__(self):
        return self.name
    
# himting settings  
class HuntingDays(models.Model):
    days_in_number = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = 'Hunting Days'
        db_table = 'bm_hunting_days'

    def __str__(self):
        return str(self.day_in_number)
    
# himting settings  
class BushmanHuntingScope(models.Model):
    """
    Determine by Quota and number of species remaning in quota and Busman Hunting  strategic plan
    """
    block = models.ForeignKey(HuntingBlock, on_delete=models.CASCADE, related_name='bushman_hunting_scope')
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='bushman_hunting_scope')
    hunting_limit = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = 'Bushman Hunting Scopes'
        db_table = 'bm_bushman_hunting_scopes'

    def __str__(self):
        return self.block.name + " - " + self.species.name + " - " + str(self.hunting_limit)



class HunterHuntingDetails(models.Model):
    hunter = models.ForeignKey(Hunter, on_delete=models.CASCADE, related_name='hunting_details')
    hunting_block = models.ForeignKey(HuntingBlock, on_delete=models.CASCADE, related_name='hunting_block')
    outfitter = models.CharField(max_length=100)
    hunt_days = models.ForeignKey(HuntingDays, on_delete=models.CASCADE, related_name='hunt_days')
    hunt_type = models.ForeignKey(HuntingType, on_delete=models.CASCADE, related_name='hunting_type')
    species_to_be_hunted = models.ManyToManyField(
        BushmanHuntingScope
    )
    start_date = models.DateField()
    end_date = models.DateField()
    class Meta:
        verbose_name_plural = 'Hunt Details'
        db_table = 'bm_hunt_details'
    def __str__(self):
        return self.hunter.user.username
            




  
    



