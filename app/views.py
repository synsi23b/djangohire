from django.shortcuts import render
from django.http import HttpResponse

from pathlib import Path

def index(request):
    return render(request, 'base.html', context={})