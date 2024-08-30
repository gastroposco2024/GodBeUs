from django import forms
from .models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['nota_egreso', 'fecha', 'metodo_pago', 'observaciones', 'cantidad', 'impuesto', 'valor', 'archivo_adjunto', 'concepto']

    def __init__(self, *args, **kwargs):
        super(PagoForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['observaciones'].widget.attrs.update({
            'rows': 2,
            'cols': 50
        })
        if 'cantidad' not in self.initial:
            self.fields['cantidad'].initial = 1