from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .models import *
from datetime import date
from django.views.generic import DetailView
from .models import Venda

class ProdutosView(TemplateView):
    template_name = 'produtos.html'

    def get(self, request):
        produtos = Produto.objects.all()
        carrinho = Carrinho.objects.all()
        vendas = Venda.objects.all()
        tipos_venda = Tipo_venda.objects.all()  # Recupera todos os tipos de venda

        return render(request, self.template_name, {
            'produtos': produtos,
            'carrinho': carrinho,
            'vendas': vendas,
            'tipos_venda': tipos_venda  # Passa os tipos de venda para o template
        })

    def post(self, request):
        produto_id = request.POST.get('produto_id')
        produto = Produto.objects.get(id=produto_id)

        # Adiciona o produto ao carrinho
        item_carrinho, created = Carrinho.objects.get_or_create(produto=produto)
        if not created:
            item_carrinho.qtd += 1
            item_carrinho.save()

        return redirect('produtos')
class FinalizarVendaView(TemplateView):
    template_name = 'finalizar_venda.html'

    def post(self, request):
        tipo_venda_id = request.POST.get('tipo_venda')  # Captura o tipo de venda selecionado
        tipo_venda = Tipo_venda.objects.get(id=tipo_venda_id)

        # Cria uma nova venda com o tipo de venda selecionado
        nova_venda = Venda.objects.create(tipo_venda=tipo_venda)

        # Obtém todos os itens do carrinho
        carrinho = Carrinho.objects.all()
        # Associa todos os itens do carrinho à nova venda
        for item in carrinho:
            VendaDoProduto.objects.create(
                venda=nova_venda,
                produto=item.produto,
                qtd=item.qtd,
                total=item.produto.valor.valor * item.qtd
            )

        # Limpa o carrinho após a venda
        carrinho.delete()

        return redirect('venda_detalhes', pk=nova_venda.numero_venda)

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