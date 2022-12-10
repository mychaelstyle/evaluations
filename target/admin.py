from django.contrib import admin

from .models import Evaluation, EvaluationItemValue, TargetTaskEvaluationItem, Target, TargetTaskEvaluationItemAction

# Register your models here.
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','grade','industory','industory_opt','org_name','department_name','job','position','role')
    ordering = ('-created_at',)
admin.site.register(Evaluation,EvaluationAdmin)

class EvaluationItemValueAdmin(admin.ModelAdmin):
    list_display = ('evaluation','target_item','score','self_score')
    ordering = ('-created_at',)
admin.site.register(EvaluationItemValue,EvaluationItemValueAdmin)

class TargetAdmin(admin.ModelAdmin):
    list_display = ('viewname','first_name','last_name','grade','industory','industory_opt','org_name','department_name','job','position','role')
    ordering = ('-created_at',)
admin.site.register(Target,TargetAdmin)

class TargetTaskEvaluationItemAdmin(admin.ModelAdmin):
    list_display = ('target','item')
    ordering = ('-created_at',)
admin.site.register(TargetTaskEvaluationItem,TargetTaskEvaluationItemAdmin)

class TargetTaskEvaluationItemActionAdmin(admin.ModelAdmin):
    list_display = ('target_item','name','description','progress')
    ordering = ('-created_at',)
admin.site.register(TargetTaskEvaluationItemAction,TargetTaskEvaluationItemActionAdmin)
