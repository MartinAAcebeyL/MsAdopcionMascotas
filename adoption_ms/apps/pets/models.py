from djongo import models


class Pets(models.Model):
    campo1 = models.CharField(max_length=255)
    campo2 = models.IntegerField()
    campo3 = models.IntegerField()
