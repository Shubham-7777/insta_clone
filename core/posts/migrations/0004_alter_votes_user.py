# Generated by Django 3.2.10 on 2022-03-08 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220308_1658'),
        ('posts', '0003_alter_votes_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile'),
        ),
    ]
