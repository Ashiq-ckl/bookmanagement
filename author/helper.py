import os

def get_last_pk(instance):
    instance_id = 1
    if instance.pk is None:
        instance_last = instance.__class__.objects.last()
        if instance_last != None:
            instance_id = instance_last.pk + 1
    else:
        instance_id = instance.pk
    return instance_id

def delete_files(path):
    if os.path.isfile(path):
        os.remove(path)
