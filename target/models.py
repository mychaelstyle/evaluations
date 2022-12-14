from django.db import models
from django_boost.models.mixins import LogicalDeletionMixin
from django.utils.translation import gettext_lazy as _
import uuid

from competency.models import TaskEvaluationItem

GRADES = [
    (0, _("students")),
    (1, _("new_graduates")),
    (5, _("juniors")),
    (10, _("regular_members")),
    (15, _("team_leaders")),
    (20, _("managers")),
    (25, _("heads_of_section")),
    (30, _("board_members"))
]

INDUSTORIES = (
    (1,"メーカー：食品・農林・水産"),
    (11,"メーカー：建設・住宅・インテリア"),
    (21,"メーカー：遷移・化学・薬品・化粧品"),
    (31,"メーカー：鉄鋼・金属・鉱業"),
    (41,"メーカー：機械・プラント"),
    (51,"メーカー：電子・電気機器"),
    (61,"メーカー：自動車・輸送容器機"),
    (71,"メーカー：精密・医療機器"),
    (81,"メーカー：飲茶靴・事務機器関連"),
    (91,"メーカー：スポーツ・玩具"),
    (101,"メーカー：その他メーカー"),
    (111,"商社：総合商社"),
    (121,"商社：専門商社"),
    (131,"小売：百貨店・スーパー"),
    (141,"小売：コンビニ"),
    (151,"小売：専門店"),
    (161,"金融：銀行・証券"),
    (171,"金融：クレジット"),
    (181,"金融：信販・リース"),
    (191,"金融：その他金融"),
    (201,"金融：生保・損保"),
    (211,"サービス・インフラ：不動産"),
    (221,"サービス・インフラ：鉄道・航空・運輸・物流"),
    (231,"サービス・インフラ：電力・ガス・エネルギー"),
    (241,"サービス・インフラ：フードサービス"),
    (251,"サービス・インフラ：ホテル・旅行"),
    (261,"サービス・インフラ：医療・福祉"),
    (271,"サービス・インフラ：アミューズメント・レジャー"),
    (281,"サービス・インフラ：その他サービス"),
    (291,"サービス・インフラ：コンサルティング・調査"),
    (301,"サービス・インフラ：人材サービス"),
    (311,"サービス・インフラ：教育"),
    (321,"ソフトウェア：ソフトウェア"),
    (331,"ソフトウェア：インターネット"),
    (341,"ソフトウェア：通信"),
    (351,"広告・出版・マスコミ：放送"),
    (361,"広告・出版・マスコミ：新聞"),
    (371,"広告・出版・マスコミ：出版"),
    (381,"広告・出版・マスコミ：広告"),
    (391,"官公庁・公社・団体：公社・団体"),
    (401,"官公庁・公社・団体：官公庁"),
    (999,_("others"))
)

ACTION_TYPES = (
    (0,_("on_the_job")),
    (10,_("read_a_book")),
    (20,_("take_a_seminar")),
    (30,_("make_anything")),
    (40,_("presentation")),
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
    uuid = models.UUIDField(verbose_name=_("UUID"),default=uuid.uuid4, editable=False, unique=True, db_index=True)
    passcode = models.CharField(verbose_name=_("passcode"), null=True, blank=True, max_length=255)
    viewcode = models.CharField(verbose_name=_("viewcode"), null=True, blank=True, max_length=255)
    is_open = models.BooleanField(verbose_name=_("is_open"), null=False, blank=False, default=True)
    viewname = models.CharField(verbose_name=_("target_viewname"),max_length=100,null=False,blank=False)
    first_name = models.CharField(verbose_name=_("first_name"),max_length=100,null=True,blank=True)
    last_name = models.CharField(verbose_name=_("last_name"),max_length=100,null=True,blank=True)
    target_date = models.DateField(verbose_name=_("target_date"), null=True, blank=True)
    grade = models.SmallIntegerField(verbose_name=_("grade"),choices=GRADES, null=True, blank=True)
    industory = models.PositiveSmallIntegerField(verbose_name=_("organization_name"), null=True, blank=True, choices=INDUSTORIES)
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
    action_type = models.PositiveSmallIntegerField(verbose_name=_('action_type'),choices=ACTION_TYPES, null=True, blank=True)
    description = models.TextField(verbose_name=_("description"), null=True, blank=True, max_length=500)
    url = models.CharField(verbose_name=_("url"), max_length=255, null=True, blank=True)
    progress = models.PositiveSmallIntegerField(verbose_name=_("progress"), null=False, blank=False, default=0)

class Evaluation(BaseModel):
    """評価テーブル

    Args:
        BaseModel (_type_): _description_
    """
    uuid = models.UUIDField(verbose_name=_("UUID"),default=uuid.uuid4, editable=False, unique=True, db_index=True)
    target = models.ForeignKey(Target, verbose_name=_("target"),null=False,
                            db_index=True,blank=False,on_delete=models.CASCADE,related_name="evaluations")
    passcode = models.CharField(verbose_name=_("passcode"), null=True, blank=True, max_length=255)
    first_name = models.CharField(verbose_name=_("first_name"),max_length=100,null=True,blank=True)
    last_name = models.CharField(verbose_name=_("last_name"),max_length=100,null=True,blank=True)
    grade = models.SmallIntegerField(verbose_name=_("grade"),choices=GRADES, null=True, blank=True)
    industory = models.PositiveSmallIntegerField(verbose_name=_("organization_name"), null=True, blank=True, choices=INDUSTORIES)
    industory_opt = models.CharField(verbose_name=_("industry_optional"), max_length=50, null=True, blank=True)
    org_name = models.CharField(verbose_name=_("organization_name"), max_length=200, null=True, blank=True)
    org_url = models.CharField(verbose_name=_("organization_url"), max_length=255, null=True, blank=True)
    department_name = models.CharField(verbose_name=_("department_name"), max_length=200, null=True, blank=True)
    job = models.CharField(verbose_name=_("role"), max_length=200, null=True, blank=True)
    position = models.CharField(verbose_name=_("role"), max_length=200, null=True, blank=True)
    role = models.CharField(verbose_name=_("role"), max_length=255, null=True, blank=True)
    feedback_notes = models.TextField(verbose_name=_("feedback_notes"), null=True, blank=True, max_length=500)

class EvaluationItemValue(BaseModel):
    """評価項目値テーブル

    Args:
        BaseModel (_type_): _description_
    """
    evaluation = models.ForeignKey(Evaluation, verbose_name=_("evaluation"),null=False,
                            db_index=True,blank=False,on_delete=models.CASCADE,related_name="items")
    target_item = models.ForeignKey(TargetTaskEvaluationItem, verbose_name=_("target_item"),null=False,
                            db_index=True,blank=False,on_delete=models.CASCADE,related_name="evaluations")
    score = models.PositiveSmallIntegerField(verbose_name=_("evaluation_value"), blank=True, null=True)
    self_score = models.PositiveSmallIntegerField(verbose_name=_("self_evaluation_value"), blank=True, null=True)
