from .models import AuditLog
from django.utils.deprecation import MiddlewareMixin
import ipaddress

class AuditMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        request._audit_view = f"{view_func.__module__}.{view_func.__name__}"

    def process_response(self, request, response):
        try:
            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                method=getattr(request, "method", ""),
                path=getattr(request, "path", ""),
                view=getattr(request, "_audit_view", ""),
                status=response.status_code,
                ip=request.META.get("REMOTE_ADDR") or "",
                ua=request.META.get("HTTP_USER_AGENT") or "",
            )
        except Exception:
            pass
        return response
