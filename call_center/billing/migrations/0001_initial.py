# Generated by Django 2.1 on 2018-08-23 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CallStart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('source', models.CharField(max_length=20)),
                ('destination', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CallBill',
            fields=[
                ('call_start', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='billing.CallStart')),
                ('billable_duration', models.DurationField()),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='CallEnd',
            fields=[
                ('start', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='billing.CallStart')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='callbill',
            name='call_end',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='billing.CallEnd'),
        ),
    ]
