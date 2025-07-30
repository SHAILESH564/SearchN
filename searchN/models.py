from django.db import models

# Create your models here.
# Deal with Databases

class SearchN(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    url = models.URLField()
    is_remote = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    