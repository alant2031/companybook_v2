import os
from django.core.files.storage import default_storage
from django.utils.text import slugify


def set_key(instance, key, model):
    if instance.pk:
        # Retrieve the existing instance from the database
        try:
            existing_instance = model.objects.get(pk=instance.pk)
        except model.DoesNotExist:
            return

        current_field = getattr(existing_instance, key)

        # Delete the previous image file from the storage
        if current_field and current_field != getattr(instance, key):
            default_storage.delete(current_field.name)
    # Generate a unique filename by appending a timestamp
    instance_field = getattr(instance, key)
    have_path = bool(os.path.dirname(instance_field.name))
    if not have_path:
        slug = slugify(instance.company.razao)
        pk = str(instance.company.pk)
        pathname = os.path.join(pk, f"{slug}-{key}.jpg")
        unique_filename = pathname
        instance_field.name = unique_filename
