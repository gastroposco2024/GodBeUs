from django import forms
from .models import Profile, Cliente

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'address', 
            'phone', 
            'company', 
            'logo',
            'tipo_documento', 
            'numero_identificacion', 
            'nombre', 
            'segundo_nombre', 
            'apellidos', 
            'correo', 
            'municipio_departamento', 
            'direccion',
            'responsabilidad_tributaria', 
            'tipo_persona'
        ]
    
    # Personalización de widgets
    address = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'})
    )
    phone = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'})
    )
    company = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Empresa'})
    )
    logo = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    
    tipo_documento = forms.ChoiceField(
        choices=Profile.TIPO_DOCUMENTO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tipo de documento'})
    )
    numero_identificacion = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de identificación'})
    )
    nombre = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'})
    )
    segundo_nombre = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Segundo nombre'})
    )
    apellidos = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'})
    )
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    municipio_departamento = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Municipio/Departamento'})
    )
    direccion = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'})
    )
    
    responsabilidad_tributaria = forms.ChoiceField(
        choices=Profile.RESPONSABILIDAD_TRIBUTARIA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tipo_persona = forms.ChoiceField(
        choices=Profile.TIPO_PERSONA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'direccion', 'documento']  # Ajusta según los campos de tu modelo
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
        }