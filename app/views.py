from curses.ascii import HT
from uuid import uuid4
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .forms import UuidForm, ApplicantForm
from .models import Applicant


def index(request):
    res = request.session.get("resume", None)
    if res:
        form=UuidForm(initial={"resume":res})
    else:
        form=UuidForm()
        request.session.set_test_cookie()
    return render(request, 'start.html', context={"form":form})


def resume(request):
    if request.method == 'POST':
        form=UuidForm(request.POST)
        if form.is_valid():
            request.session["resume"] = form.data["resume"]
            # TODO find correct step to resume from
            step = basic
            # overwrite method 
            request.method = "GET"
            return step(request)
        else:
            del request.session["resume"]
            return index(request)
    else:
        # actually error with resume token or something
        return index(request)


def basic(request):
    form = None
    if request.method == 'POST':
        form = ApplicantForm(request.POST)
        if form.is_valid():
            form.instance.resume = request.session.get("resume")
            form.save()
            return HttpResponse("Next")
    res = request.session.get("resume", None)
    if res:
        if form is None:
            try:
                appl = Applicant.objects.get(resume__exact=res)
                form = ApplicantForm(instance=appl)
            except ObjectDoesNotExist:
                form = ApplicantForm()
        ctx = {
            "res_token": res,
            "form": form
        }
    else:
        request.session["resume"] = str(uuid4())
        ctx = {
            "res_token": request.session["resume"],
            "form": ApplicantForm()
        }
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            #return HttpResponse("You're logged in.")
        else:
            pass
            #return HttpResponse("Please enable cookies and try again.")
    return render(request, 'basic.html', context=ctx)