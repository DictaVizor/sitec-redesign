# Generated by Django 3.2.4 on 2021-06-10 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentSitecData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('panel_data', models.TextField()),
                ('reinscription_data', models.TextField()),
                ('cycle_advance_data', models.TextField()),
                ('kardex_data', models.TextField()),
                ('log_data', models.TextField()),
            ],
        ),
    ]
