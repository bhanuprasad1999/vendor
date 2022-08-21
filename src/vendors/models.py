from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Skills(models.Model):
    id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.skill_name

class VendorModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True)
    skills = models.ManyToManyField(Skills)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        db_table = 'vendor_details'

    def __str__(self):
        return self.name
