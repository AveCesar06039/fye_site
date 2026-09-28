# miembros/forms.py

from django import forms
from django.forms import inlineformset_factory

from .models import Member, Beneficiario, Cargo


class MemberForm(forms.ModelForm):
    """
    Formulario principal de Miembro.
    Incluye campos extra para crear usuario (checkbox + contraseñas).
    """

    crear_usuario = forms.BooleanField(
        required=False,
        label="Crear usuario para acceso al sistema",
        help_text="Si se marca, se creará un usuario usando el correo electrónico y contraseña.",
    )
    password1 = forms.CharField(
        required=False,
        label="Contraseña",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        required=False,
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = Member
        # Usamos todos los campos del modelo, excepto los internos
        fields = "__all__"
        exclude = ["numero_registro", "creado", "modificado", "user"]
        # 👇 Aquí definimos los widgets de fecha con type="date"
        widgets = {
            "fecha_nacimiento": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "fecha_iniciacion": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Esconde campos internos si por alguna razón llegan
        for hidden_field in ["user", "creado", "modificado"]:
            if hidden_field in self.fields:
                self.fields[hidden_field].widget = forms.HiddenInput()
                self.fields[hidden_field].required = False

        # Personalizar etiquetas
        if "foto" in self.fields:
            self.fields["foto"].label = "Fotografía"
        if "fecha_nacimiento" in self.fields:
            self.fields["fecha_nacimiento"].label = "Fecha de nacimiento"
        if "fecha_iniciacion" in self.fields:
            self.fields["fecha_iniciacion"].label = "Fecha de iniciación"
        if "correo_electronico" in self.fields:
            self.fields["correo_electronico"].label = "Correo electrónico"
        if "correo_alterno" in self.fields:
            self.fields["correo_alterno"].label = "Correo alterno"

        if "tipo_sanguineo" in self.fields:
            self.fields["tipo_sanguineo"].label = "Tipo sanguíneo"
        if "observaciones" in self.fields:
            self.fields["observaciones"].label = "Observaciones (alergias, datos importantes)"

    def clean(self):
        """
        Validación de contraseñas SOLO si se marcó 'crear_usuario'.
        """
        cleaned = super().clean()
        crear_usuario = cleaned.get("crear_usuario")
        pwd1 = cleaned.get("password1")
        pwd2 = cleaned.get("password2")

        if crear_usuario:
            # Obligar a capturar correo y contraseña
            correo = cleaned.get("correo_electronico") or cleaned.get("correo")
            if not correo:
                self.add_error(
                    "correo_electronico",
                    "Debes capturar un correo para crear el usuario.",
                )

            if not pwd1 or not pwd2:
                self.add_error("password1", "Debes capturar y confirmar la contraseña.")
            elif pwd1 != pwd2:
                self.add_error("password2", "Las contraseñas no coinciden.")

        return cleaned


class BeneficiarioForm(forms.ModelForm):
    """
    Formulario de Beneficiario.
    Usa fields='__all__' para que no truene si el modelo cambia.
    Esconde campos de relación/internos si existen.
    """

    class Meta:
        model = Beneficiario
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Esconde campos internos/relacionales si existen
        for hidden_field in ["member", "creado", "modificado"]:
            if hidden_field in self.fields:
                self.fields[hidden_field].widget = forms.HiddenInput()
                self.fields[hidden_field].required = False

        # Ajustar etiquetas si los campos existen
        if "nombre_completo" in self.fields:
            self.fields["nombre_completo"].label = "Nombre completo"
        if "relacion" in self.fields:
            self.fields["relacion"].label = "Relación o parentesco"
        if "correo" in self.fields:
            self.fields["correo"].label = "Correo del beneficiario"
        if "telefono" in self.fields:
            self.fields["telefono"].label = "Teléfono del beneficiario"
        if "porcentaje" in self.fields:
            self.fields["porcentaje"].label = "Porcentaje"


# Inline formset para capturar beneficiarios desde el formulario de miembro
BeneficiarioFormSet = inlineformset_factory(
    Member,
    Beneficiario,
    form=BeneficiarioForm,
    extra=1,
    can_delete=True,
)
