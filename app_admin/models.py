from django.db import models
from django.contrib.auth.hashers import make_password


from django.db import models
from django.contrib.auth.models import User # Usaremos el usuario nativo de Django para el login

# Mantenemos Producto igual
class Producto(models.Model):
    CATEGORIAS = [
        ("altavoces", "Altavoces"),
        ("amplificadores", "Amplificadores"),
        ("cine", "Cine en Casa"),
        ("portatiles", "Portátiles"),
    ]
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    tipo_conectividad = models.CharField(max_length=100)
    numero = models.IntegerField()
    stock = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return f"{self.marca} {self.modelo}"

# Modificamos Pedido para incluir impuestos y datos de envío directos
class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Usuario registrado (opcional)
    # Datos del cliente para este pedido específico
    nombre_cliente = models.CharField(max_length=100)
    email_cliente = models.EmailField()
    telefono_cliente = models.CharField(max_length=20)
    domicilio = models.CharField(max_length=255)
    
    # Totales
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    impuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    forma_pago = models.CharField(max_length=50) # 'tarjeta' o 'paypal'
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido #{self.id} - {self.nombre_cliente}"

class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.modelo} x{self.cantidad}"

# ----------------------------------------------------
#                    USUARIO
# ----------------------------------------------------

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    domicilio = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)  # Guardar hasheada

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

    def save(self, *args, **kwargs):
        if self.contraseña and not self.contraseña.startswith('$pbkdf2-sha256$'):
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)



# ----------------------------------------------------
#                    PEDIDO
# ----------------------------------------------------


