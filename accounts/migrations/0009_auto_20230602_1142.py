# Generated by Django 3.1 on 2023-06-02 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20230517_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='type_address',
            field=models.CharField(max_length=50),
        ),
    ]
