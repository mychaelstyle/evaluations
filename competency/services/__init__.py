from ..models import TaskEvaluation, TaskFulltext, TaskEvaluationItem, TaskEvaluationTaskProfile, TaskProfile, TaskSkill, SkillEvaluation, SkillEvaluationKnowledge
    
def get_task_fulltext(taskid:int):
    # 関連タスク全ての配列
    related_tasks = []
    # 親を含めてタスクを取得
    task = TaskEvaluation.objects.alive().select_related("parent","parent__parent").get(pk=taskid)
    if task is None:
        raise FileNotFoundError("対象のタスクは見つかりません")
    related_tasks.append(task)
    result = task.name + "\n"
    if task.parent is not None:
        related_tasks.append(task.parent)
        result = result + task.parent.name + "\n"
        if task.parent.parent is not None:
            related_tasks.append(task.parent.parent)
            result = result + task.parent.parent.name + "\n"
    # 子があるなら探す
    tasks = TaskEvaluation.objects.alive().filter(parent=task).all()
    for t in tasks:
        related_tasks.append(t)
        result = result + t.name + "\n"
        # 孫があるなら探す
        children = TaskEvaluation.objects.alive().filter(parent=t).all()
        for c in children:
            related_tasks.append(c)
            result = result + c.name + "\n"

    # タスク評価項目を全て取得
    task_items = TaskEvaluationItem.objects.filter(task_evaluation__in=related_tasks).alive().all()
    for item in task_items:
        result = result + item.name + "\n"
    # 関連するタスクプロフィールを全て取得
    task_profiles = TaskEvaluationTaskProfile.objects.filter(task_evaluation__in=related_tasks).select_related("task_profile").alive().all()
    for item in task_profiles:
        result = result + item.task_profile.name + "\n"
        result = result + item.task_profile.description + "\n"
    # 関連するスキルを収集
    skills = TaskSkill.objects.filter(task_evaluation__in=related_tasks).select_related("skill_evaluation").alive().all()
    for skill in skills:
        result = result + skill.skill_evaluation.name + "\n"
        # スキル関連知識を収集
        knowledges = SkillEvaluationKnowledge.objects.filter(skill_evaluation=skill.skill_evaluation).alive().all()
        for knowledge in knowledges:
            result = result + knowledge.name + "\n"
    return result.lower()