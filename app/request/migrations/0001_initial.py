# Generated by Django 2.0.2 on 2019-08-10 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_jalali.db.models
import request.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_fa', django_jalali.db.models.jDateField(default=django.utils.timezone.now)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('body', models.TextField(blank=True)),
                ('is_read', models.BooleanField(default=False)),
                ('object_id', models.PositiveIntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='FrameSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ICType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='IEType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='IMType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='IPType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='IssueType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('summary', models.TextField(blank=True, max_length=600, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('temp_number', models.IntegerField(blank=True, null=True, unique=True)),
                ('amount', models.FloatField()),
                ('payment_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_fa', django_jalali.db.models.jDateField(default=django.utils.timezone.now)),
                ('due_date', django_jalali.db.models.jDateField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, max_length=600, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('read_payment', 'Can read payment details'), ('index_payment', 'Can see list of payments')),
            },
        ),
        migrations.CreateModel(
            name='PaymentFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to=request.models.upload_location)),
                ('pay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.Payment')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='PrefSpec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.BigIntegerField(default=99009900)),
                ('qty', models.IntegerField(default=1)),
                ('type', models.TextField(default=1)),
                ('price', models.FloatField(blank=True, null=True)),
                ('kw', models.FloatField()),
                ('rpm', models.IntegerField()),
                ('voltage', models.IntegerField(default=380)),
                ('ip_type', models.IntegerField(blank=True, null=True)),
                ('ic_type', models.IntegerField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, max_length=500, null=True)),
                ('considerations', models.TextField(blank=True, max_length=500, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('sent', models.BooleanField(default=False)),
                ('qty_sent', models.IntegerField(blank=True, default=0, null=True)),
                ('finished', models.BooleanField(default=False)),
                ('ic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='request.ICType')),
                ('im', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='request.IMType')),
                ('ip', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='request.IPType')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to=request.models.upload_location)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('summary', models.TextField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='ReqSpec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.BigIntegerField(default=99009900)),
                ('qty', models.IntegerField(default=1)),
                ('kw', models.FloatField()),
                ('rpm', models.IntegerField()),
                ('voltage', models.IntegerField(default=380)),
                ('ip_type', models.IntegerField(blank=True, null=True)),
                ('ic_type', models.IntegerField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, max_length=500, null=True)),
                ('tech', models.BooleanField(default=False)),
                ('price', models.BooleanField(default=False)),
                ('permission', models.BooleanField(default=False)),
                ('sent', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('cancelled', models.BooleanField(default=False)),
                ('finished', models.BooleanField(default=False)),
                ('frame_size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='request.FrameSize')),
                ('ic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='request.ICType')),
                ('ie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='request.IEType')),
                ('im', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='request.IMType')),
                ('ip', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='request.IPType')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('index_reqspecs', 'can see list of request Specs'), ('read_reqspecs', 'can read request Specs')),
            },
        ),
        migrations.CreateModel(
            name='RequestFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to=request.models.upload_location)),
            ],
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('temp_number', models.IntegerField(blank=True, null=True, unique=True)),
                ('parent_number', models.IntegerField(blank=True, null=True)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_fa', django_jalali.db.models.jDateField(default=django.utils.timezone.now)),
                ('date_finished', django_jalali.db.models.jDateField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, max_length=1000, null=True)),
                ('added_by_customer', models.BooleanField(default=False)),
                ('edited_by_customer', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('finished', models.BooleanField(default=False)),
                ('date_modified', models.DateTimeField(blank=True, null=True)),
                ('follow_up', models.TextField(blank=True, null=True)),
                ('to_follow', models.BooleanField(default=False)),
                ('on', models.BooleanField(default=False)),
                ('colleagues', models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='customer.Customer')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='req_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('index_requests', 'can see list of requests'), ('read_requests', 'can read requests'), ('public_requests', 'public in requests'), ('sale_expert', 'can edit own stuff')),
            },
        ),
        migrations.CreateModel(
            name='RpmType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rpm', models.IntegerField()),
                ('pole', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Xpref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('number_auto', models.IntegerField(unique=True)),
                ('number_td', models.IntegerField(blank=True, null=True)),
                ('temp_number', models.IntegerField(blank=True, null=True)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_fa', django_jalali.db.models.jDateField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(blank=True, null=True)),
                ('exp_date_fa', django_jalali.db.models.jDateField(default=django.utils.timezone.now)),
                ('perm_number', models.IntegerField(blank=True, null=True)),
                ('perm_date', django_jalali.db.models.jDateField(blank=True, null=True)),
                ('due_date', django_jalali.db.models.jDateField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, max_length=600, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('perm', models.BooleanField(default=False)),
                ('follow_up', models.TextField(blank=True, null=True)),
                ('to_follow', models.BooleanField(default=False)),
                ('on', models.BooleanField(default=False)),
                ('issue_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='request.IssueType')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('req_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='request.Requests')),
            ],
            options={
                'permissions': (('index_proforma', 'Can index Proforma'), ('read_proforma', 'Can read Proforma')),
            },
        ),
        migrations.AddField(
            model_name='requestfiles',
            name='req',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.Requests'),
        ),
        migrations.AddField(
            model_name='reqspec',
            name='req_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.Requests'),
        ),
        migrations.AddField(
            model_name='reqspec',
            name='rpm_new',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='request.RpmType'),
        ),
        migrations.AddField(
            model_name='reqspec',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='request.ProjectType'),
        ),
        migrations.AddField(
            model_name='proffiles',
            name='prof',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.Xpref'),
        ),
        migrations.AddField(
            model_name='prefspec',
            name='reqspec_eq',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='request.ReqSpec'),
        ),
        migrations.AddField(
            model_name='prefspec',
            name='xpref_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.Xpref'),
        ),
        migrations.AddField(
            model_name='payment',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='request.PaymentType'),
        ),
        migrations.AddField(
            model_name='payment',
            name='xpref_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='request.Xpref'),
        ),
    ]
