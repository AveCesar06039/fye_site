# utils/mixins.py
# B:\desarrollo\FeyEsp2.0\fye_site\utils\mixins.py
class RLSScopeMixin(object):
    """
    Espera que el usuario tenga atributos rls_scope o rls_scope_id.
    Solo aporta utilidad; NO hereda de ninguna CBV para evitar conflictos MRO.
    """
    def get_rls_id(self):
        user = getattr(self, "request", None) and self.request.user or None
        return getattr(user, "rls_scope_id", None) or getattr(user, "rls_id", None)

    def filter_by_rls(self, qs, field="rls_id"):
        rls_id = self.get_rls_id()
        return qs.filter(**{field: rls_id}) if rls_id else qs
