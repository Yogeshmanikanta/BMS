# Generated by Django 3.2.19 on 2024-12-24 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='movies/')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3)),
                ('cast', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('time', models.DateTimeField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='theaters', to='movies.movie')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.CharField(max_length=10)),
                ('is_booked', models.BooleanField(default=False)),
                ('theater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='movies.theater')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booked_at', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('seat', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='movies.seat')),
                ('theater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.theater')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]