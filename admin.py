from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from models import Pessoa, Historico, Conta

class AdminPessoa(ModelAdmin):
    list_display = ('nome','telefone','cpf',)
    
class AdminHistorico(ModelAdmin):
    list_display = ('descricao',)
    
class AdminConta(ModelAdmin):
    list_display = ('data_vencimento','valor','status','operacao','historico','pessoa',)
    search_fields = ('descricao',)
    list_filter = ('data_vencimento','status','operacao','historico','pessoa',)
    
admin.site.register(Pessoa, AdminPessoa)
admin.site.register(Historico, AdminHistorico)
admin.site.register(Conta, AdminConta)
