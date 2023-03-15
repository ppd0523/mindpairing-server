import os


def path_and_rename(instance, filename: str):
    upload_to = 'post_images/'
    ext = filename.split('.')[-1]
    if instance.id:
        filename = f"{instance.id}.{ext}"

    return os.path.join(upload_to, filename)
