from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
import os
import pandas as pd

from competency.models import TaskEvaluation, TaskFulltext
from competency.services import get_task_fulltext

class Command(BaseCommand):
    help = 'iコンピテンシディクショナリのExcelファイルをデータベースにインポートするためのコマンドです'
    file = None
    COMPETENCY_NAME = "iコンピテンシディレクトリ"
    
    def handle(self, *args, **options):
        try:
            print('バッチが動きました： {}'.format(options))
            self.make_searchtext()
        except Exception as e:
            print(e)

    def make_searchtext(self):
        tasks = TaskEvaluation.objects.alive().all()
        for task in tasks:
            print("-----------------------")
            tasktext = TaskFulltext.objects.filter(task_evaluation_id=task.id).first()
            if tasktext is None:
                tasktext = TaskFulltext()
                tasktext.task_evaluation = task
            text = get_task_fulltext(task.id)
            print(text)
            tasktext.contents = text
            tasktext.save()
