# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

class HistoricoManager(models.Model):
    def get_query_set(self):
        query_set = super(HistoricoManager, self).get_query_set()
        
        return query_set.extra(
            select = {
                '_valor_total': """select sum(valor * case operacao when 'c' then 1 else -1 end) 
                                  from contas_conta
                                  where contas_conta.historico_id = contas_historico.id""",
                }
            )

class Historico(models.Model):
    class Meta:
        ordering = ('descricao',)
        
    descricao = models.CharField(max_length=50)
    objects = HistoricoManager()
    
    def valor_total(self):
        return self.v_valor_total or 0.0
        
    def __unicode__(self):
        return self.descricao
    
class PessoaManager(models.Manager):
    def get_query_set(self):
        query_set = super(PessoaManager, self).get_query_set()
        
        return query_set.extra(
            select = {
                '_valor_total': """select sum(valor * case operacao when 'c' then 1 else -1 end) 
                                    from contas_conta
                                    where contas_conta.pessoa_id = contas_pessoa.id""",
                '_quantidade_contas': """select count(valor) from contas_conta
                                        where contas_conta.pessoa_id = contas_pessoa.id""",
                }
            )
        
class Pessoa(models.Model):
    class Meta:
        ordering = ('nome',)
        
    nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=25, blank=True)
    cpf = models.CharField(max_length=11, blank=False)
    objects = PessoaManager()
    
    def valor_total(self):
        return self._valor_total or 0.0
    
    def quantidade_contas(self):
        return self._quantidade_contas or 0 
    
    def __unicode__(self):
        return self.nome
    
CONTA_OPERACAO_DEBITO = 'd'
CONTA_OPERACAO_CREDITO = 'c'
CONTA_OPERACAO_CHOICES = (
    (CONTA_OPERACAO_DEBITO, _('Debito')),
    (CONTA_OPERACAO_CREDITO, _('Credito')),
)

CONTA_STATUS_APAGAR = 'a'
CONTA_STATUS_PAGO = 'p'
CONTA_STATUS_CHOICES = (
    (CONTA_STATUS_APAGAR, _('A Pagar')),
    (CONTA_STATUS_PAGO, _('Pago')),
)

class Conta(models.Model):
    class Meta:
        ordering = ('data_vencimento', 'valor')

    pessoa = models.ForeignKey('Pessoa')
    historico = models.ForeignKey('Historico')
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    operacao = models.CharField(
        max_length=1,
        default=CONTA_OPERACAO_DEBITO,
        choices=CONTA_OPERACAO_CHOICES,
        blank=True,
        )
    status = models.CharField(
        max_length=1,
        default=CONTA_STATUS_APAGAR,
        choices=CONTA_STATUS_CHOICES,
        blank=True,
        )
    descricao = models.TextField(blank=True)
    
    def __unicode__(self):
        data_vencto = self.data_vencimento.strftime('%d/%m/%Y')
        valor = '%0.02f'%self.valor
        return '%s - %s (%s)'%(valor, self.pessoa.nome, data_vencto)
    
class ContaPagar(Conta):
    class Meta:
        ordering = ('data_vencimento', 'valor')
        verbose_name = _('Conta Pagar')
        verbose_name_plural = _('Contas a pagar')
        
    def save(self, *args, **kwargs):
        self.operacao = CONTA_OPERACAO_DEBITO
        super(ContaPagar, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('conta_a_pagar', kwargs={'conta_id': self.id})
    
    def pagamentos(self):
        return self.pagamentopago_set.all()
    
    def lancar_pagamento(self, data_pagamento, valor):
        return PagamentoPago.objects.create(
            conta=self,
            data_pagamento=data_pagamento,
            valor=valor,
            )   
        
class ContaReceber(Conta):
    class Meta:
        ordering = ('data_vencimento', 'valor')
        verbose_name = _('Conta Recebers')
        verbose_name_plural = _('Contas a receber')
        
    def save(self, *args, **kwargs):
        self.operacao = CONTA_OPERACAO_CREDITO
        super(ContaReceber, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('conta_a_receber', kwargs={'conta_id': self.id})
    
    def pagamentos(self):
        return self.pagamentorecebido_set.all()
    
    def lancar_pagamento(self, data_pagamento, valor):
        return PagamentoRecebido.objects.create(
            conta=self,
            data_pagamento=data_pagamento,
            valor=valor,
            )
        
class Pagamento(models.Model):
    class Meta:
        abstract = True
        
    data_pagamento = models.DateField()
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    
class PagamentoPago(Pagamento):
    conta = models.ForeignKey('ContaPagar')
    
class PagamentoRecebido(Pagamento):
    conta = models.ForeignKey('ContaReceber')