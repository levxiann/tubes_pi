# Generated by Django 4.1.7 on 2023-05-08 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "tourdest",
            "0005_alter_user_managers_user_date_joined_user_first_name_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="shop",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT, to="tourdest.shop"
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="paymentdetail",
            name="payment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT, to="tourdest.payment"
            ),
        ),
        migrations.AlterField(
            model_name="paymentdetail",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT, to="tourdest.product"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="shop",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT, to="tourdest.shop"
            ),
        ),
        migrations.AlterField(
            model_name="shopposition",
            name="shop",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT, to="tourdest.shop"
            ),
        ),
        migrations.AlterField(
            model_name="shopposition",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
