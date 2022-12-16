from django.contrib import admin
from .models import Competency, TaskEvaluation, TaskEvaluationItem, SkillEvaluation, SkillEvaluationKnowledge, TaskSkill, TaskProfile, TaskEvaluationTaskProfile, TaskFulltext, TaskSearchWords,Synonym

# Register your models here.
class CompetencyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('-created_at',)
admin.site.register(Competency,CompetencyAdmin)
    
class TaskEvaluationAdmin(admin.ModelAdmin):
    list_display = ('competency','parent','code','name')
    ordering = ('-created_at',)
admin.site.register(TaskEvaluation,TaskEvaluationAdmin)

class TaskEvaluationItemAdmin(admin.ModelAdmin):
    list_display = ('task_evaluation','parent','code','name')
    ordering = ('-created_at',)
admin.site.register(TaskEvaluationItem,TaskEvaluationItemAdmin)

class TaskProfileAdmin(admin.ModelAdmin):
    list_display = ('competency','code','name','description')
    ordering = ('-created_at',)
admin.site.register(TaskProfile,TaskProfileAdmin)

class TaskEvaluationTaskProfileAdmin(admin.ModelAdmin):
    list_display = ('task_evaluation','task_profile','weight')
    ordering = ('-created_at',)
admin.site.register(TaskEvaluationTaskProfile,TaskEvaluationTaskProfileAdmin)

class SkillEvaluationAdmin(admin.ModelAdmin):
    list_display = ('competency','parent','code','name')
    ordering = ('-created_at',)
admin.site.register(SkillEvaluation,SkillEvaluationAdmin)

class SkillEvaluationKnowledgeAdmin(admin.ModelAdmin):
    list_display = ('skill_evaluation','parent','code','name')
    ordering = ('-created_at',)
admin.site.register(SkillEvaluationKnowledge,SkillEvaluationKnowledgeAdmin)

class TaskSkillAdmin(admin.ModelAdmin):
    list_display = ('task_evaluation','skill_evaluation')
    ordering = ('-created_at',)
admin.site.register(TaskSkill,TaskSkillAdmin)

class TaskFulltextAdmin(admin.ModelAdmin):
    list_display = ('task_evaluation','contents')
    ordering = ('-updated_at',)
admin.site.register(TaskFulltext,TaskFulltextAdmin)

class TaskSearchWordsAdmin(admin.ModelAdmin):
    list_display = ('word','searched_count')
    ordering = ('-searched_count',)
admin.site.register(TaskSearchWords,TaskSearchWordsAdmin)

class SynonymAdmin(admin.ModelAdmin):
    list_display = ('word','synonym','available')
    ordering = ('-created_at',)
admin.site.register(Synonym,SynonymAdmin)


