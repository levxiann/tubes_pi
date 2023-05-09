# Generated by Django 4.1.7 on 2023-05-09 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tourdest", "0009_alter_payment_options_remove_payment_payment_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="status",
            field=models.CharField(
                choices=[("P", "Paid"), ("NP", "Not Paid"), ("R", "Rejected")],
                default="NP",
                max_length=2,
            ),
        ),
    ]