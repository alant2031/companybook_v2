# Generated by Django 4.2.2 on 2023-08-31 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscriber",
            name="ytb_id",
            field=models.CharField(
                blank=True, max_length=16, verbose_name="Youtube ID"
            ),
        ),
        migrations.AlterField(
            model_name="subscriber",
            name="company",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                to="core.company",
                verbose_name="Entidade",
            ),
        ),
    ]
