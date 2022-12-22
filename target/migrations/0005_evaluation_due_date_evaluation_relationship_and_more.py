# Generated by Django 4.1 on 2022-12-20 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0004_alter_targettaskevaluationitemaction_action_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='due_date',
            field=models.DateField(blank=True, null=True, verbose_name='due_date'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='relationship',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(40, 'boss'), (30, 'colleague'), (20, 'clients'), (10, 'subordinate'), (0, 'friends')], null=True, verbose_name='relationship'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='remote_address',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='remote_address'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='remote_host',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='remote_host'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'new'), (10, 'initialized'), (20, 'in_progress'), (100, 'completed')], default=0, verbose_name='status'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='user_agent',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='remote_host'),
        ),
        migrations.AddField(
            model_name='evaluationitemvalue',
            name='remote_address',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='remote_address'),
        ),
        migrations.AddField(
            model_name='evaluationitemvalue',
            name='remote_host',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='remote_host'),
        ),
        migrations.AddField(
            model_name='evaluationitemvalue',
            name='user_agent',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='remote_host'),
        ),
    ]