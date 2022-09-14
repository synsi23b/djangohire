from django import forms
from .models import Applicant


class UuidForm(forms.Form):
    resume = forms.UUIDField(label="Already started your application? Enter your token to continue editing!")


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        exclude = ["resume"]