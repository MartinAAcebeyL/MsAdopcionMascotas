from django.db import models


class AdoptionEntity(models.Model):
    STATUS_CHOICES = [
        ("adopted", "Adopted"),
        ("progress", "In Progress"),
        ("rejected", "Rejected"),
    ]
    _id = models.CharField(max_length=24)
    pet_id = models.CharField(max_length=24)
    user_id = models.CharField(max_length=24)
    owner_id = models.CharField(max_length=24)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
