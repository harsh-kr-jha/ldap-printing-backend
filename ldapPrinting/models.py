from django.db import models
from django.db.models.fields import EmailField
# Create your models here.


class User(models.Model):

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    roll_number = models.CharField(max_length=150, primary_key=True)
    email = EmailField(max_length=254)
    department_name = models.CharField(max_length=150, blank=True, null=True)
    degree_name = models.CharField(max_length=150, blank=True, null=True)
    join_year = models.IntegerField(blank=True, null=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    hostel = models.CharField(max_length=150, blank=True, null=True)
    hostel_name = models.CharField(max_length=150, blank=True, null=True)
    room = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    # objects = BaseUserManager()

    def __str__(self):
        return self.email


class session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=150, primary_key=True)
