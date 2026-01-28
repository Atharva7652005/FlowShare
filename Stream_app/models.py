import uuid
from django.db import models

# Create your models here.
class StorageEntry(models.Model):
    storage_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    storage_code = models.CharField(max_length=4, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class StorageFiles(models.Model):
    storage_entry_id = models.ForeignKey(
        StorageEntry,
        related_name="storage_files",
        on_delete=models.CASCADE
    )
    storage_files = models.FileField(upload_to="storageFiles")