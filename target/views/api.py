from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.forms.models import model_to_dict
from django.db import transaction
from django.contrib import messages
import datetime
import json

from competency.models import TaskEvaluationItem
from ..models import Target, TargetTaskEvaluationItem
from ..forms import TargetCreateForm
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
        print(data)
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
