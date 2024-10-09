from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class UserProfile(models.Model):
    gender_choices = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", null=True, blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        choices=gender_choices, max_length=6, null=True, blank=True
    )
    photo = models.ImageField(upload_to="profile_photos", null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    country = CountryField(null=True)
    passport_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        db_table = "bm_user_profile"

    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return self.passport_number
