# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Historico(models.Model):
    class Meta:
        ordering = ('descricao',)
        
    descricao = models.CharField(max_length=50)
        
    def __unicode__(self):
        return self.descricao
        
class Pessoa(models.Model):
    class Meta:
        ordering = ('nome',)
        
    nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=25, blank=True)
    cpf = models.CharField(max_length=11, blank=False)
    
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