# Generated by Django 4.2.2 on 2023-10-02 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0007_rename_unita_histransction_consommation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='histransction',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]