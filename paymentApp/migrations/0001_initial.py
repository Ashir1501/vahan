# Generated by Django 4.2.14 on 2024-08-18 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customerApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_fare', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(choices=[('pending', 'pending'), ('paid', 'paid')], max_length=30)),
                ('advance_payment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('advance_payment_percent', models.CharField(choices=[('25', '25'), ('50', '50')], max_length=10)),
                ('advance_payment_type', models.CharField(choices=[('Wallet', 'Wallet'), ('credit', 'credit'), ('debit', 'debit')], max_length=20)),
                ('pending_paymeny_Type', models.CharField(choices=[('online', 'online'), ('cash', 'cash'), ('wallet', 'wallet')], max_length=20)),
                ('advance_payment_date', models.DateTimeField()),
                ('pending_payment_date', models.DateTimeField()),
                ('ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customerApp.ride')),
            ],
        ),
    ]
