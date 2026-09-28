# miembros/templatetags/forms_extras.py
from django import template

register = template.Library()

@register.filter(name="add_class")
def add_class(field, css):
    """
    Añade clases CSS a un widget de formulario sin perder las existentes.
    Uso: {{ field|add_class:"w-full px-2" }}
    """
    existing = field.field.widget.attrs.get("class", "")
    new = (existing + " " + css).strip() if existing else css
    return field.as_widget(attrs={**field.field.widget.attrs, "class": new})

@register.filter(name="set_attr")
def set_attr(field, arg):
    """
    Setea un atributo HTML genérico: 'placeholder:Texto aquí'
    Uso: {{ field|set_attr:"placeholder:Ejemplo" }}
    """
    try:
        key, value = arg.split(":", 1)
    except ValueError:
        return field
    attrs = {**field.field.widget.attrs, key: value}
    return field.as_widget(attrs=attrs)
