from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404
from . import api

from competency.models import TaskEvaluationTaskProfile, TaskSkill
from ..models import Target

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
    print(vars(target))
    item_relations = target.items.select_related('item','item__task_evaluation').all()
    tasks = {}
    task_ids = []
    for item_relation in item_relations:
        #print(vars(item_relation))
        #print(vars(item_relation.item))
        #print(vars(item_relation.item.task_evaluation))
        #print(vars(item_relation.item.task_evaluation.parent))
        #print(vars(item_relation.item.task_evaluation.parent.parent))
        task = item_relation.item.task_evaluation
        if task.id not in task_ids:
            task_ids.append(task.id)
        if task.id not in tasks:
            tasks[task.id] = {"task":task}
            tasks[task.id]["items"] = []
        tasks[task.id]["items"].append(item_relation.item)
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
        print('-------')
        print(vars(skill))
        if "skills" not in tasks[task_id]:
            tasks[task_id]["skills"] = []
        tasks[task_id]["skills"].append(skill)
        
    return render(request, 'target.html', {'target':target, 'tasks':tasks})