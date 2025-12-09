from django import forms
from django.contrib.auth.models import User
from .models import Pedido

class CheckoutForm(forms.ModelForm):
    # Campos simulados de pago (no se guardan en BD por seguridad)
    numero_tarjeta = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': '0000 0000 0000 0000', 'class': 'form-control'}))
    cvv = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'placeholder': '123', 'class': 'form-control', 'maxlength':'3'}))
    caducidad = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'MM/YY', 'class': 'form-control'}))
    
    class Meta:
        model = Pedido
        fields = ['nombre_cliente', 'email_cliente', 'telefono_cliente', 'domicilio', 'forma_pago']
        widgets = {
            'forma_pago': forms.RadioSelect(choices=[('tarjeta', 'Tarjeta de Crédito/Débito'), ('paypal', 'PayPal')]),
            'domicilio': forms.Textarea(attrs={'rows': 3}),
        }

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden")