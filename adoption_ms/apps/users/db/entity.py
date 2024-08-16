from django.db import models


class UserComplementaryInfo(models.Model):
    # user complementary information
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    birth_date = models.DateField
    identity_document = models.CharField(max_length=50)
    class Meta:
        abstract = True


class UserAuxiliar(UserComplementaryInfo):
    # basic user information
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    is_institute = models.BooleanField(default=False)
    login_type = models.CharField(max_length=100)
