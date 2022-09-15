from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

SEX_CHOICES = [
    ("M", _("Male")),
    ("F", _("Female")),
    ("D", _("Diverse"))
]


NATIONALITY = [
    ("AUS", _("Austria")),
    ("BEL", _("Belgium")),
    ("BGR", _("Bulgaria")),
    ("CRO", _("Croatia")),
    ("CYP", _("Cyprus")),
    ("CZE", _("Czech Republic")),
    ("DNK", _("Denmark")),
    ("EST", _("Estonia")),
    ("FIN", _("Finland")),
    ("FRA", _("France")),
    ("DEU", _("Germany")),
    ("GRC", _("Greece")),
    ("HUN", _("Hungary")),
    ("ISL", _("Iceland")),
    ("IRE", _("Ireland")),
    ("ITA", _("Italy")),
    ("LVA", _("Latvia")),
    ("LIE", _("Liechtenstein")),
    ("LTU", _("Lithuania")),
    ("LUX", _("Luxembourg")),
    ("MAL", _("Malta")),
    ("NOR", _("Norway")),
    ("NLD", _("Netherlands")),
    ("POL", _("Poland")),
    ("POR", _("Portugal")),
    ("ROM", _("Romania")),
    ("SVK", _("Slovakia")),
    ("SVN", _("Slovenia")),
    ("SPA", _("Spain")),
    ("SWE", _("Sweden")),
    ("CHE", _("Switzerland")),
    ("OTH", _("Other"))
]


class Applicant(models.Model):
    resume = models.UUIDField()
    step = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(_("First Name"), max_length=127)
    lastname = models.CharField(_("Last Name"), max_length=127)
    birth = models.DateField(_("Birthday YYYY-MM-DD"))
    email = models.EmailField(_("E-Mail"), max_length=127)
    nationality = models.CharField(_("Nationality"), max_length=3, choices=NATIONALITY)
    nation_other = models.CharField(_("In case of nationality other then EWR+ please provide it here"), max_length=63, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)

