from django.http import Http404
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from utilities import CommonJsonResponse
from ..models import Competency

def competencies(request):
    res = CommonJsonResponse(request)
    competencies = Competency.objects.alive()
    res.set_data(competencies)
    return res.get()

def competency(request,id):
    res = CommonJsonResponse(request)
    competency = get_object_or_404(Competency,pk=id)
    method = request.method.lower()
    if "post" == method:
        return Http404()
    elif "put" == method:
        return Http404()
    elif "delete" == method:
        return Http404()
    elif "option" == method:
        return res.get()
    elif "get" == method:
        res.set_data(competency)
        return res.get()
