from django import forms
from .models import Applicant, ChildrenProof, IncomeTax, JobOutline, JobDates, WorkPermit, SocialSec


class UuidForm(forms.Form):
    resume = forms.UUIDField(label="Already started your application? Enter your token to continue editing!")


class ApplicantForm(forms.ModelForm):
    template_name = "form_basic.html"
    class Meta:
        model = Applicant
        exclude = ["resume", "step"]


class PermitForm(forms.ModelForm):
    template_name = "form_basic.html"
    class Meta:
        model = WorkPermit
        exclude = ["resume",]


class JobOutlineForm(forms.ModelForm):
    template_name = "form_basic.html"
    class Meta:
        model = JobOutline
        exclude = ["resume",]


class JobDatesForm(forms.ModelForm):
    template_name = "form_basic.html"
    class Meta:
        model = JobDates
        exclude = ["resume",]


class SocialSecForm(forms.ModelForm):
    template_name = "form_basic.html"
    class Meta:
        model = SocialSec
        exclude = ["resume",]


class IncomeTaxForm(forms.ModelForm):
    template_name = "form_basic.html"
    class Meta:
        model = IncomeTax
        exclude = ["resume",]


class ChildrenProofForm(forms.ModelForm):
    template_name = "form_basic.html"
    class Meta:
        model = ChildrenProof
        exclude = ["resume",]

