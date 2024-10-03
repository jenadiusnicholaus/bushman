from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils import timezone

from bm_hunting_settings.models import Package


class ClientType(models.Model):
    TYPE_CHOICES = (        
        ('Hunter', 'Hunter'),
        ('Companion', 'Companion'),
        ('Observer', 'Observer'),
        )    
    client_type = models.CharField(max_length=100, choices=TYPE_CHOICES)

    class Meta:
        verbose_name_plural = 'Client Types'        
        db_table = 'client_types'

    def __str__(self):
        return self.client_type


class Client(models.Model):
    passport_number = models.CharField(max_length=100, unique=True)
    client_type = models.ForeignKey(ClientType, on_delete=models.CASCADE, related_name='clients', null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email_address = models.EmailField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    country = CountryField(null=True,)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    create_date = models.DateTimeField(default=timezone.now)    
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clients'    

    def __str__(self):
        return self.first_name





    
class ClientDocument(models.Model):

    DocTYpe = ( 
        ('Passport_Copy', 'Travel Packet(Passport Copy)'),
        ("Passport_Photo", "Travel Packet(Passport  Photo"),
        ('Visa', 'Visa'),
        ('Gun Permits', 'Gun Permits'),
        ('CITES Documentation', 'CITES Documentation'),
    )    
    document_type = models.CharField(max_length=100, choices=DocTYpe)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='hunder_documents')
    document = models.FileField(upload_to='documents/')
    class Meta:
        verbose_name_plural = 'Client Documents'
        db_table = 'client_documents'

    def __str__(self):
       return self.client.first_name + " - " + self.document_type + " - " + self.document.name
    

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
        verbose_name_plural = 'Weapons'
        db_table = 'weapons'

    def __str__(self):
        return self.owner + " - " + self.brand + " - " + self.caliber + " - " + self.serial_number + " - " + str(self.ammo_quantity) + " - " + self.maker_number + " - " + self.weapon_owner
    


class HunterItinerary(models.Model):
    hunter = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='hunter_itinerary')
    airport_arrival = models.CharField(max_length=100)
    airport_departure = models.CharField(max_length=100)
    charter_flight_arrangements = models.TextField()
    hotel_bookings = models.TextField(
        help_text="Number of rooms and types required"
    )
    arrival_date = models.DateField()
    departure_date = models.DateField()
    class Meta:
        verbose_name_plural = 'client Itineraries'
        # db_table = 'client_itineraries'

    def __str__(self):
        return self.hunter.user.username + " - " + self.airport_arrival + " - " + self.airport_departure + " - " + self.charter_flight_arrangements + " - " + self.hotel_bookings + " - " + str(self.arrival_date) + " - " + str(self.departure_date)
    


class ClientPreferences(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_preferences')
    food_preferences = models.TextField()
    beverage_preferences = models.TextField()
    allergies = models.TextField()
    alcohol_preferences = models.TextField()
    clothing_gear_needs = models.TextField()
    special_requests = models.TextField()
    class Meta:
        verbose_name_plural = 'Client Preferences'
        db_table = 'client_preferences'


    def __str__(self):
        return self.client.first_name + " - " + self.food_preferences + " - " + self.beverage_preferences + " - " + self.allergies + " - " + self.alcohol_preferences + " - " + self.clothing_gear_needs + " - " + self.special_requests
    
class ClinetSalesOrder(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sales_orders')
    order_number = models.CharField(max_length=100)
    order_date = models.DateField()
    
    package = models.ManyToManyField(Package, related_name='sales_order_package')
    class Meta:
        verbose_name_plural = 'Sales Orders'
        db_table = 'client_sales_orders'
    def __str__(self):
        return self.client.first_name + " - " + self.order_number + " - " + str(self.order_date)



# hunting settings  
class HuntingClientLicense(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='hunting_license')
    license_number = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    licence_document = models.FileField(upload_to='documents/')
    class Meta:
        verbose_name_plural = 'Hunting Licenses'
        db_table = 'client_hunting_licenses'

    def __str__(self):
        return self.client.first_name + " - " + self.license_number + " - " + str(self.issue_date) + " - " + str(self.expiry_date) + " - " + self.licence_document.name








            




  
    



