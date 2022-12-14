from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Target,TargetTaskEvaluationItemAction

class TargetCreateForm(forms.ModelForm):
    """_summary_

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = Target
        fields = ['viewname','passcode','first_name','last_name','grade','industory','industory_opt','org_name','org_url','department_name','job','position','role','description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'
            self.fields[key].widget.attrs['id'] = 'target-' + key

class TargetTaskEvaluationItemActionCreateForm(forms.ModelForm):
    """目標設定項目アクション新規作成用フォーム

    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = TargetTaskEvaluationItemAction
        fields = ['target_item','name','action_type','description','url']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'
            self.fields[key].widget.attrs['id'] = 'target-item-action-' + key
