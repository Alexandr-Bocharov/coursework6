# Generated by Django 4.2 on 2024-10-31 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("newsletter", "0003_alter_newsletter_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="email",
            field=models.EmailField(max_length=150, verbose_name="почта"),
        ),
    ]
