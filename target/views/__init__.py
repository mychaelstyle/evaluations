from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import check_password
from django.contrib import messages

from . import api

from competency.models import TaskEvaluationTaskProfile, TaskSkill
from ..models import Target
from ..forms import TargetTaskEvaluationItemActionCreateForm

# Create your views here.

def target(request,uuid:str):
    target = Target.objects.prefetch_related('items','items__item').filter(uuid=uuid).first()
    if target is None:
        raise Http404('Not found!')
    if request.method.lower() == "post":
        pass
    elif request.method.lower() == "put":
        pass
    elif request.method.lower() == "delete":
        pass
    elif request.method.lower() == "option":
        pass

    item_relations = target.items.prefetch_related('actions').select_related('item','item__task_evaluation').all()
    tasks = {}
    task_ids = []
    for item_relation in item_relations:
        task = item_relation.item.task_evaluation
        if task.id not in task_ids:
            task_ids.append(task.id)
        if task.id not in tasks:
            tasks[task.id] = {"task":task}
            tasks[task.id]["items"] = []
        tasks[task.id]["items"].append(item_relation)
    profiles = TaskEvaluationTaskProfile.objects.filter(task_evaluation_id__in=task_ids).all()
    for profiler in profiles:
        task_id = profiler.task_evaluation.id
        profile = profiler.task_profile
        if "profiles" not in tasks[task_id]:
            tasks[task_id]["profiles"] = []
        tasks[task_id]["profiles"].append(profile)
    skills = TaskSkill.objects.filter(task_evaluation_id__in=task_ids).select_related('skill_evaluation').prefetch_related('skill_evaluation__knowledges').all()
    for skillrow in skills:
        task_id = skillrow.task_evaluation.id
        skill = skillrow.skill_evaluation
        if "skills" not in tasks[task_id]:
            tasks[task_id]["skills"] = []
        tasks[task_id]["skills"].append(skill)
    action_form = TargetTaskEvaluationItemActionCreateForm()
    return render(request, 'target.html', {'target':target, 'tasks':tasks, 'action_form':action_form})

def add_action(request,uuid:str):
    """目標設定にアクション項目を追加します

    Args:
        request (_type_): _description_
        uuid (str): _description_
    """
    target = Target.objects.prefetch_related('items','items__item').filter(uuid=uuid).first()
    form = TargetTaskEvaluationItemActionCreateForm(request.POST)
    if target is None:
        raise Http404('Not found!')
    if len(target.passcode)>0:
        passcode = request.POST.get('passcode', None)
        if passcode is None or len(passcode)==0:
            messages.error(request,_("passcode_is_required"))
            return redirect("show-target",uuid)
        elif not check_password(passcode,target.passcode):
            messages.error(request,_("passcode_is_invalid"))
            return redirect("show-target",uuid)
        
    if form.is_valid():
        form.save()
    else:
        messages.error(request,form.errors)
    
    return redirect("show-target",uuid)