from django.db import models
from django.conf import settings
class AuditLog(models.Model):
    user = models.ForeignKey("accounts.User", null=True, blank=True, on_delete=models.SET_NULL)
    method = models.CharField(max_length=8)
    path = models.CharField(max_length=255)
    view = models.CharField(max_length=255, blank=True)
    status = models.PositiveIntegerField()
    ip = models.GenericIPAddressField(null=True, blank=True)
    ua = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]
