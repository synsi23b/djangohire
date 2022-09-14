from django.db import models

# Create your models here.

SEX_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
    ("D", "Diverse")
]


class Applicant(models.Model):
    resume = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField("First Name", max_length=127)
    lastname = models.CharField("Last Name", max_length=127)
    birth = models.DateField("Birthday")
    email = models.EmailField("E-Mail", max_length=127)
    nationality = models.TextField("Nationality", max_length=63)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
