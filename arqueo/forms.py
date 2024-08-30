from django import forms
from .models import ArqueoCajaInicial

class ArqueoCajaForm(forms.ModelForm):
    class Meta:
        model = ArqueoCajaInicial
        fields = [
            'efectivo_inicial', 'efectivo_final', 'observaciones', 'estado',
            'total_efectivo', 'total_consignacion', 'total_transferencia',
            'total_cheque', 'total_tarjeta_credito', 'total_tarjeta_debito',
            'monedas_50', 'monedas_100', 'monedas_200', 'monedas_500', 'monedas_1000',
            'billetes_2000', 'billetes_5000', 'billetes_10000', 'billetes_20000', 'billetes_50000', 'billetes_100000'
        ]
        widgets = {
            'efectivo_inicial': forms.NumberInput(attrs={'class': 'form-control'}),
            'efectivo_final': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
            'estado': forms.HiddenInput(),
            'total_efectivo': forms.HiddenInput(),
            'total_consignacion': forms.HiddenInput(),
            'total_transferencia': forms.HiddenInput(),
            'total_cheque': forms.HiddenInput(),
            'total_tarjeta_credito': forms.HiddenInput(),
            'total_tarjeta_debito': forms.HiddenInput(),
            'monedas_50': forms.NumberInput(attrs={'class': 'form-control'}),
            'monedas_100': forms.NumberInput(attrs={'class': 'form-control'}),
            'monedas_200': forms.NumberInput(attrs={'class': 'form-control'}),
            'monedas_500': forms.NumberInput(attrs={'class': 'form-control'}),
            'monedas_1000': forms.NumberInput(attrs={'class': 'form-control'}),
            'billetes_2000': forms.NumberInput(attrs={'class': 'form-control'}),
            'billetes_5000': forms.NumberInput(attrs={'class': 'form-control'}),
            'billetes_10000': forms.NumberInput(attrs={'class': 'form-control'}),
            'billetes_20000': forms.NumberInput(attrs={'class': 'form-control'}),
            'billetes_50000': forms.NumberInput(attrs={'class': 'form-control'}),
            'billetes_100000': forms.NumberInput(attrs={'class': 'form-control'}),
        }