from decimal import Decimal
from django.conf import settings
from .models import Producto
import copy  # <--- IMPORTANTE: Necesario para solucionar el error

class Carrito:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, producto, cantidad=1):
        product_id = str(producto.id)
        if product_id not in self.cart:
            # Guardamos el precio como STRING para que JSON no falle
            self.cart[product_id] = {'cantidad': 0, 'precio': str(producto.precio)}
        
        self.cart[product_id]['cantidad'] += cantidad
        self.save()

    def update(self, producto, cantidad):
        product_id = str(producto.id)
        if product_id in self.cart:
            self.cart[product_id]['cantidad'] = cantidad
            self.save()

    def remove(self, producto):
        product_id = str(producto.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        productos = Producto.objects.filter(id__in=product_ids)
        
        # --- CORRECCIÓN DEL ERROR ---
        # Usamos deepcopy para trabajar con una copia totalmente independiente
        # y no contaminar la sesión con objetos Decimal o Producto.
        cart = copy.deepcopy(self.cart)

        for producto in productos:
            cart[str(producto.id)]['producto'] = producto

        for item in cart.values():
            # Aquí convertimos a Decimal solo para la visualización/cálculo en este momento
            # Como es una deepcopy, no afecta a self.session['cart']
            item['precio'] = Decimal(item['precio'])
            item['total_precio'] = item['precio'] * item['cantidad']
            yield item

    def get_total_price(self):
        # Convertimos a Decimal al vuelo para calcular, sin guardar
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.cart.values())

    def get_tax(self):
        return self.get_total_price() * Decimal('0.16')
    
    def get_total_with_tax(self):
        return self.get_total_price() + self.get_tax()

    def clear(self):
        del self.session['cart']
        self.save()