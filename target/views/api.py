from django.http import Http404
from django.utils.translation import gettext as _
from django.forms.models import model_to_dict
from django.forms import ValidationError
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import datetime
from django.utils import timezone
from datetime import datetime, date, time, timedelta
from uuid import uuid4
import json

from competency.models import TaskEvaluationItem
from ..models import Target, TargetTaskEvaluationItem, TargetTaskEvaluationItemAction, Evaluation
from ..forms import TargetCreateForm, TargetTaskEvaluationItemActionCreateForm
from ..services import is_authenticated, authenticate, get_anonymous
from utilities import CommonJsonResponse, get_remote_address

def create(request):
    """_summary_

    Args:
        request (_type_): _description_
    """
    res = CommonJsonResponse(request)
    if request.method.lower() == "post":
        for m in messages.get_messages(request):
            print(m)
            pass
        data = json.loads(request.body)
        if 'passcode' in data and len(data['passcode']) > 0:
            data['passcode'] = make_password(data['passcode'])
        form = TargetCreateForm(data)
        items = {}
        if not form.is_valid():
            res.set_fielderrors(form.errors)
        if 'items' not in data:
            res.add_fielderror("items",_("no_selected_items"))
        else:
            item_ids = data['items']
            if len(item_ids) < 3:
                res.add_fielderror("items",_("select_more_than_3_items"))
            elif len(item_ids) > 10:
                res.add_fielderror("items",_("select_less_than_10_items"))
            else:
                for item_id in item_ids:
                    taskitem = TaskEvaluationItem.objects.filter(id=item_id).first()
                    if taskitem is None:
                        res.add_fielderror("items",_("invalid_selected_items"))
                    else:
                        items[item_id] = taskitem
        if res.is_error():
            res.add_message(_("validation_error"))
            return res.get()

        try:
            with transaction.atomic():
                form.save()
                target = form.instance
                print(vars(target))
                item_objects = []
                for item_id in item_ids:
                    taskitem = items[item_id]
                    evalitem = TargetTaskEvaluationItem()
                    evalitem.target = target
                    evalitem.item = taskitem
                    evalitem.save()
                    item_objects.append(model_to_dict(evalitem.item))
                target = Target.objects.prefetch_related('items','items__item').get(pk=target.id)
                # 作成者のuuidを作成
                creator_id = get_anonymous(request)
                target.creator_id = creator_id
                target.save()
                target_dict = model_to_dict(target)
                target_dict['uuid'] = target.uuid
                target_dict['items'] = item_objects
                print(target.uuid)
                res.set_data(target_dict)
                response = res.get()
                response.set_cookie("euuid",str(creator_id))
                return response
        except Exception as e:
            res.add_message(e)
            return res.get()

    return res.get()

def self_evaluation(request,id):
    """自己評価の更新

    Args:
        request (_type_): _description_
        id (_type_): _description_
    """
    res = CommonJsonResponse(request)
    item = TargetTaskEvaluationItem.objects.select_related('target','item').filter(id=id).first()
    if item is None:
        raise Http404('not_found')

    if request.method.lower() == "post":
        for m in messages.get_messages(request):
            pass
        data = json.loads(request.body)
        if not is_authenticated(request,item.target.uuid):
            if 'passcode' in data:
                try:
                    authenticate(request=request,uuid=item.target.uuid,passcode=data['passcode'])
                except ValidationError as e:
                    for m in e.messages:
                        res.add_message(m)
            else:
                res.add_fielderror("passcode",_("passcode_is_required"))

        if 'self_evaluation' not in data:
            res.add_fielderror("self_evaluation",_("self_evaluation_is_required"))
        elif not str.isdecimal(data['self_evaluation']):
            res.add_fielderror("self_evaluation",_("self_evaluation_must_be_decimal"))
        elif int(data['self_evaluation']) < 0 or int(data['self_evaluation']) > 100:
            res.add_fielderror("self_evaluation",_("self_evaluation_must_be_0_to_100"))

        if res.is_error():
            res.set_data(item)
            res.add_message(_("validation_error"))
            return res.get()

        item.self_evaluation = int(data['self_evaluation'])
        item.save()
        
        res.set_data(item)
        response = res.get()
        response.set_cookie('euuid',item.target.creator_id)
        return response

def action_progress(request,id):
    """自己評価の更新

    Args:
        request (_type_): _description_
        id (_type_): _description_
    """
    res = CommonJsonResponse(request)
    action = TargetTaskEvaluationItemAction.objects.select_related('target_item','target_item__item','target_item__target').filter(id=id).first()
    if action is None:
        raise Http404('not_found')

    if request.method.lower() == "post":
        for m in messages.get_messages(request):
            pass
        data = json.loads(request.body)
        if not is_authenticated(request,action.target_item.target.uuid):
            if 'passcode' in data:
                try:
                    authenticate(request=request,uuid=action.target_item.target.uuid,passcode=data['passcode'])
                except ValidationError as e:
                    for m in e.messages:
                        res.add_message(m)
            else:
                res.add_fielderror("passcode",_("passcode_is_required"))

        if 'progress' not in data:
            res.add_fielderror("progress",_("progress_is_required"))
        elif not str.isdecimal(data['progress']):
            res.add_fielderror("progress",_("progress_must_be_decimal"))
        elif int(data['progress']) < 0 or int(data['progress']) > 100:
            res.add_fielderror("progress",_("progress_must_be_0_to_100"))

        if res.is_error():
            res.set_data(action)
            res.add_message(_("validation_error"))
            return res.get()

        action.progress = int(data['progress'])
        action.save()
        
        res.set_data(action)
        return res.get()


def request_evaluation(request,uuid:str):
    """評価リクエストを作成

    Args:
        request (_type_): _description_
        uuid (str): _description_
    """
    res = CommonJsonResponse(request)
    target = Target.objects.prefetch_related('items','items__item').filter(uuid=uuid).first()
    if target is None:
        raise Http404('Not found!')

    if not is_authenticated(request,uuid):
        res.add_message(_('authentication_required'))
        return res.get()
    
    if request.method.lower() == "post":
        evaluation = Evaluation()
        evaluation.target = target
        for m in messages.get_messages(request):
            pass
        data = json.loads(request.body)
        days = data.get('days', 14)
        due_date = timezone.now() + timedelta(days=days)
        evaluation.due_date = due_date.date()
        evaluation.remote_address = get_remote_address(request)
        evaluation.remote_host = request.META.get('REMOTE_HOST', None)
        evaluation.user_agent = request.META.get('HTTP_USER_AGENT', None)
        evaluation.save()
        
        evaluation = Evaluation.objects.filter(uuid=evaluation.uuid).first()
        
        res.set_data(evaluation)
        return res.get()
    
    return res.get()
