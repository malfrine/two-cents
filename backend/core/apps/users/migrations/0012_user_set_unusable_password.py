from django.db import migrations


def set_unusable_password(apps, schema_editor):

    User = apps.get_model("users", "User")
    for user in User.objects.all():
        user.password = ""
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0011_user_stripe_id"),
    ]

    operations = [migrations.RunPython(set_unusable_password)]
