# Generated by Django 4.2.3 on 2023-08-07 11:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="otp",
            name="mobile_number",
            field=models.CharField(max_length=10, unique=True),
        ),
    ]