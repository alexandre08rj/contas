from django.contrib import admin
from django.contrib.admin.options import ModelAdmin, TabularInline

from models import Pessoa, Historico, Conta, ContaPagar, ContaReceber,\
    PagamentoPago, PagamentoRecebido

class AdminPessoa(ModelAdmin):
    list_display = ('nome','telefone','cpf','valor_total','quantidade_contas')
    
class AdminHistorico(ModelAdmin):
    list_display = ('descricao','valor_total')
    
class AdminConta(ModelAdmin):
    list_display = ('data_vencimento','valor','status','operacao','historico','pessoa',)
    search_fields = ('descricao',)
    list_filter = ('data_vencimento','status','operacao','historico','pessoa',)
    
class InlinePagamentoPago(TabularInline):
    model = PagamentoPago
    
class AdminContaPagar(ModelAdmin):
    list_display = ('data_vencimento','valor','status','historico','pessoa',)
    search_fields = ('descricao',)
    list_filter = ('data_vencimento','status','historico','pessoa',)
    exclude = ['operacao',]
    inlines = [InlinePagamentoPago,]
    date_hierarchy = 'data_vencimento'
    
    def changelist_view(self, request, extra_context={}):
        qs = self.queryset(request)
        
        extra_context['soma'] = sum([i['valor'] for i in qs.values('valor')])
        extra_context['total'] = qs.count()
        
        return super(AdminContaPagar, self).changelist_view(request, extra_context)

class InlinePagamentoRecebido(TabularInline):
    model = PagamentoRecebido
    

class AdminContaReceber(ModelAdmin):
    list_display = ('data_vencimento','valor','status','historico','pessoa',)
    search_fields = ('descricao',)
    list_filter = ('data_vencimento','status','historico','pessoa',)
    exclude = ['operacao',]
    inlines = [InlinePagamentoRecebido,]
    date_hierarchy = 'data_vencimento'
    
admin.site.register(Pessoa, AdminPessoa)
admin.site.register(Historico, AdminHistorico)
admin.site.register(Conta, AdminConta)
admin.site.register(ContaPagar, AdminContaPagar)
admin.site.register(ContaReceber, AdminContaReceber)
