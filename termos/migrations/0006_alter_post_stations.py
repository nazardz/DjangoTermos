# Generated by Django 4.1.4 on 2023-01-17 05:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('termos', '0005_alter_post_stations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='stations',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='termos.station'),
        ),
    ]
