# Generated by Django 2.0.2 on 2019-06-21 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0060_auto_20190618_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('summary', models.TextField(blank=True, max_length=600, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='xpref',
            name='issue_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='request.IssueType'),
        ),
    ]