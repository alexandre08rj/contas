from datetime import date
from django import forms

class FormPagamento(forms.Form):
    valor = forms.DecimalField(max_digits=15, decimal_places=2)
    
    def salvar_pagamento(self, conta):
        return conta.lancar_pagamento(
            data_pagamento=date.today(),
            valor=self.cleaned_data['valor'],                          
            )