from django.urls import path
from .views import ProdutosView, FinalizarVendaView, VendaDetailView

urlpatterns = [
    path('', ProdutosView.as_view(), name='produtos'),
    path('finalizar_venda/', FinalizarVendaView.as_view(), name='finalizar_venda'),
    path('venda/<int:pk>/', VendaDetailView.as_view(), name='venda_detalhes'),
]
