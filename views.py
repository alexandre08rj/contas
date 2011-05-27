from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect

from models import ContaPagar, ContaReceber, CONTA_STATUS_APAGAR, CONTA_STATUS_PAGO
from forms import FormPagamento

def contas(request):
    contas_a_pagar = ContaPagar.objects.filter(
        status=CONTA_STATUS_APAGAR,
        )
    contas_a_receber = ContaReceber.objects.filter(
        status=CONTA_STATUS_PAGO,
        )
    
    return render_to_response(
        'contas/contas.html',
        locals(),
        context_instance=RequestContext(request),
        )
    
def conta(request, conta_id, classe):
    conta = get_object_or_404(classe, id=conta_id)
    form_pagamento = FormPagamento()
    return render_to_response(
        'contas/conta.html',
        locals(),
        context_instance=RequestContext(request),
        )
    
def conta_pagamento(request, conta_id, classe):
    conta = get_object_or_404(classe, id=conta_id)
    
    if request.method == 'POST':
        form_pagamento = FormPagamento(request.POST)
        
        if form_pagamento.is_valid():
            form_pagamento.salvar_pagamento(conta)
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])