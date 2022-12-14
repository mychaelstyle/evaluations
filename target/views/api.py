from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.forms.models import model_to_dict
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import datetime
import json

from competency.models import TaskEvaluationItem
from ..models import Target, TargetTaskEvaluationItem, TargetTaskEvaluationItemAction
from ..forms import TargetCreateForm, TargetTaskEvaluationItemActionCreateForm
from utilities import CommonJsonResponse

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
                target_dict = model_to_dict(target)
                target_dict['uuid'] = target.uuid
                target_dict['items'] = item_objects
                print(target.uuid)
                res.set_data(target_dict)
                return res.get()
        except Exception as e:
            res.add_message(e)
            return res.get()

    return res.get()

def self_evaluation(request,id):
    """自己評価の更新

    Args:
        request (_type_): _description_
        code (_type_): _description_
    """
    res = CommonJsonResponse(request)
    item = TargetTaskEvaluationItem.objects.select_related('target','item').filter(id=id).first()
    if item is None:
        raise Http404('not_found')
    if request.method.lower() == "post":
        for m in messages.get_messages(request):
            print(m)
            pass
        data = json.loads(request.body)
        if item.target.passcode is not None and len(item.target.passcode)>0:
            if 'passcode' not in data:
                res.add_fielderror("passcode",_("passcode_is_required"))
            elif not check_password(data['passcode'],item.target.passcode):
                res.add_fielderror("passcode",_("passcode_is_invalid"))
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
        return res.get()

def create_action(request,eval_item_id):
    """目標設定項目アクションを新規作成する

    Args:
        request (_type_): _description_
        eval_item_id (_type_): _description_
    """
    eval_item = TargetTaskEvaluationItemAction.objects.select_related('target','item').filter(id=eval_item_id).first()
    res = CommonJsonResponse(request)
    if eval_item is None:
        raise Http404('not_found')
    if request.method.lower() == "post":
        for m in messages.get_messages(request):
            print(m)
            pass
        data = json.loads(request.body)
        form = TargetTaskEvaluationItemActionCreateForm(data)
        if eval_item.target.passcode is not None and len(eval_item.target.passcode)>0:
            if 'passcode' not in data:
                res.add_fielderror("passcode",_("passcode_is_required"))
            elif not check_password(data['passcode'],eval_item.target.passcode):
                res.add_fielderror("passcode",_("passcode_is_invalid"))
        elif not form.is_valid():
            res.set_fielderrors(form.errors)
        if res.is_error():
            res.set_data(eval_item)
            res.add_message(_("validation_error"))
            return res.get()
        
        form.save()
        instance = form.instance
        res.set_data(instance)
        return res.get()
    else:
        raise Http404('not_found')