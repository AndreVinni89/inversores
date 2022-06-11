# Generated by Django 4.0.5 on 2022-06-11 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SimpleBuy', '0004_auto_20220302_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inversor',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='localidade',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Leitura_H',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField()),
                ('data', models.DateTimeField()),
                ('parametro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SimpleBuy.parametro')),
            ],
        ),
    ]
