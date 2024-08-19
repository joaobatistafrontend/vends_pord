from django.contrib import admin
from .models import *

admin.site.register(NovaCategoria)
admin.site.register(NovoValor)
admin.site.register(Produto)
admin.site.register(VendaDoProduto)
admin.site.register(Carrinho)
admin.site.register(Venda)


admin.site.register(EntregaBairro)
admin.site.register(Entregador)
admin.site.register(Atendente)
admin.site.register(DadosEntrega)
admin.site.register(DadosRetirada)
admin.site.register(DadosVendaLocal)
admin.site.register(Tipo_venda)