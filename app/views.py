from uuid import uuid4
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from pathlib import Path
from .forms import ChildrenProofForm, IncomeTaxForm, JobDatesForm, JobOutlineForm, PermitForm, SocialSecForm, UuidForm, ApplicantForm
from .models import Applicant




def index(request):
    request.session.set_test_cookie()
    res = request.session.get("resume", None)
    if res:
        form=UuidForm(initial={"resume":res})
    else:
        form=UuidForm()
    return render(request, 'start.html', context={"form":form})


def resume(request):
    if request.method == 'POST':
        if "fresh" in request.POST:
            request.session["resume"] = str(uuid4())
            request.session["step"] = 1
        else:
            form=UuidForm(request.POST)
            if form.is_valid():
                request.session["resume"] = form.data["resume"]
                # find correct step to resume from
                try:
                    applicant = Applicant.objects.get(resume__exact=form.data["resume"])
                    request.session["step"] = applicant.step
                except ObjectDoesNotExist:
                    request.session["step"] = 1
            else:
                return HttpResponse(_("Error: bad token, try again or start new"))
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


def _jump(request, resu):
    if request.method == 'POST' and "jump" in request.POST:
        jump = int(request.POST["jump"])
        try:
            applicant = Applicant.objects.get(resume__exact=resu)
            if jump <= applicant.step:
                request.session["step"] = jump
                request.method = "GET"
            else:
                return _("Could not switch to step %d! You need to complete the steps in order." % jump)
        except:
            request.method = "GET"
            return _("Could not switch to step %d! You need to complete the steps in order." % jump)


def stepper(request):
    resu = request.session["resume"]
    jump_warn = _jump(request, resu)
    step = request.session["step"]
    
    ctx = STEPS[step-1](request)
    ctx["jump_warn"] = jump_warn
    newstep = request.session["step"]
    if newstep > step:
        applicant = Applicant.objects.get(resume__exact=resu)
        applicant.step = newstep
        applicant.save()
    ctx["res_token"] = resu
    ctx["step"] = newstep
    if not "submit" in ctx:
        ctx["submit"] = _("Submit")
    ctx["steps_verbose"] = STEPS_VERBOSE
    return render(request, "step.html", context=ctx)


def _basic_form_process(request, form_class, on_valid, greeting, explenation="", js=""):
    if request.method == 'POST':
        if "file" in form_class.base_fields:
            form = form_class(request.POST, request.FILES)
        else:
            form = form_class(request.POST)
        if form.is_valid() and on_valid(request, form):
            resu = request.session["resume"]
            form.instance.resume = resu
            try:
                obj = type(form.instance).objects.get(resume__exact=resu)
                form.instance.pk = obj.pk
                form.instance.created_at = obj.created_at
            except:
                pass
            form.save()
            request.method = "GET"
            step = request.session["step"]
            return STEPS[step-1](request)
    else:
        form = _get_resume_obj_form(request, form_class)
    return {"form": form, "greeting": greeting, "explenation": explenation, "injected_js": js}


def _get_resume_obj_form(request, form_class):
    try:
        applicant = form_class.Meta.model.objects.get(resume__exact=request.session["resume"])
    except ObjectDoesNotExist:
        applicant = None
    if applicant:
        form = form_class(instance=applicant)
    else:
        form = form_class()
    return form


def _store_file(request):
    files = request.FILES.getlist('file')
    folder = Path(f"uploads/{request.session['resume']}")
    folder.mkdir(parents=True, exist_ok=True)
    for f in files:
        with open(str(folder / f.name), 'wb+') as dest:
            for chunk in f.chunks():
                dest.write(chunk)


def basic(request):
    greet = _("""First, please provide some basic information about yourself.""")
    #expl = _("""Here you can see your transmitted data: (NOT YET IMPLEMENTED)""")
    def _valid(req, frm):
        frm.instance.resume = req.session["resume"]
        if frm.instance.nationality == "OTH":
            req.session["step"] += 1
        else:
            req.session["step"] += 2
        return True
    ctx = _basic_form_process(request, ApplicantForm, _valid, greet, "", "form_attach_toggle_nationality();")
    return ctx


def permit(request):
    applicant = Applicant.objects.get(resume__exact=request.session["resume"])
    if applicant.nationality != "OTH":
        request.session["step"] += 1
        return STEPS[request.session["step"]-1](request)
    greet = _("""As your nationality is not within the EGR or Swiss, please provide your working permit.""")
    #expl = _("""Here you can see your transmitted data: (NOT YET IMPLEMENTED)""")
    def _valid(req, frm):
        _store_file(req)
        req.session["step"] += 1
        return True
    ctx = _basic_form_process(request, PermitForm, _valid, greet)
    return ctx


def job_outline(request):
    greet = _("""The outline of the job you are applying for.""")
    def _valid(req, frm):
        req.session["step"] += 1
        return True
    ctx = _basic_form_process(request, JobOutlineForm, _valid, greet)
    return ctx


def job_dates(request):
    greet = _("""The start and end time you are planing to work for.""")
    def _valid(req, frm):
        req.session["step"] += 1
        return True
    ctx = _basic_form_process(request, JobDatesForm, _valid, greet)
    return ctx


def socialsec(request):
    greet = _("""Some information regarding details of your social security.""")
    def _valid(req, frm):
        req.session["step"] += 1
        return True
    ctx = _basic_form_process(request, SocialSecForm, _valid, greet)
    return ctx


def incometax(request):
    greet = _("""Please provide details about your income tax.""")
    expl = _("""Enter information here only if the income tax card is actually available""")
    def _valid(req, frm):
        if frm.instance.children:
            req.session["step"] += 1
        else:
            req.session["step"] += 2
        return True
    ctx = _basic_form_process(request, IncomeTaxForm, _valid, greet, expl)
    return ctx


def children(request):
    greet = _("""Please submit a file proofing your children.""")
    def _valid(req, frm):
        _store_file(req)
        req.session["step"] += 1
        return True
    ctx = _basic_form_process(request, ChildrenProofForm , _valid, greet)
    return ctx


def finished(request):
    greet = _("""You are done filling out, you will here from us soon!""")
    expl = _("""Here you can see your transmitted data: (NOT YET IMPLEMENTED)""")
    return {"greeting": greet, "explenation": expl }


STEPS = [basic, permit, job_outline, job_dates, socialsec, incometax, children, finished]
STEPS_VERBOSE = [_("Basics"), _("Work permit"), _("Job description"), _("Dates"), _("Social security"), _("Income tax"), _("Proof of children"), _("Finished")]