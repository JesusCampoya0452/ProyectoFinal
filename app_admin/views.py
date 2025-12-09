from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Usuario, Producto, Pedido, PedidoDetalle
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q

from .models import Producto, Pedido, PedidoDetalle
from .forms import CheckoutForm, RegistroUsuarioForm
from .cart import Carrito

# ==========================================
#              VISTAS PÚBLICAS (USUARIO)
# ==========================================

class TiendaView(ListView):
    model = Producto
    template_name = 'usuario/tienda_home.html'
    context_object_name = 'productos'
    
    def get_queryset(self):
        query = self.request.GET.get('marca')
        if query:
            return Producto.objects.filter(marca__icontains=query)
        return Producto.objects.all()

# Vistas por categoría (Templates separados como pediste)
class AltavocesView(ListView):
    model = Producto
    template_name = 'usuario/cat_altavoces.html'
    context_object_name = 'productos'
    def get_queryset(self):
        return Producto.objects.filter(categoria='altavoces')

class AmplificadoresView(ListView):
    model = Producto
    template_name = 'usuario/cat_amplificadores.html'
    context_object_name = 'productos'
    def get_queryset(self):
        return Producto.objects.filter(categoria='amplificadores')

class CineView(ListView):
    model = Producto
    template_name = 'usuario/cat_cine.html'
    context_object_name = 'productos'
    def get_queryset(self):
        return Producto.objects.filter(categoria='cine')

class PortatilesView(ListView):
    model = Producto
    template_name = 'usuario/cat_portatiles.html'
    context_object_name = 'productos'
    def get_queryset(self):
        return Producto.objects.filter(categoria='portatiles')

class ProductoPublicDetailView(DetailView):
    model = Producto
    template_name = 'usuario/producto_public_detail.html'
    context_object_name = 'producto'

# --- CARRITO ---

def add_to_cart(request, product_id):
    cart = Carrito(request)
    producto = get_object_or_404(Producto, id=product_id)
    cart.add(producto=producto)
    return redirect('carrito-detail')

def remove_from_cart(request, product_id):
    cart = Carrito(request)
    producto = get_object_or_404(Producto, id=product_id)
    cart.remove(producto)
    return redirect('carrito-detail')

def carrito_detail(request):
    cart = Carrito(request)
    # Lógica para actualizar cantidades si es POST
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cantidad = int(request.POST.get('cantidad'))
        if cantidad > 0:
            producto = get_object_or_404(Producto, id=product_id)
            cart.update(producto, cantidad)
    
    return render(request, 'usuario/carrito.html', {'cart': cart})

# --- CHECKOUT Y PAGO ---

def checkout(request):
    cart = Carrito(request)
    if not cart.cart:
        return redirect('tienda-home')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            if request.user.is_authenticated:
                pedido.user = request.user
            
            pedido.subtotal = cart.get_total_price()
            pedido.impuestos = cart.get_tax()
            pedido.total = cart.get_total_with_tax()
            pedido.pagado = True # Simulamos pago exitoso
            pedido.save()

            for item in cart:
                PedidoDetalle.objects.create(
                    pedido=pedido,
                    producto=item['producto'],
                    precio_unitario=item['precio'],
                    cantidad=item['cantidad']
                )
                # Disminuir stock
                prod = item['producto']
                prod.stock -= item['cantidad']
                prod.save()

            cart.clear()
            return render(request, 'usuario/gracias.html', {'pedido': pedido})
    else:
        # Pre-llenar datos si está logueado
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'nombre_cliente': f"{request.user.first_name} {request.user.last_name}",
                'email_cliente': request.user.email
            }
        form = CheckoutForm(initial=initial_data)

    return render(request, 'usuario/checkout.html', {'cart': cart, 'form': form})

# --- AUTH ---

