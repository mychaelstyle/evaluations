from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.http import Http404
from django.forms import ValidationError
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, date, time
import random

from . import api

from competency.models import TaskEvaluationTaskProfile, TaskSkill
from ..models import Target, Evaluation, EvaluationItemValue
from ..forms import TargetTaskEvaluationItemActionCreateForm, EvaluationRelationshipForm, EvaluationProfileForm, EvaluationEvaluateForm, EvaluationFeedbackForm
from ..services import is_authenticated, authenticate, remove_auth, get_anonymous, relate_anonymous
from utilities import get_remote_address

# Create your views here.
def auth_passcode(request, uuid:str):
    passcode = request.POST.get('passcode', None)
    try:
        target = authenticate(request=request,uuid=uuid,passcode=passcode)
    except ValidationError as e:
        messages.error(request,e)
    return redirect("show-target",uuid)

def exit_authenticated(request, uuid:str):
    remove_auth(request, uuid)
    return redirect("show-target",uuid)

def target(request, uuid:str):
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
    action_form = request.session.get('action_form',TargetTaskEvaluationItemActionCreateForm())
    if 'action_form' in request.session:
        del request.session['action_form']
    
    authenticated = is_authenticated(request,uuid)
    
    return render(request, 'target.html', {'target':target, 'tasks':tasks, 'action_form':action_form, 'authenticated':authenticated})

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
    
    if is_authenticated(request,uuid):
        if form.is_valid():
            form.save()
        else:
            messages.error(request,form.errors)
            request.session['action_form'] = form
    else:
        messages.error(request,_("passcode_is_required"))
        request.session['action_form'] = form

    return redirect("show-target",uuid)

