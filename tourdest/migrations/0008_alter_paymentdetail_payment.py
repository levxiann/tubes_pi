# Generated by Django 4.1.7 on 2023-05-08 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tourdest", "0007_alter_shopposition_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentdetail",
            name="payment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tourdest.payment"
            ),
        ),
    ]