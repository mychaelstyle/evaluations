from django.db import models
from django_boost.models.mixins import LogicalDeletionMixin
from django.utils.translation import gettext_lazy as _

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

#
# コンピテンシーフレームワーク
#
class Competency(BaseModel):
    """コンピテンシーフレームワークの種類を入れます
    今はiCDしか入れませんので固定で１行です。

    Args:
        BaseModel (_type_): _description_
    """
    name = models.CharField(verbose_name=_("task.title"),max_length=255)

#
# タスクテーブル
#
class TaskEvaluation(BaseModel):
    """iCDのタスク情報を階層的に取り込むテーブル
    Taskだけだとタスク管理と勘違いしそうなのでタスク評価という名前にしました。
    親IDを持ってiCDの３階層構成のタスクをインポートします。

    Args:
        BaseModel (_type_): _description_
    """
    competency = models.ForeignKey(Competency,verbose_name=_("competency"), 
        on_delete=models.CASCADE,null=False,blank=False,related_name="task_evaluation_competency")
    parent = models.ForeignKey("self",verbose_name=_("task_parent"),null=True,db_index=True,blank=True,on_delete=models.CASCADE)
    node_level = models.PositiveSmallIntegerField(verbose_name=_("node_level"),null=False,blank=False,default=0)
    is_leaf = models.BooleanField(verbose_name=_('is_leaf'),null=False,blank=False,default=False)
    code = models.CharField(verbose_name=_("task_code"),max_length=50)
    name = models.CharField(verbose_name=_("task_name"),max_length=255)

#
# タスク評価項目テーブル
#
class TaskEvaluationItem(BaseModel):
    """iCDのタスクに対する評価項目を取り込むテーブル
    親を持たせたのはさらに評価項目を分解することを視野に入れてのことで、iCDを取り込む際に子階層は生成されません。

    Args:
        BaseModel (_type_): _description_
    """
    task_evaluation = models.ForeignKey(TaskEvaluation,verbose_name=_("task_evaluation"), 
        on_delete=models.CASCADE,null=False,blank=False,related_name="task_evaluation_item_task_evaluation")
    parent = models.ForeignKey("self",verbose_name=_("task_item_parent"),null=True,db_index=True,blank=True,on_delete=models.CASCADE)
    node_level = models.PositiveSmallIntegerField(verbose_name=_("node_level"),null=False,blank=False,default=0)
    is_leaf = models.BooleanField(verbose_name=_('is_leaf'),null=False,blank=False,default=False)
    code = models.CharField(verbose_name=_("task_item_code"),max_length=50)
    name = models.CharField(verbose_name=_("task_item_name"),max_length=255)

#
# タスクプロフィールテーブル
#
class TaskProfile(BaseModel):
    """iCDのタスクプロフィールを取り込むテーブル
    プロフィールカテゴリと分類もコードを作成して無理やり３階層として取り込みます。

    Args:
        BaseModel (_type_): _description_
    """
    competency = models.ForeignKey(Competency,verbose_name=_("competency"), 
        on_delete=models.CASCADE,null=False,blank=False,related_name="task_profile_competency")
    parent = models.ForeignKey("self",verbose_name=_("task_profile_parent"),null=True,db_index=True,blank=True,on_delete=models.CASCADE)
    node_level = models.PositiveSmallIntegerField(verbose_name=_("node_level"),null=False,blank=False,default=0)
    is_leaf = models.BooleanField(verbose_name=_('is_leaf'),null=False,blank=False,default=False)
    code = models.CharField(verbose_name=_("task_item_code"),max_length=50)
    name = models.CharField(verbose_name=_("task_item_name"),max_length=255)
    description = models.CharField(verbose_name=_("task_item_name"),max_length=255)

