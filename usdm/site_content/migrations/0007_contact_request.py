from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("site_content", "0006_internal_page_translations")]
    operations = [
        migrations.CreateModel(
            name="ContactRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=120)),
                ("last_name", models.CharField(blank=True, max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=80)),
                ("message", models.TextField()),
                ("language", models.CharField(choices=[("uk", "Українська"), ("de", "Deutsch")], max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "contact_requests", "ordering": ("-created_at",)},
        ),
    ]
