from django.db import models

# Create your models here.
# Deal with Databases

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)

class Reservation(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    number_of_people = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    comments = models.CharField(max_length=255, blank=True)

class SearchN(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    url = models.URLField()
    is_remote = models.BooleanField(default=False)
    # image = models.BinaryField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    