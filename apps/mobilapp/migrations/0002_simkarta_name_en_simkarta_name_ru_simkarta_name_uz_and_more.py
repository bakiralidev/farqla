# apps/mobilapp/migrations/0002_....py
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('mobilapp', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[  # <-- faqat STATE
                migrations.AddField(
                    model_name='simkarta',
                    name='name_en',
                    field=models.CharField(max_length=100, null=True, verbose_name='nomi'),
                ),
                migrations.AddField(
                    model_name='simkarta',
                    name='name_ru',
                    field=models.CharField(max_length=100, null=True, verbose_name='nomi'),
                ),
                migrations.AddField(
                    model_name='simkarta',
                    name='name_uz',
                    field=models.CharField(max_length=100, null=True, verbose_name='nomi'),
                ),
                migrations.AddField(
                    model_name='simkarta',
                    name='tarif_en',
                    field=models.CharField(max_length=100, null=True, verbose_name='tarif nomi'),
                ),
                migrations.AddField(
                    model_name='simkarta',
                    name='tarif_ru',
                    field=models.CharField(max_length=100, null=True, verbose_name='tarif nomi'),
                ),
                migrations.AddField(
                    model_name='simkarta',
                    name='tarif_uz',
                    field=models.CharField(max_length=100, null=True, verbose_name='tarif nomi'),
                ),
                migrations.AddField(
                    model_name='simkarta',
                    name='tavsif_en',
                    field=models.TextField(blank=True, null=True, verbose_name='tavsif'),
                ),
                migrations.AddField(
                    model_name='simkarta',
                    name='tavsif_ru',
                    field=models.TextField(blank=True, null=True, verbose_name='tavsif'),
                ),
                migrations.AddField(
                    model_name='simkarta',
                    name='tavsif_uz',
                    field=models.TextField(blank=True, null=True, verbose_name='tavsif'),
                ),
            ],
            database_operations=[  # <-- DBga hech narsa qilmaysiz
            ],
        ),
    ]
