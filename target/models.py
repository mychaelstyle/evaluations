from django.db import models
from django_boost.models.mixins import LogicalDeletionMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from uuid import uuid4

from competency.models import TaskEvaluationItem

ACTION_TYPES = (
    (0,_("on_the_job")),
    (10,_("read_a_book")),
    (20,_("take_a_seminar")),
    (30,_("make_anything")),
    (40,_("presentation")),
    (50,_("learnig_on_a_website")),
)

RELATIONSHIPS = (
    (40, _("boss")),
    (30, _("colleague")),
    (20, _("clients")),
    (10, _("subordinate")),
    (0, _("friends")),
)

COWORKINGS = (
    (0, _("not_coworked")),
    (10, _("one_time_project")),
    (20, _("several_projects")),
    (30, _("several_years")),
    (40, _("always"))
)

EVALUATION_STATUSES = (
    (0, _("new")),
    (1, _("set_passcode")),
    (2,_("set_relationship")),
    (3,_("set_profile")),
    (10, _("in_progress")),
    (20,_("set_feedback")),
    (100, _("completed")),
)

#
# 本アプリケーションのベースモデル
#
class BaseModel(LogicalDeletionMixin):
    """ accountアプリケーションのベースデータモデル

    Args:
        LogicalDeletionMixin (_type_): 論理削除のミックスインが入ってます
    """
    created_at = models.DateTimeField(verbose_name=_("created_at"),auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated_at"),auto_now=True)
    class Meta:
        abstract = True

class Target(BaseModel):
    """目標設定情報テーブル

    Args:
        BaseModel (_type_): _description_
    """
    uuid = models.UUIDField(verbose_name=_("UUID"),default=uuid4, editable=False, unique=True, db_index=True)
    creator_id = models.CharField(verbose_name=_('creator_uuid'), max_length=50, null=True, blank=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,verbose_name=_("user"),related_name="targets", null=True, blank=True)
    passcode = models.CharField(verbose_name=_("passcode"), null=True, blank=True, max_length=255)
    viewcode = models.CharField(verbose_name=_("viewcode"), null=True, blank=True, max_length=255)
    is_open = models.BooleanField(verbose_name=_("is_open"), null=False, blank=False, default=True)
    viewname = models.CharField(verbose_name=_("target_viewname"),max_length=100,null=False,blank=False)
    first_name = models.CharField(verbose_name=_("first_name"),max_length=100,null=True,blank=True)
    last_name = models.CharField(verbose_name=_("last_name"),max_length=100,null=True,blank=True)
    target_date = models.DateField(verbose_name=_("target_date"), null=True, blank=True)
    grade = models.SmallIntegerField(verbose_name=_("grade"),choices=settings.GRADES, null=True, blank=True)
    industory = models.PositiveSmallIntegerField(verbose_name=_("organization_name"), null=True, blank=True, choices=settings.INDUSTORIES)
    industory_opt = models.CharField(verbose_name=_("industry_optional"), max_length=50, null=True, blank=True)
    org_name = models.CharField(verbose_name=_("organization_name"), max_length=200, null=True, blank=True)
    org_url = models.CharField(verbose_name=_("organization_url"), max_length=255, null=True, blank=True)
    department_name = models.CharField(verbose_name=_("department_name"), max_length=200, null=True, blank=True)
    job = models.CharField(verbose_name=_("role"), max_length=200, null=True, blank=True)
    position = models.CharField(verbose_name=_("role"), max_length=200, null=True, blank=True)
    role = models.CharField(verbose_name=_("role"), max_length=255, null=True, blank=True)
    description = models.TextField(verbose_name=_("description"), null=True, blank=True, max_length=500)

class TargetTaskEvaluationItem(BaseModel):
    """目標設定評価項目

    Args:
        BaseModel (_type_): _description_
    """
    target = models.ForeignKey(Target, verbose_name=_("target"),null=False,
                            db_index=True,blank=False,on_delete=models.CASCADE,related_name="items")
    item = models.ForeignKey(TaskEvaluationItem, verbose_name=_("task_evaluation_item"),null=False,
                            db_index=True,blank=False,on_delete=models.CASCADE,related_name="targets")
    self_evaluation = models.PositiveSmallIntegerField(verbose_name=_("self_evaluation"),null=True,blank=True)

class TargetTaskEvaluationItemAction(BaseModel):
    """評価項目アクション設定

    Args:
        BaseModel (_type_): _description_
    """
    target_item = models.ForeignKey(TargetTaskEvaluationItem, verbose_name=_("target_item"),null=False,
                            db_index=True,blank=False,on_delete=models.CASCADE,related_name="actions")
    name = models.CharField(verbose_name=_("user_viewname"),max_length=255, null=False, blank=False)
    action_type = models.PositiveSmallIntegerField(verbose_name=_('action_type'),choices=ACTION_TYPES, null=False, blank=False)
    description = models.TextField(verbose_name=_("description"), null=True, blank=True, max_length=500)
    url = models.TextField(verbose_name=_("url"), max_length=2000, null=True, blank=True)
    progress = models.PositiveSmallIntegerField(verbose_name=_("progress"), null=False, blank=False, default=0)

class Evaluation(BaseModel):
    """評価テーブル

    Args:
        BaseModel (_type_): _description_
    """
    uuid = models.UUIDField(verbose_name=_("UUID"),default=uuid4, editable=False, unique=True, db_index=True)
    evaluator_id = models.CharField(verbose_name=_('evaluator_uuid'), max_length=50, null=True, blank=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,verbose_name=_("user"),related_name="evaluations", null=True, blank=True)
    target = models.ForeignKey(Target, verbose_name=_("target"),null=False,
                            db_index=True,blank=False,on_delete=models.CASCADE,related_name="evaluations")
    passcode = models.CharField(verbose_name=_("passcode"), null=True, blank=True, max_length=255)
    status = models.PositiveSmallIntegerField(verbose_name=_("status"), null=False, blank=False, default=0, choices=EVALUATION_STATUSES)
    first_name = models.CharField(verbose_name=_("first_name"),max_length=100,null=True,blank=True)
    last_name = models.CharField(verbose_name=_("last_name"),max_length=100,null=True,blank=True)
    grade = models.SmallIntegerField(verbose_name=_("grade"),choices=settings.GRADES, null=True, blank=True)
    industory = models.PositiveSmallIntegerField(verbose_name=_("organization_name"), null=True, blank=True, choices=settings.INDUSTORIES)
    industory_opt = models.CharField(verbose_name=_("industry_optional"), max_length=50, null=True, blank=True)
    org_name = models.CharField(verbose_name=_("organization_name"), max_length=200, null=True, blank=True)
    org_url = models.CharField(verbose_name=_("organization_url"), max_length=255, null=True, blank=True)
    department_name = models.CharField(verbose_name=_("department_name"), max_length=200, null=True, blank=True)
    job = models.CharField(verbose_name=_("role"), max_length=200, null=True, blank=True)
    position = models.CharField(verbose_name=_("role"), max_length=200, null=True, blank=True)
    role = models.CharField(verbose_name=_("role"), max_length=255, null=True, blank=True)
    feedback_notes = models.TextField(verbose_name=_("feedback_notes"), null=True, blank=True, max_length=500)
    relationship = models.PositiveSmallIntegerField(verbose_name=_('relationship'),choices=RELATIONSHIPS, null=True, blank=True)
    coworked = models.PositiveSmallIntegerField(verbose_name=_('coworked'),choices=COWORKINGS, null=True, blank=True)
    due_date = models.DateField(verbose_name=_("due_date"),null=True, blank=True)
    remote_address = models.GenericIPAddressField(verbose_name=_("remote_address"),blank=True,null=True)
    remote_host = models.TextField(verbose_name=_("remote_host"), null=True, blank=True, max_length=1000)
    user_agent = models.TextField(verbose_name=_("remote_host"), null=True, blank=True, max_length=1000)

class EvaluationItemValue(BaseModel):
    """評価項目値テーブル

    Args:
        BaseModel (_type_): _description_
    """
    evaluation = models.ForeignKey(Evaluation, verbose_name=_("evaluation"),null=False,
                            db_index=True,blank=False,on_delete=models.CASCADE,related_name="items")
    target_item = models.ForeignKey(TargetTaskEvaluationItem, verbose_name=_("target_item"),null=False,
                            db_index=True,blank=False,on_delete=models.CASCADE,related_name="evaluations")
    evaluator_id = models.CharField(verbose_name=_('evaluator_uuid'), max_length=50, null=True, blank=True, db_index=True)
    score = models.PositiveSmallIntegerField(verbose_name=_("evaluation_value"), blank=True, null=True)
    self_score = models.PositiveSmallIntegerField(verbose_name=_("self_evaluation_value"), blank=True, null=True)
    remote_address = models.GenericIPAddressField(verbose_name=_("remote_address"),blank=True,null=True)
    remote_host = models.TextField(verbose_name=_("remote_host"), null=True, blank=True, max_length=1000)
    user_agent = models.TextField(verbose_name=_("remote_host"), null=True, blank=True, max_length=1000)

class Anonymous(BaseModel):
    """匿名ユーザのUUIDと関係性を保存する
    Args:
        BaseModel (_type_): _description_
    """
    uuid = models.UUIDField(verbose_name=_("user_uuid"), default=uuid4, editable=False, null=False,blank=False, db_index=True)
    related = models.CharField(verbose_name=_('related_uuid'), max_length=50, null=True, blank=True, db_index=True)
