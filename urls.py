from django.conf.urls.defaults import *
from models import ContaPagar, ContaReceber

urlpatterns = patterns('contas.views',
    url('^$', 'contas', name='contas'),
    url('^pagar/(?P<conta_id>\d+)/$', 'conta', {'classe': ContaPagar},
        name='conta_a_pagar'),
    url('^receber/(?P<conta_id>\d+)/$', 'conta', {'classe': ContaReceber},
        name='conta_a_receber'),
    url('^pagar/(?P<conta_id>\d+)/pagar/$', 'conta_pagamento',
        {'classe': ContaPagar},
        name='conta_a_pagar_pagamento'),
    url('^receber/(?P<conta_id>\d+)/pagar/$', 'conta_pagamento',
        {'classe': ContaReceber},
        name='conta_a_receber_pagamento'),
)