def register_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('tienda-home')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuario/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tienda-home')
    else:
        form = AuthenticationForm()
    return render(request, 'usuario/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('tienda-home')

# MANTENER TUS VISTAS DE ADMIN (ListView, CreateView, etc) ABAJO...
# (Asegúrate de cambiar los nombres de templates de admin si es necesario o déjalos como app_admin/...)

# ----------------------------------------------------
#                    HOME VIEW
# ----------------------------------------------------

class HomeView(TemplateView):
    template_name = 'app_admin/inicio.html'

# ----------------------------------------------------
#                    USUARIO VIEWS
# ----------------------------------------------------

class UsuarioListView(ListView):
    model = Usuario
    template_name = 'app_admin/usuario_list.html'
    context_object_name = 'usuarios'


class UsuarioDetailView(DetailView):
    model = Usuario
    template_name = 'app_admin/usuario_detail.html'
    context_object_name = 'usuario'


class UsuarioCreateView(CreateView):
    model = Usuario
    form_class = RegistroUsuarioForm
    template_name = 'app_admin/usuario_form.html'
    success_url = reverse_lazy('usuario-list')


class UsuarioUpdateView(UpdateView):
    model = Usuario
    template_name = 'app_admin/usuario_form.html'
    fields = ['nombre', 'apellidos', 'telefono', 'domicilio', 'fecha_nacimiento', 'email']
    success_url = reverse_lazy('usuario-list')


class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'app_admin/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario-list')


# ----------------------------------------------------
#                    PRODUCTO VIEWS
# ----------------------------------------------------

class ProductoListView(ListView):
    model = Producto
    template_name = 'app_admin/producto_list.html'
    context_object_name = 'productos'


class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'app_admin/producto_detail.html'
    context_object_name = 'producto'


class ProductoCreateView(CreateView):
    model = Producto
    template_name = 'app_admin/producto_form.html'
    fields = ['categoria', 'marca', 'modelo', 'tipo_conectividad', 'numero', 'stock', 'precio', 'imagen']
    success_url = reverse_lazy('producto-list')


class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'app_admin/producto_form.html'
    fields = ['categoria', 'marca', 'modelo', 'tipo_conectividad', 'numero', 'stock', 'precio', 'imagen']
    success_url = reverse_lazy('producto-list')


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'app_admin/producto_confirm_delete.html'
    success_url = reverse_lazy('producto-list')


class ProductosView(ListView):
    model = Producto
    template_name = 'app_admin/productos.html'
    context_object_name = 'productos'

    def get_queryset(self):
        return Producto.objects.all()


# ----------------------------------------------------
#                    PEDIDO VIEWS
# ----------------------------------------------------

class PedidoListView(ListView):
    model = Pedido
    template_name = 'app_admin/pedido_list.html'
    context_object_name = 'pedidos'


class PedidoDetailView(DetailView):
    model = Pedido
    template_name = 'app_admin/pedido_detail.html'
    context_object_name = 'pedido'


class PedidoCreateView(CreateView):
    model = Pedido
    template_name = 'app_admin/pedido_form.html'
    fields = ['usuario', 'subtotal', 'forma_pago', 'domicilio', 'detalles']
    success_url = reverse_lazy('pedido-list')


class PedidoUpdateView(UpdateView):
    model = Pedido
    template_name = 'app_admin/pedido_form.html'
    fields = ['usuario', 'subtotal', 'forma_pago', 'domicilio', 'detalles']
    success_url = reverse_lazy('pedido-list')


class PedidoDeleteView(DeleteView):
    model = Pedido
    template_name = 'app_admin/pedido_confirm_delete.html'
    success_url = reverse_lazy('pedido-list')


# ----------------------------------------------------
#                PEDIDO DETALLE VIEWS
# ----------------------------------------------------

class PedidoDetalleListView(ListView):
    model = PedidoDetalle
    template_name = 'app_admin/pedidodetalle_list.html'
    context_object_name = 'pedidodetalles'


class PedidoDetalleDetailView(DetailView):
    model = PedidoDetalle
    template_name = 'app_admin/pedidodetalle_detail.html'
    context_object_name = 'pedidodetalle'


class PedidoDetalleCreateView(CreateView):
    model = PedidoDetalle
    template_name = 'app_admin/pedidodetalle_form.html'
    fields = ['pedido', 'producto', 'cantidad', 'precio_unitario']
    success_url = reverse_lazy('pedidodetalle-list')


class PedidoDetalleUpdateView(UpdateView):
    model = PedidoDetalle
    template_name = 'app_admin/pedidodetalle_form.html'
    fields = ['pedido', 'producto', 'cantidad', 'precio_unitario']
    success_url = reverse_lazy('pedidodetalle-list')


class PedidoDetalleDeleteView(DeleteView):
    model = PedidoDetalle
    template_name = 'app_admin/pedidodetalle_confirm_delete.html'
    success_url = reverse_lazy('pedidodetalle-list')