#
# タスクxタスクプロフィール関連テーブル
#
class TaskEvaluationTaskProfile(BaseModel):
    """iCDタスクとタスクプロフィールの関連づけテーブル

    Args:
        BaseModel (_type_): _description_
    """
    task_evaluation = models.ForeignKey(TaskEvaluation,verbose_name=_("task_evaluation"), 
        on_delete=models.CASCADE,null=False,blank=False,related_name="task_evaluation_profile_task_evaluation")
    task_profile = models.ForeignKey(TaskProfile,verbose_name=_("task_evaluation"), 
        on_delete=models.CASCADE,null=False,blank=False,related_name="task_evaluation_profile_task_profile")
    weight = models.PositiveSmallIntegerField(verbose_name=_("task_profile_relation_weight"),null=False,blank=False,default=0)

#
# スキルテーブル
#
class SkillEvaluation(BaseModel):
    """iCDスキル情報テーブル
    親IDを持ちiCDの３階層の構造を取り込みます。

    Args:
        BaseModel (_type_): _description_
    """
    competency = models.ForeignKey(Competency,verbose_name=_("competency"), 
        on_delete=models.CASCADE,null=False,blank=False,related_name="skill_evaluation_competency")
    parent = models.ForeignKey("self",verbose_name=_("skill_parent"),null=True,db_index=True,blank=True,on_delete=models.CASCADE)
    node_level = models.PositiveSmallIntegerField(verbose_name=_("node_level"),null=False,blank=False,default=0)
    is_leaf = models.BooleanField(verbose_name=_('is_leaf'),null=False,blank=False,default=False)
    code = models.CharField(verbose_name=_("skill_code"),max_length=50)
    name = models.CharField(verbose_name=_("skill_name"),max_length=255)

#
# スキル関連知識
#
class SkillEvaluationKnowledge(BaseModel):
    """スキル関連知識テーブル
    親IDを持たせたのはさらに知識をブレイクダウンする可能性を視野に入れてのことです。iCDの取り込みでは子階層は生成されません。

    Args:
        BaseModel (_type_): _description_
    """
    skill_evaluation = models.ForeignKey(SkillEvaluation,verbose_name=_("skill_evaluation"), 
        on_delete=models.CASCADE,null=False,blank=False,related_name="skill_evaluation_knowledge_skill_evaluation")
    parent = models.ForeignKey("self",verbose_name=_("skill_knowledge_parent"),null=True,db_index=True,blank=True,on_delete=models.CASCADE)
    node_level = models.PositiveSmallIntegerField(verbose_name=_("node_level"),null=False,blank=False,default=0)
    is_leaf = models.BooleanField(verbose_name=_('is_leaf'),null=False,blank=False,default=False)
    code = models.CharField(verbose_name=_("skill_knowledge_code"),max_length=50)
    name = models.CharField(verbose_name=_("skill_knowledge_name"),max_length=255)

#
# タスクxスキル関連
#
class TaskSkill(BaseModel):
    """タスクxスキル関連づけテーブル

    Args:
        BaseModel (_type_): _description_
    """
    task_evaluation = models.ForeignKey(TaskEvaluation,verbose_name=_("task_evaluation"), 
        on_delete=models.CASCADE,null=False,blank=False,related_name="task_skill_task_evaluation")
    skill_evaluation = models.ForeignKey(SkillEvaluation,verbose_name=_("skill_evaluation"), 
        on_delete=models.CASCADE,null=False,blank=False,related_name="task_skill_skill_evaluation")

#
# タスクフルテキスト検索用テーブル
#
class TaskFulltext(BaseModel):
    """タスクに関連する情報のテキストを全てまとめてテキスト検索するためのテーブル
    全文検索はそのうち検討

    Args:
        BaseModel (_type_): _description_
    """
    task_evaluation = models.ForeignKey(TaskEvaluation,verbose_name=_("task_evaluation"), 
        on_delete=models.CASCADE,null=False,blank=False,related_name="task_fulltext_task_evaluation")
    contents = models.TextField(verbose_name="task_fulltext_contents",null=False,blank=False)
