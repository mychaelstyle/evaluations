from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.forms.models import model_to_dict
from django.db.models import Q
from django.db.models import Prefetch
from django.db.models import Subquery, OuterRef
import inspect

from utilities import CommonJsonResponse
from ..models import TaskEvaluation, TaskEvaluationItem, TaskSkill, TaskFulltext

def search(request):
    res = CommonJsonResponse(request)
    competency_id = request.GET.get("competency",1)
    query = request.GET.get("q",None)
    per_page = request.GET.get("perpage",100)
    page = request.GET.get("page",1)
    queryset = TaskEvaluation.objects.filter(competency_id=competency_id, is_leaf=True).alive()
    queryset_txt = TaskFulltext.objects.alive()
    if query is not None:
        query = query.replace("　"," ")
        queries = query.split(" ")
        for q in queries:
            queryset_txt = queryset_txt.filter(contents__icontains=q)
    queryset = queryset.filter(pk__in=Subquery(queryset_txt.values('task_evaluation'))).all()
    res.set_data(queryset,perpage=per_page,page=page)

    """
    result = TaskEvaluationItem.objects.select_related(
        "task_evaluation","task_evaluation__parent","task_evaluation__parent__parent").prefetch_related(
            Prefetch('task_evaluation', queryset=TaskSkill.objects.select_related("skill_evaluation").alive(), to_attr="task_evaluation__skills")
            ).filter(
            task_evaluation__competency_id=competency_id)
    if query is not None:
        query = query.replace("　"," ")
        queries = query.split(" ")
        for q in queries:
            result = result.filter(Q(name__icontains=q)
                                    | Q(task_evaluation__name__icontains=q)
                                    | Q(task_evaluation__parent__name__icontains=q)
                                    | Q(task_evaluation__parent__parent__name__icontains=q))
    result = result.alive()
    data = {}
    for row in result.all():
        task = row.task_evaluation
        print("--------------")
        for m in inspect.getmembers(task):
            if m[0].startswith("_"):
                continue
            else:
                print(m[0])
        print(task.task_skill_task_evaluation)
        if task.parent is not None:
            if task.parent.parent is not None and task.parent.parent.id not in data:
                data[task.parent.parent.id] = model_to_dict(task.parent.parent)
                data[task.parent.parent.id]["tasks"] = {}
            if task.parent.id not in data[task.parent.parent.id]["tasks"]:
                data[task.parent.parent.id]["tasks"][task.parent.id] = model_to_dict(task.parent)
                data[task.parent.parent.id]["tasks"][task.parent.id]["tasks"] = {}
        if task.id not in data[task.parent.parent.id]["tasks"][task.parent.id]["tasks"]:
            data[task.parent.parent.id]["tasks"][task.parent.id]["tasks"][task.id] = model_to_dict(task)
            data[task.parent.parent.id]["tasks"][task.parent.id]["tasks"][task.id]["items"] = {}
            data[task.parent.parent.id]["tasks"][task.parent.id]["tasks"][task.id]["skills"] = {}
            if hasattr(task,'skills'):
                for skill in task.skills:
                    data[task.parent.parent.id]["tasks"][task.parent.id]["tasks"][task.id]["skills"][skill.skill_evaluation.id] = model_to_dict(skill.skill_evaluation)
        data[task.parent.parent.id]["tasks"][task.parent.id]["tasks"][task.id]["items"][row.id] = model_to_dict(row)
    res.set_data(data,perpage=per_page,page=page)
    """
    return res.get()

def tasks(request):
    res = CommonJsonResponse(request)
    query = request.GET.get("q",None)
    per_page = request.GET.get("perpage",100)
    page = request.GET.get("page",1)
    result = TaskEvaluation.objects.select_related("parent","parent__parent","competency")
    if query is not None:
        query = query.replace("　"," ")
        queries = query.split(" ")
        for q in queries:
            result = result.filter(Q(name__icontains=q) | Q(parent__name__icontains=q) | Q(parent__parent__name__icontains=q))
    result = result.alive()
    res.set_data(result,perpage=per_page,page=page)
    return res.get()

def task(request,id):
    res = CommonJsonResponse(request)
    task_evaluation = get_object_or_404(TaskEvaluation,pk=id)
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
        res.set_data(task_evaluation)
        return res.get()

def task_evaluation_items(request):
    res = CommonJsonResponse(request)
    task_evaluation_items = TaskEvaluationItem.objects.alive()
    res.set_data(task_evaluation_items)
    return res.get()

def task_evaluation_item(request,id):
    res = CommonJsonResponse(request)
    task_evaluation_item = get_object_or_404(TaskEvaluationItem,pk=id)
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
        res.set_data(task_evaluation_item)
        return res.get()

