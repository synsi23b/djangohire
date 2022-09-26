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
    phone = models.CharField(_("Phone Number"), max_length=63)
    nationality = models.CharField(_("Nationality"), max_length=3, choices=NATIONALITY)
    nation_other = models.CharField(_("In case of nationality other then EWR+ please provide it here"), max_length=63, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    education = models.CharField(_("School education / degree"), max_length=63)
    training = models.CharField(_("Preofessional training (if applicable)"), max_length=63, blank=True)


class WorkPermit(models.Model):
    resume = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    #title = models.CharField(max_length=127)
    file = models.FileField()


PAYROLL = [
    ("SAL", _("Salaried employee")),
    ("TRN", _("Trainee (salaried)")),
    ("MRH", _("Marginal help (salaried)")),
    ("SRT", _("Short term (salaried)")),
    ("WST", _("Working student")),
    ("COM", _("Commercial")),
    ("TRC", _("Trainee (commercial)")),
    ("MRC", _("Marginal help (commercial)")),
    ("SRC", _("Short term (commercial)"))
]


class JobOutline(models.Model):
    resume = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    jobtitle = models.CharField(_("Exact Job Title"), max_length=127)
    association = models.CharField(_("Trade association / Hazard tariff key"), max_length=127)
    hours = models.FloatField(_("Hours per week"))
    payrolltype = models.CharField(_("Payroll type"), max_length=3, choices=PAYROLL)
    salary = models.FloatField(_("Salary"))


class JobDates(models.Model):
    resume = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    start = models.DateField(_("Start Date YYYY-MM-DD"))
    end = models.DateField(_("End Date YYYY-MM-DD (if known)"), blank=True, null=True)


class SocialSec(models.Model):
    resume = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    insurance = models.CharField(_("Health insurance company"), max_length=127)
    socialsec = models.CharField(_("Social security number"), max_length=63, blank=True, null=True)
    birthplace = models.CharField(_("Birth name and Birthplace"), max_length=127, blank=True, null=True)


SLIDEPAY = [
    ("DontApp", _("Do not apply sliding pay scale (remuneration over 800 €)")),
    ("NoTopUp", _("Apply sliding pay scale, without top-up pension insurance")),
    ("TopUp", _("Apply sliding pay scale, with top-up pension insurance")),
]


class IncomeTax(models.Model):
    resume = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(_("Income Tax card is available"), default=True)
    bracket = models.CharField(_("Tax bracket"), max_length=63, blank=True)
    children = models.BooleanField(_("Children"))
    religion = models.CharField(_("Religious denomination"), max_length=63)
    exempt_year = models.FloatField(_("tax allowance per year"), blank=True, default=0.0)
    exempt_month = models.FloatField(_("tax allowance per month"), blank=True, default=0.0)
    finoffice = models.CharField(_("Tax office"), max_length=255, blank=True)
    taxnum = models.CharField(_("Tax identification number"), max_length=63, blank=True)
    lumptax = models.BooleanField(_("2% lump-sum taxation for marginal employees (if no income tax card is available)"))
    payslide = models.CharField(_("Sliding pay scale"), max_length=7, choices=SLIDEPAY)

class ChildrenProof(models.Model):
    resume = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    #title = models.CharField(max_length=127)
    file = models.FileField()
