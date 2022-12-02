from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
import os
import pandas as pd

from competency.models import Competency, TaskEvaluation, TaskEvaluationItem, SkillEvaluation, SkillEvaluationKnowledge, TaskSkill, TaskProfile, TaskEvaluationTaskProfile

class Command(BaseCommand):
    help = 'iコンピテンシディクショナリのExcelファイルをデータベースにインポートするためのコマンドです'
    file = None
    COMPETENCY_NAME = "iコンピテンシディレクトリ"
    def add_arguments(self, parser):
        parser.add_argument('--type', help=_('インポートするExcelのタイプをtask|skill|relationで指定してください。'), required=True, type=str)
        parser.add_argument('--file', help=_('インポートするファイルパスを入力してください。'), required=True, type=str)
    
    def handle(self, *args, **options):
        try:
            print('バッチが動きました： {}'.format(options))
            self.file = options['file']
            if not os.path.isfile(self.file):
                print(_('指定されたパスにファイルが存在しません'))
            elif not self.file.endswith('.xlsx'):
                print(_('Excel形式のファイルを指定してください'))
            elif 'task' == options['type'].lower():
                self.import_tasks()
                self.import_profile()
                self.import_profile_relation()
            elif 'skill' == options['type'].lower():
                self.import_skills()
            elif 'relation' == options['type'].lower():
                self.import_relation()
            else:
                print(_('タイプオプション(--type)はtask|skill|relationのいずれかで指定してください。'))
        except Exception as e:
            print(e)
    
    def import_tasks(self):
        competency = self.get_or_create_competency()
        df = pd.read_excel(self.file,sheet_name="タスク一覧")
        df.columns = df.columns.str.replace("\n",'')
        for index, row in df.iterrows():
            b_code = row["タスク大分類コード"]
            m_code = row["タスク中分類コード"]
            s_code = row["タスク小分類コード"]
            # 大分類
            b_obj = TaskEvaluation.objects.filter(code=b_code).first()
            if b_obj is None:
                b_obj = TaskEvaluation()
            b_obj.competency = competency
            b_obj.code = b_code
            b_obj.node_level = 0
            b_obj.is_leaf = False
            b_obj.name = row["タスク大分類"]
            b_obj.save()
            b_obj = TaskEvaluation.objects.filter(code=b_code).first()
            print(b_obj)
            # 中分類
            m_obj = TaskEvaluation.objects.filter(code=m_code).first()
            if m_obj is None:
                m_obj = TaskEvaluation()
            m_obj.competency = competency
            m_obj.parent = b_obj
            m_obj.node_level = 1
            m_obj.is_leaf = False
            m_obj.code = m_code
            m_obj.name = row["タスク中分類"]
            m_obj.save()
            m_obj = TaskEvaluation.objects.filter(code=m_code).first()
            print(m_obj)
            # タスク項目
            s_obj = TaskEvaluation.objects.filter(code=s_code).first()
            if s_obj is None:
                s_obj = TaskEvaluation()
            s_obj.competency = competency
            s_obj.parent = m_obj
            s_obj.node_level = 2
            s_obj.is_leaf = True
            s_obj.code = s_code
            s_obj.name = row["タスク小分類"]
            s_obj.save()
            s_obj = TaskEvaluation.objects.filter(code=s_code).first()
            print(s_obj)
            eval_item = TaskEvaluationItem.objects.filter(code=row["評価項目コード"],task_evaluation=s_obj).first()
            if eval_item is None:
                eval_item = TaskEvaluationItem()
            eval_item.task_evaluation = s_obj
            eval_item.node_level = 0
            eval_item.is_leaf = True
            eval_item.code = row["評価項目コード"]
            eval_item.name = row["評価項目"]
            eval_item.save()

    def import_profile(self):
        competency = self.get_or_create_competency()
        df = pd.read_excel(self.file,sheet_name="タスクプロフィール一覧")
        df.columns = df.columns.str.replace("\n",'')
        df.columns = df.columns.str.replace(" ",'')
        df["タスクプロフィール種別コード"] = df["タスクプロフィールコード"].str[0:1]
        df["タスクプロフィールグループコード"] = df["タスクプロフィールコード"].str[0:5]
        b_code_last = None
        m_code_last = None
        for index, row in df.iterrows():
            b_code = row["タスクプロフィール種別コード"]
            m_code = row["タスクプロフィールグループコード"]
            s_code = row["タスクプロフィールコード"]
            # 大分類
            b_obj = TaskProfile.objects.filter(code=b_code).first()
            if b_obj is None:
                b_obj = TaskProfile()
            b_obj.competency = competency
            b_obj.node_level = 0
            b_obj.is_leaf = False
            b_obj.code = b_code
            b_obj.name = row["タスクプロフィール種別"]
            b_obj.save()
            print(b_obj)
            b_obj = TaskProfile.objects.filter(code=b_code).first()
            # 中分類
            m_obj = TaskProfile.objects.filter(code=m_code).first()
            if m_obj is None:
                m_obj = TaskProfile()
            m_obj.competency = competency
            m_obj.parent = b_obj
            m_obj.node_level = 1
            m_obj.is_leaf = False
            m_obj.code = m_code
            m_obj.name = row["タスクプロフィールグループ"]
            if "-" == m_obj.name:
                m_obj.name = b_obj.name
            m_obj.save()
            m_obj = TaskProfile.objects.filter(code=m_code).first()
            print(m_obj)
            # プロフィール項目
            s_obj = TaskProfile.objects.filter(code=s_code).first()
            if s_obj is None:
                s_obj = TaskProfile()
            s_obj.competency = competency
            s_obj.parent = m_obj
            s_obj.node_level = 2
            s_obj.is_leaf = True
            s_obj.code = s_code
            s_obj.name = row["タスクプロフィール"]
            s_obj.description = row["タスクプロフィールの説明"]
            s_obj.save()
            s_obj = TaskProfile.objects.filter(code=s_code).first()
            print(s_obj)
            b_code_last = b_code
            m_code_last = m_code

    def import_profile_relation(self):
        df = pd.read_excel(self.file,sheet_name="タスクプロフィール×タスク対応表", header=3)
        df.columns = df.columns.str.replace("\n",'')
        df.columns = df.columns.str.replace(" ",'')
        df = df.drop("Unnamed:0",axis=1)
        df = df.drop("Unnamed:1",axis=1)
        df = df.drop("Unnamed:2",axis=1)
        df = df.drop("Unnamed:3",axis=1)
        df = df.rename(columns={"Unnamed:4":"タスク小分類コード"})
        df = df.rename(columns={"Unnamed:5":"タスク小分類"})
        print(df)
        for index, row in df.iterrows():
            print("------------------------------")
            task_code = row["タスク小分類コード"]
            print(index, " "+task_code)
            for profile_code in df.columns:
                val = row[profile_code]
                if "◎" == val:
                    print("      = " + profile_code)
                    task = TaskEvaluation.objects.filter(code=task_code).first()
                    profile = TaskProfile.objects.filter(code=profile_code).first()
                    if task is not None and profile is not None:
                        taskprofile = TaskEvaluationTaskProfile.objects.filter(task_evaluation_id=task.id, task_profile_id=profile.id).first()
                        if taskprofile is None:
                            taskprofile = TaskEvaluationTaskProfile()
                            taskprofile.task_evaluation = task
                            taskprofile.task_profile = profile
                            taskprofile.weight = 100
                            taskprofile.save()
                elif "○" == val:
                    print("      - " + profile_code)
                    task = TaskEvaluation.objects.filter(code=task_code).first()
                    profile = TaskProfile.objects.filter(code=profile_code).first()
                    if task is not None and profile is not None:
                        taskprofile = TaskEvaluationTaskProfile.objects.filter(task_evaluation_id=task.id, task_profile_id=profile.id).first()
                        if taskprofile is None:
                            taskprofile = TaskEvaluationTaskProfile()
                            taskprofile.task_evaluation = task
                            taskprofile.task_profile = profile
                            taskprofile.weight = 50
                            taskprofile.save()

    def import_skills(self):
        competency = self.get_or_create_competency()
        df = pd.read_excel(self.file,sheet_name="スキル一覧")
        df.columns = df.columns.str.replace("\n",'').str.replace(" ","")
        for index, row in df.iterrows():
            b_code = row["スキルカテゴリコード"]
            m_code = row["スキル分類コード"]
            s_code = row["スキル項目コード"]
            # 大分類
            b_obj = SkillEvaluation.objects.filter(code=b_code).first()
            if b_obj is None:
                b_obj = SkillEvaluation()
            b_obj.competency = competency
            b_obj.node_level = 0
            b_obj.is_leaf = False
            b_obj.code = b_code
            b_obj.name = row["スキルカテゴリ"]
            b_obj.save()
            b_obj = SkillEvaluation.objects.filter(code=b_code).first()
            print(b_obj)
            # 中分類
            m_obj = SkillEvaluation.objects.filter(code=m_code).first()
            if m_obj is None:
                m_obj = SkillEvaluation()
            m_obj.competency = competency
            m_obj.parent = b_obj
            m_obj.node_level = 1
            m_obj.is_leaf = False
            m_obj.code = m_code
            m_obj.name = row["スキル分類"]
            m_obj.save()
            m_obj = SkillEvaluation.objects.filter(code=m_code).first()
            print(m_obj)
            # スキル項目
            s_obj = SkillEvaluation.objects.filter(code=s_code).first()
            if s_obj is None:
                s_obj = SkillEvaluation()
            s_obj.competency = competency
            s_obj.parent = m_obj
            s_obj.node_level = 2
            s_obj.is_leaf = True
            s_obj.code = s_code
            s_obj.name = row["スキル項目"]
            s_obj.save()
            s_obj = SkillEvaluation.objects.filter(code=s_code).first()
            # 知識項目
            if row["知識項目"] != "-":
                eval_item = SkillEvaluationKnowledge.objects.filter(code=row["知識項目コード"],skill_evaluation=s_obj).first()
                if eval_item is None:
                    eval_item = SkillEvaluationKnowledge()
                eval_item.skill_evaluation = s_obj
                eval_item.node_level = 0
                eval_item.is_leaf = True
                eval_item.code = row["知識項目コード"]
                eval_item.name = row["知識項目"]
                eval_item.save()
    
    def import_relation(self):
        df = pd.read_excel(self.file,sheet_name="タスク×スキル対応表")
        df.columns = df.columns.str.replace("\n",'')
        df = df.loc[3:,:]
        df = df.drop("Unnamed: 1",axis=1)
        df = df.drop("Unnamed: 2",axis=1)
        df = df.drop('スキル項目コード ',axis=1)
        df = df.rename(columns={"Unnamed: 0":"スキル項目コード"})

        for index, row in df.iterrows():
            print("------------------------------")
            print(index)
            print(row["スキル項目コード"])
            task_code = row["スキル項目コード"]
            task_obj = TaskEvaluation.objects.filter(code=task_code).first()
            if task_obj is None:
                continue
            for skill_code in df.columns:
                val = row[skill_code]
                if "◎" == val:
                    print("      - " + skill_code)
                    skill_obj = SkillEvaluation.objects.filter(code=skill_code).first()
                    if skill_obj is None:
                        continue
                    task_skill = TaskSkill()
                    task_skill.task_evaluation = task_obj
                    task_skill.skill_evaluation = skill_obj
                    task_skill.save()

    def get_or_create_competency(self):
        competency = Competency.objects.filter(name=self.COMPETENCY_NAME).first()
        if competency is None:
            competency = Competency()
            competency.name = self.COMPETENCY_NAME
            competency.save()
        return Competency.objects.filter(name=self.COMPETENCY_NAME).first()
    
