# Generated by Django 3.2.4 on 2021-06-10 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_studentsitecdata_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsitecdata',
            name='cycle_advance_data',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='studentsitecdata',
            name='kardex_data',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='studentsitecdata',
            name='log_data',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='studentsitecdata',
            name='panel_data',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='studentsitecdata',
            name='reinscription_data',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
