from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Target,TargetTaskEvaluationItemAction, Evaluation, EvaluationItemValue
from competency.models import TaskEvaluationItem

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
        widgets = {
            'name': forms.TextInput(attrs={'placeholder':_('action_name_placeholder')}),
            'url': forms.URLInput(attrs={'placeholder':_('action_url_placeholder')})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'
            self.fields[key].widget.attrs['id'] = 'target-item-action-' + key

class EvaluationRelationshipForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['relationship','coworked']
        widgets = {
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'
            self.fields[key].widget.attrs['id'] = 'evaluation-' + key
    
    def clean_relationship(self):
        relationship = self.cleaned_data.get("relationship", None)
        if relationship is None:
            raise forms.ValidationError(_('relationship_is_required'))
        return relationship
    
    def clean_coworked(self):
        coworked = self.cleaned_data.get("coworked", None)
        if coworked is None:
            raise forms.ValidationError(_('coworked_is_required'))
        return coworked

class EvaluationProfileForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['industory','industory_opt','org_name','department_name','org_url','job','position','role','grade','first_name','last_name']
        widgets = {
            "industory_opt" : forms.widgets.TextInput(attrs={"class":"form-control", "placeholder":_("input_if_you_choice_others")}),
            "job" : forms.widgets.TextInput(attrs={"class":"form-control", "placeholder":_("EX_Web_application_engineer")}),
            "first_name" : forms.widgets.TextInput(attrs={"class":"form-control", "placeholder":_("first_name")}),
            "last_name" : forms.widgets.TextInput(attrs={"class":"form-control", "placeholder":_("last_name")}),
            "org_name" : forms.widgets.TextInput(attrs={"class":"form-control", "placeholder":_("org_name")}),
            "department_name" : forms.widgets.TextInput(attrs={"class":"form-control", "placeholder":_("department_name")}),
            "position" : forms.widgets.TextInput(attrs={"class":"form-control", "placeholder":_("EX_manager")}),
            "role" : forms.widgets.TextInput(attrs={"class":"form-control", "placeholder":_("EX_role")}),
            "org_url" : forms.widgets.TextInput(attrs={"class":"form-control", "placeholder":_("EX_url")}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'
            self.fields[key].widget.attrs['id'] = 'evaluation-' + key

    def clean_industory(self):
        industory = self.cleaned_data.get("industory", None)
        if industory is None:
            raise forms.ValidationError(_('industory_is_required'))
        return industory

    def clean_industory_opt(self):
        industory_opt = self.cleaned_data.get("industory_opt", None)
        if industory_opt is not None:
            industory_opt = industory_opt.strip()
        return industory_opt

    def clean_job(self):
        job = self.cleaned_data.get("job", None)
        if job is None or len(job.strip()) == 0:
            raise forms.ValidationError(_('job_is_required'))
        return job.strip()

    def clean_grade(self):
        grade = self.cleaned_data.get("grade", None)
        if grade is None:
            raise forms.ValidationError(_('grade_is_required'))
        return grade
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", None)
        if last_name is None:
            raise forms.ValidationError(_('last_name_is_required'))
        else:
            last_name = last_name.strip()
            if len(last_name) == 0:
                raise forms.ValidationError(_('last_name_is_required'))
        return last_name.strip()

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", None)
        if first_name is None:
            raise forms.ValidationError(_('first_name_is_required'))
        else:
            first_name = first_name.strip()
            if len(first_name) == 0:
                raise forms.ValidationError(_('first_name_is_required'))
        return first_name.strip()

    def clean_org_name(self):
        org_name = self.cleaned_data.get("org_name", None)
        if org_name is not None:
            org_name = org_name.strip()
        return org_name

    def clean_department_name(self):
        department_name = self.cleaned_data.get("department_name", None)
        if department_name is not None:
            department_name = department_name.strip()
        return department_name

    def clean_position(self):
        position = self.cleaned_data.get("position", None)
        if position is not None:
            position = position.strip()
        return position

    def clean_role(self):
        role = self.cleaned_data.get("role", None)
        if role is None:
            raise forms.ValidationError(_('role_is_required'))
        else:
            role = role.strip()
            if len(role) == 0:
                raise forms.ValidationError(_('role_is_required'))
        return role

    def clean_org_url(self):
        org_url = self.cleaned_data.get("org_url", None)
        if org_url is not None:
            org_url = org_url.strip()
        return org_url

class EvaluationEvaluateForm(forms.Form):
    item_id = forms.IntegerField(min_value=1,required=True)
    score = forms.IntegerField(max_value=100,required=True)
    self_score = forms.IntegerField(max_value=100,required=True)
    skip = forms.BooleanField(required=True)
    class Meta:
        model = EvaluationItemValue
        fields = ['score','self_score']
        widgets = {
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'
            self.fields[key].widget.attrs['id'] = 'evaluation-' + key
    
    def clean_item_id(self):
        item_id = self.cleaned_data.get("item_id", None)
        if item_id is None:
            raise forms.ValidationError(_('item_id_is_required'))
        item = TaskEvaluationItem.objects.filter(id=item_id).alive().first()
        if item is None:
            raise forms.ValidationError(_('item_id_is_invalid'))
        return item_id
    
    def clean_score(self):
        score = self.cleaned_data.get("score", None)
        if score is None:
            raise forms.ValidationError(_('score_is_required'))
        if score > 100:
            raise forms.ValidationError(_('score_must_be_less_than_100'))
        return score
        
    def clean_self_score(self):
        self_score = self.cleaned_data.get("self_score", None)
        if self_score is None:
            raise forms.ValidationError(_('score_is_required'))
        if self_score > 100:
            raise forms.ValidationError(_('score_must_be_less_than_100'))
        return self_score

class EvaluationFeedbackForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['feedback_notes']
        widgets = {
            'feedback_notes': forms.widgets.Textarea(attrs={'class':'form-control','id':'evaluation-feedback_notes','rows':"2", 'cols':"100"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'
            self.fields[key].widget.attrs['id'] = 'evaluation-' + key

