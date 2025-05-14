from django.db import models

# Create your models here.
class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    es_casa_matriz = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre} ({self.sucursal.nombre})"
    
class Carrito(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.total() for item in self.items.all())
    
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def total(self):
        return self.cantidad * self.producto.precio
    