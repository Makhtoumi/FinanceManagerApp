from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2 , default=0)

class BalanceTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.description}"

class Categorie(models.Model):
    name = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

class SousCategorie(models.Model):
    name = models.CharField(max_length=25)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True , blank=True)

class HisTransction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.CharField(max_length=50)
    souscategorie = models.CharField (max_length=50,default='')
    descrption = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_in_masrif = models.BooleanField(default=False)  # New field

    def save(self, *args, **kwargs):
        if not self.saved_in_masrif and self.amount < 0:
            # Create a Masrif object with the same attributes and save it
            Masrif.objects.create(
                amount=self.amount*-1,
                categorie=self.categorie,
                souscategorie=self.souscategorie,
                descrption=self.descrption,
                date=self.date,
                user=self.user
            )
            self.saved_in_masrif = True  # Set the flag
        super().save(*args, **kwargs)


class Masrif(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.CharField(max_length=50)
    souscategorie = models.CharField (max_length=50,default='')
    descrption = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.categorie}"
