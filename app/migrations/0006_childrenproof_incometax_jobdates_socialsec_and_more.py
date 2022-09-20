# Generated by Django 4.1.1 on 2022-09-20 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_joboutline_workpermit_applicant_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChildrenProof',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.UUIDField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='IncomeTax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.UUIDField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('available', models.BooleanField(default=True, verbose_name='Income Tax card is available')),
                ('bracket', models.CharField(max_length=63, verbose_name='Tax bracket')),
                ('children', models.BooleanField(verbose_name='Children')),
                ('religion', models.CharField(max_length=63, verbose_name='Religious denomination')),
                ('exempt_year', models.FloatField(verbose_name='tax allowance per year')),
                ('exempt_month', models.FloatField(verbose_name='tax allowance per month')),
                ('finoffice', models.CharField(blank=True, max_length=255, verbose_name='Tax office')),
                ('taxnum', models.CharField(max_length=63, verbose_name='Tax identification number')),
                ('lumptax', models.BooleanField(verbose_name='2% lump-sum taxation for marginal employees (if no income tax card is available)')),
                ('payslide', models.CharField(choices=[('DontApp', 'Do not apply sliding pay scale (remuneration over 800 €)'), ('NoTopUp', 'Apply sliding pay scale, without top-up pension insurance'), ('TopUp', 'Apply sliding pay scale, with top-up pension insurance')], max_length=7, verbose_name='Sliding pay scale')),
            ],
        ),
        migrations.CreateModel(
            name='JobDates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.UUIDField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('start', models.DateField(verbose_name='Start Date YYYY-MM-DD')),
                ('end', models.DateField(verbose_name='End Date YYYY-MM-DD (if known)')),
            ],
        ),
        migrations.CreateModel(
            name='SocialSec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.UUIDField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('insurance', models.CharField(max_length=127, verbose_name='Health insurance company')),
                ('socialsec', models.CharField(max_length=63, verbose_name='Social security number')),
                ('birthplace', models.CharField(max_length=127, verbose_name='Birth name and Birthplace')),
            ],
        ),
        migrations.AddField(
            model_name='applicant',
            name='education',
            field=models.CharField(default='hauptschule', max_length=63, verbose_name='School education / degree'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applicant',
            name='training',
            field=models.CharField(blank=True, max_length=63, verbose_name='Preofessional training (if applicable)'),
        ),
    ]