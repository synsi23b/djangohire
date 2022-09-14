from uuid import uuid4
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .forms import UuidForm, ApplicantForm
from .models import Applicant


def index(request):
    request.session.set_test_cookie()
    res = request.session.get("resume", None)
    if res:
        form=UuidForm(initial={"resume":res})
        del request.session["resume"]
    else:
        form=UuidForm()
    return render(request, 'start.html', context={"form":form})


def resume(request):
    if request.method == 'POST':
        if "fresh" in request.POST:
            request.session["resume"] = str(uuid4())
            request.session["step"] = 0
        else:
            form=UuidForm(request.POST)
            if form.is_valid():
                request.session["resume"] = form.data["resume"]
                # find correct step to resume from
                try:
                    applicant = Applicant.objects.get(resume__exact=form.data["resume"])
                    request.session["step"] = applicant.step
                except ObjectDoesNotExist:
                    request.session["step"] = 0
            else:
                return HttpResponse("Error: bad token")
        # overwrite method 
        request.method = "GET"
        return stepper(request)
    # actually error with resume token or something
    #if request.session.test_cookie_worked():
        #request.session.delete_test_cookie()
        #return HttpResponse("You're logged in.")
    #else:
        #pass
        #return HttpResponse("Please enable cookies and try again.")
    return index(request)


def stepper(request):
    step = request.session["step"]
    resu = request.session["resume"]
    try:
        applicant = Applicant.objects.get(resume__exact=resu)
    except ObjectDoesNotExist:
        applicant = None
    newstep, tmpl, ctx = STEPS[step](request, step)
    if newstep != step and applicant is not None:
        request.session["step"] = newstep
        applicant.step = newstep
        applicant.save()
    return render(request, tmpl, context=ctx)


def basic(request, step):
    if request.method == 'POST':
        form = ApplicantForm(request.POST)
        if form.is_valid():
            form.instance.resume = request.session["resume"]
            step += 1
            form.instance.step = step
            form.save()
            request.method = "GET"
            return STEPS[step](request, step)
    else:
        try:
            applicant = Applicant.objects.get(resume__exact=request.session["resume"])
        except ObjectDoesNotExist:
            applicant = None
        if applicant:
            form = ApplicantForm(instance=applicant)
        else:
            form = ApplicantForm()
    return step, 'basic.html', {"form": form}


def finished(request, step):
    return step, 'finished.html', {}

STEPS = [basic, finished]