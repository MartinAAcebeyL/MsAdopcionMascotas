from django.db import models


class PetEntity(models.Model):
    STATUS_CHOICES = [
        ("able", "Able"),
        ("adopted", "Adopted"),
        ("progress", "In Progress"),
    ]
    id = models.CharField(max_length=24, primary_key=True)
    name = models.CharField(max_length=50)
    history = models.TextField()
    age_value = models.IntegerField()
    age_time = models.CharField(max_length=10)
    person = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    sex = models.CharField(max_length=1)
    size = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