def evaluation(request,uuid:str):
    """他者評価ページを表示します

    Args:
        request (_type_): _description_
        uuid (str): _description_
    """
    evaluation = Evaluation.objects.select_related("target").prefetch_related("items","target__items","target__items__item").filter(uuid=uuid).first()
    if evaluation is None:
        raise Http404('Not found!')
    elif evaluation.due_date is not None and evaluation.due_date < timezone.now().date():
        raise Http404('Not found!')
    
    if evaluation.status == 0:
        # パスコードの設定
        if request.method.lower() == "post":
            passcode = request.POST.get('passcode', None)
            if passcode is None or len(passcode) < 4:
                messages.error(request,_("passcode_is_required_more_than_4chars"))
                return render(request,'evaluation/welcome.html',{"evaluation":evaluation})
            else:
                evaluation.passcode = make_password(passcode)
                evaluation.status = 1
                # アクセス者UUIDの作成
                evaluator_id = get_anonymous(request)
                evaluation.evaluator_id = evaluator_id
                evaluation.remote_address = get_remote_address(request)
                evaluation.remote_host = request.META.get('REMOTE_HOST', None)
                evaluation.user_agent = request.META.get('HTTP_USER_AGENT', None)

                evaluation.save()
                # セッションの設定
                authed_evals = request.session.get("authorized_evaluations",[])
                authed_evals.append(uuid)
                request.session["authorized_evaluations"] = authed_evals
                response = redirect("evaluation",uuid=uuid)
                response.set_cookie('euuid',str(evaluator_id))
                return response
        elif request.method.lower() == "get":
            return render(request,'evaluation/welcome.html',{"evaluation":evaluation})
    else:
        # パスコード認証
        authed_evals = request.session.get("authorized_evaluations",[])
        if uuid not in authed_evals:
            if request.method.lower() == "post":
                passcode = request.POST.get('passcode',None)
                if passcode is None or len(passcode) == 0:
                    messages.error(request,_("passcode_is_required"))
                    return render(request,'evaluation/auth_passcode.html',{"evaluation":evaluation})
                elif not check_password(password=passcode, encoded=evaluation.passcode):
                    messages.error(request,_("passcode_is_invalid"))
                    return render(request,'evaluation/auth_passcode.html',{"evaluation":evaluation})
                else:
                    authed_evals.append(uuid)
                    request.session["authorized_evaluations"] = authed_evals
                    evaluator_id = get_anonymous(request)
                    if evaluator_id != evaluation.evaluator_id:
                        relate_anonymous(evaluation.evaluator_id, evaluator_id)
                    evaluation.evaluator_id = evaluator_id
                    evaluation.remote_address = get_remote_address(request)
                    evaluation.remote_host = request.META.get('REMOTE_HOST', None)
                    evaluation.user_agent = request.META.get('HTTP_USER_AGENT', None)
                    evaluation.save()

                    response = redirect("evaluation",uuid=uuid)
                    response.set_cookie('euuid',str(evaluator_id))
                    return response
            else:
                return render(request,'evaluation/auth_passcode.html',{"evaluation":evaluation})                

        if evaluation.status == 1:
            # 関係性を入力
            if request.method.lower() == "post":
                form = EvaluationRelationshipForm(request.POST,instance=evaluation)
                if form.is_valid():
                    form.save()
                    evaluation = Evaluation.objects.select_related("target").prefetch_related("target__items","target__items__item").filter(uuid=uuid).first()
                    evaluation.status = 2
                    evaluation.save()
                    return redirect("evaluation",uuid=uuid)
                else:
                    return render(request,'evaluation/relationship.html',{"evaluation":evaluation, "relationship_form":form})
            elif request.method.lower() == "get":
                form = EvaluationRelationshipForm()
                return render(request,'evaluation/relationship.html',{"evaluation":evaluation, "relationship_form":form})
        elif evaluation.status == 2:
            # プロフィールを入力
            if request.method.lower() == "post":
                form = EvaluationProfileForm(request.POST, instance=evaluation)
                if form.is_valid():
                    form.save()
                    evaluation = Evaluation.objects.select_related("target").prefetch_related("target__items","target__items__item").filter(uuid=uuid).first()
                    evaluation.status = 3
                    evaluation.save()
                    return redirect("evaluation",uuid=uuid)
                else:
                    return render(request,'evaluation/profile.html',{"evaluation":evaluation, "profile_form":form})
            else:
                form = EvaluationProfileForm(instance=evaluation)
                return render(request,'evaluation/profile.html',{"evaluation":evaluation, "profile_form":form})
        elif evaluation.status == 3 or evaluation.status == 10:
            # 評価項目で評価が終わっていないものを表示
            items = evaluation.target.items.all()
            evalues = evaluation.items.all()
            evaluateds = []
            candidates = {}
            for item in items:
                candidates[item.id] = item
                for evalue in evalues:
                    if evalue.target_item.id == item.id:
                        evaluateds.append(item.id)
            
            for vid in evaluateds:
                del candidates[vid]
            if len(candidates) == 0:
                evaluation.status == 20
                evaluation.save()
                return redirect("evaluation",uuid=uuid)

            if request.method.lower() == "post":
                form = EvaluationEvaluateForm(request.POST)
                print(request.POST)
                if form.is_valid():
                    target_item = None
                    item_id = form.cleaned_data.get('item_id')
                    for item in evaluation.target.items.all():
                        if item.item.id == item_id:
                            target_item = item
                            break
                    if target_item is None:
                        messages.error(request,_('item_id_is_required'))
                        target_item_id, target_item = random.choice(list(candidates.items()))
                        return render(request,'evaluation/evaluate.html',{
                            "evaluation":evaluation,
                            "evaluation_item":target_item,
                            "evaluation_form":form})
                    
                    evaluation_value = EvaluationItemValue()
                    evaluation_value.evaluation = evaluation
                    evaluation_value.target_item = target_item
                    print(form.cleaned_data)
                    if form.cleaned_data.get("skip"):
                        evaluation_value.score = None
                        evaluation_value.self_score = None
                    else:
                        evaluation_value.score = form.cleaned_data.get("score")
                        evaluation_value.self_score = form.cleaned_data.get("self_score")
                    evaluation_value.evaluator_id = get_anonymous(request)
                    evaluation_value.remote_address = get_remote_address(request)
                    evaluation_value.remote_host = request.META.get('REMOTE_HOST', None)
                    evaluation_value.user_agent = request.META.get('HTTP_USER_AGENT', None)
                    evaluation_value.save()
                    
                    if len(candidates) <= 1:
                        evaluation = Evaluation.objects.select_related("target").prefetch_related("target__items","target__items__item").filter(uuid=uuid).first()
                        evaluation.status = 20
                        evaluation.save()
                    return redirect("evaluation",uuid=uuid)
                else:
                    print(form.errors)
                    print(vars(request.POST))
                    target_item_id, target_item = random.choice(list(candidates.items()))
                    return render(request,'evaluation/evaluate.html',{"evaluation":evaluation, "evaluation_item":target_item, "evaluation_form":form})
            else:
                form = EvaluationEvaluateForm()
                target_item_id, target_item = random.choice(list(candidates.items()))
                return render(request,'evaluation/evaluate.html',{"evaluation":evaluation, "evaluation_item":target_item, "evaluation_form":form})
        elif evaluation.status == 20:
            # フィードバックコメントを入力
            if request.method.lower() == "post":
                form = EvaluationFeedbackForm(request.POST,instance=evaluation)
                if form.is_valid():
                    form.save()
                    evaluation = Evaluation.objects.select_related("target").prefetch_related("target__items","target__items__item").filter(uuid=uuid).first()
                    evaluation.status = 100
                    evaluation.save()
                    return redirect("evaluation",uuid=uuid)
                else:
                    return render(request,'evaluation/feedback.html',{"evaluation":evaluation, "feedback_form":form})
            else:
                form = EvaluationFeedbackForm()
                return render(request,'evaluation/feedback.html',{"evaluation":evaluation, "feedback_form":form})
        else:
            return render(request,'evaluation/complete.html',{"evaluation":evaluation})