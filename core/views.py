from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .models import *
from datetime import date

class ProdutosView(TemplateView):
    template_name = 'produtos.html'

    def get(self, request):
        produtos = Produto.objects.all()
        carrinho = Carrinho.objects.all()  # Recupera os itens do carrinho
        venda = Venda.objects.all()

        return render(request, self.template_name, {'produtos': produtos, 'carrinho': carrinho, 'vendas':venda})

    def post(self, request):
        produto_id = request.POST.get('produto_id')
        produto = Produto.objects.get(id=produto_id)

        # Adiciona o produto ao carrinho
        item_carrinho, created = Carrinho.objects.get_or_create(produto=produto)
        if not created:
            item_carrinho.qtd += 1
            item_carrinho.save()

        return redirect('produtos')  # Redireciona de volta para a lista de produtos


class FinalizarVendaView(TemplateView):
    template_name = 'finalizar_venda.html'

    def post(self, request):
        # Cria uma nova venda única
        nova_venda = Venda.objects.create()

        # Obtém todos os itens do carrinho
        carrinho = Carrinho.objects.all()
        # Associa todos os itens do carrinho à nova venda
        for item in carrinho:
            VendaDoProduto.objects.create(
                venda=nova_venda,  # Associa os produtos à venda criada
                produto=item.produto,
                qtd=item.qtd,
                total=item.produto.valor.valor * item.qtd
            )

        # Limpa o carrinho após a venda
        carrinho.delete()

        # Redireciona para a página de detalhes da venda ou de produtos
        return redirect('venda_detalhes', pk=nova_venda.numero_venda)
    

from django.views.generic import DetailView
from .models import Venda

class VendaDetailView(DetailView):
    model = Venda
    template_name = 'venda_detalhes.html'
    context_object_name = 'venda'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calcula o total da venda somando o total de todos os itens
        total_venda = sum(item.total for item in self.object.itens.all())
        context['total_venda'] = total_venda
        return context