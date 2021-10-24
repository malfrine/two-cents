from django.db import migrations
from django.contrib.auth.hashers import make_password


def set_unusable_password(apps, schema_editor):

    User = apps.get_model("users", "User")
    for user in User.objects.all():
        user.password = make_password(None)
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0012_user_set_unusable_password"),
    ]

    operations = [migrations.RunPython(set_unusable_password)]
