from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    # --- Tienda Pública ---
    path('', views.TiendaView.as_view(), name='tienda-home'),
    path('p/<int:pk>/', views.ProductoPublicDetailView.as_view(), name='producto-public-detail'),
    
    # Categorías (Templates distintos)
    path('cat/altavoces/', views.AltavocesView.as_view(), name='cat-altavoces'),
    path('cat/amplificadores/', views.AmplificadoresView.as_view(), name='cat-amplificadores'),
    path('cat/cine/', views.CineView.as_view(), name='cat-cine'),
    path('cat/portatiles/', views.PortatilesView.as_view(), name='cat-portatiles'),

    # Carrito
    path('carrito/', views.carrito_detail, name='carrito-detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    
    # Checkout
    path('checkout/', views.checkout, name='checkout'),

    # Auth
    path('registro/', views.register_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # --- Admin (Mantén tus rutas anteriores para gestionar) ---
    path('admin-panel/productos/', views.ProductoListView.as_view(), name='producto-list'),
    path('admin-panel/productos/create/', views.ProductoCreateView.as_view(), name='producto-create'),
    # ... resto de rutas admin con prefijo admin-panel/ ...

    # Usuario URLs
    path('usuarios/', views.UsuarioListView.as_view(), name='usuario-list'),
    path('usuarios/<int:pk>/', views.UsuarioDetailView.as_view(), name='usuario-detail'),
    path('usuarios/create/', views.UsuarioCreateView.as_view(), name='usuario-create'),
    path('usuarios/<int:pk>/update/', views.UsuarioUpdateView.as_view(), name='usuario-update'),
    path('usuarios/<int:pk>/delete/', views.UsuarioDeleteView.as_view(), name='usuario-delete'),

    # Producto URLs
    path('productos/', views.ProductoListView.as_view(), name='producto-list'),
    path('productos/<int:pk>/', views.ProductoDetailView.as_view(), name='producto-detail'),
    path('productos/create/', views.ProductoCreateView.as_view(), name='producto-create'),
    path('productos/<int:pk>/update/', views.ProductoUpdateView.as_view(), name='producto-update'),
    path('productos/<int:pk>/delete/', views.ProductoDeleteView.as_view(), name='producto-delete'),

    # Pedido URLs
    path('pedidos/', views.PedidoListView.as_view(), name='pedido-list'),
    path('pedidos/<int:pk>/', views.PedidoDetailView.as_view(), name='pedido-detail'),
    path('pedidos/create/', views.PedidoCreateView.as_view(), name='pedido-create'),
    path('pedidos/<int:pk>/update/', views.PedidoUpdateView.as_view(), name='pedido-update'),
    path('pedidos/<int:pk>/delete/', views.PedidoDeleteView.as_view(), name='pedido-delete'),

    # PedidoDetalle URLs
    path('pedido-detalles/', views.PedidoDetalleListView.as_view(), name='pedidodetalle-list'),
    path('pedido-detalles/<int:pk>/', views.PedidoDetalleDetailView.as_view(), name='pedidodetalle-detail'),
    path('pedido-detalles/create/', views.PedidoDetalleCreateView.as_view(), name='pedidodetalle-create'),
    path('pedido-detalles/<int:pk>/update/', views.PedidoDetalleUpdateView.as_view(), name='pedidodetalle-update'),
    path('pedido-detalles/<int:pk>/delete/', views.PedidoDetalleDeleteView.as_view(), name='pedidodetalle-delete'),

    # Productos URL
    path('productos-altavoces/', views.ProductosView.as_view(), name='productos'),
]
