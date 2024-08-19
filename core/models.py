from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import date



class NovaCategoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.nome}'

class NovoValor(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'R${self.valor}'

class Tipo_venda(models.Model):
    tipo = models.CharField(max_length=100,null=True, blank=True)
    def __str__(self):
        return self.tipo
    

class Produto(models.Model):
    nome_produto = models.CharField(max_length=100, blank=True, null=True)  # Nome do produto
    tipo_categoria = models.ForeignKey(NovaCategoria, on_delete=models.CASCADE)  # Categoria do produto
    valor = models.ForeignKey(NovoValor, on_delete=models.CASCADE)  # Valor do produto

    def __str__(self):
        return f"{self.nome_produto} - {self.tipo_categoria.nome} - R${self.valor.valor}"

class Carrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)  # Produto adicionado ao carrinho
    qtd = models.IntegerField(default=1)  # Quantidade do produto no carrinho

    def __str__(self):
        return f"{self.produto.nome_produto} - {self.qtd} unidades"

from datetime import date

class Venda(models.Model):
    numero_venda = models.AutoField(primary_key=True)  # Número da venda (identificador único)
    data_venda = models.DateField(default=date.today)  # Data da venda
    tipo_venda = models.ForeignKey(Tipo_venda, on_delete=models.SET_NULL, null=True, blank=True)  # Tipo de venda

    def __str__(self):
        return f"Venda #{self.numero_venda} - {self.data_venda} - Tipo: {self.tipo_venda.tipo}"
class VendaDoProduto(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')  # Associação com a venda
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)  # Produto vendido
    qtd = models.IntegerField(blank=True, null=True)  # Quantidade vendida
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Total calculado

    def __str__(self):
        return f"{self.produto.nome_produto} - {self.qtd} unidades - Total: R${self.total}"
# Função que será chamada antes de salvar uma instância de VendaDoProduto
@receiver(pre_save, sender=VendaDoProduto)
def update_total(sender, instance, **kwargs):
    # Verifica se o produto e a quantidade não são nulos e calcula o total
    if instance.produto.valor and instance.qtd:
        instance.total = instance.produto.valor.valor * instance.qtd
    else:
        instance.total = 0  # Define total como 0 se valor ou qtd forem nulos

class EntregaBairro(models.Model):
    bairro = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.bairro} {self.valor}'
class Entregador(models.Model):
    nome = models.CharField(max_length=100,null=True, blank=True)
    telefone = models.IntegerField(blank=True, null=True)
    veiculo = models.CharField(max_length=100,null=True, blank=True)
    placa = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.telefone} {self.veiculo} -  {self.placa}"

class Atendente(models.Model):
    nome = models.CharField(max_length=100,null=True, blank=True)
    def __str__(self):
        return f"{self.nome}"


class DadosEntrega(models.Model):
    entregador = models.ForeignKey(Atendente, on_delete=models.CASCADE)
    bairroPadrao = models.ForeignKey(EntregaBairro, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100,blank=True, null=True)
    telefone = models.IntegerField(blank=True, null=True)
    endereco = models.CharField(max_length=100,blank=True, null=True)
    pontoReferencia = models.CharField(max_length=100,blank=True, null=True)
    def __str__(self):
        return f"{self.entregador} {self.bairroPadrao} {self.nome} "

class DadosRetirada(models.Model):
    nome = models.CharField(max_length=100,blank=True, null=True)
    telefone = models.IntegerField(blank=True, null=True)
    def __str__(self):
            return f"{self.nome} {self.telefone}"
class DadosVendaLocal(models.Model):
    vendedor = models.ForeignKey(NovoValor, on_delete=models.CASCADE)
    nomeClienteMesa = models.CharField(max_length=100,blank=True, null=True)
    def __str__(self):
        return f"{self.vendedor} {self.nomeClienteMesa}"