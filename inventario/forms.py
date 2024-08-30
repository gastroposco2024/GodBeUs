from django import forms
from .models import Producto, PlatoProducto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'cantidad_disponible', 'precio',  'unidad_medida']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad disponible'}),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Precio', 
                'step': '0.01',  # Permite decimales
                'min': '0'       # Establece el valor mínimo permitido (opcional)
            }),
            'unidad_medida': forms.Select(attrs={'class': 'form-control'})
        }

class AsociarProductoForm(forms.ModelForm):
    class Meta:
        model = PlatoProducto
        fields = ['producto', 'cantidad_necesaria', 'unidad_medida']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad_necesaria': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad necesaria'}),
            'unidad_medida': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.all()
        self.fields['unidad_medida'].queryset = UnidadMedida.objects.all()