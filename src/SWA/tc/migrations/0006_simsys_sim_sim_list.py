# Generated by Django 4.1.2 on 2022-12-02 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tc', '0005_remove_testconductor_button_value_sim_button_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimSys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sym_name', models.CharField(default='', max_length=15)),
                ('button_value', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='sim',
            name='sim_list',
            field=models.ManyToManyField(to='tc.simsys', verbose_name='Sys'),
        ),
    ]