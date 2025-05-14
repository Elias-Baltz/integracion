import requests
from django.shortcuts import render, redirect, get_object_or_404
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.webpay.webpay_plus.transaction import WebpayOptions
from transbank.common.integration_type import IntegrationType
import uuid
from .models import Producto, Sucursal, ItemCarrito, Carrito

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductoSerializer, SucursalSerializer

from decimal import Decimal

# Configura las opciones del comercio de integración
options = WebpayOptions(
    commerce_code="597055555532",  # Comercio de pruebas oficial
    api_key="579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",  # API Key oficial de pruebas
    integration_type=IntegrationType.TEST
)

# Crea una instancia de Transaction con las opciones configuradas
transaction = Transaction(options)

# Create your views here.
def index(request):
    return render(request, 'base.html')

def comprar(request):
    nombre = request.GET.get('nombre', '')
    sucursal_id = request.GET.get('sucursal', '')

    productos = Producto.objects.all()

    if nombre:
        productos = productos.filter(nombre__icontains=nombre)

    if sucursal_id:
        productos = productos.filter(sucursal_id=sucursal_id)

    sucursales = Sucursal.objects.all()

    return render(request, 'comprar.html', {
        'productos': productos,
        'sucursales': sucursales,
        'nombre': nombre,
        'sucursal_id': sucursal_id
    })

def iniciar_pago(request):
    carrito = obtener_carrito(request)
    total = carrito.total

    if total == 0:
        return redirect('ver_carrito')  

    buy_order = str(uuid.uuid4()).replace("-", "")[:26]
    session_id = "session123"
    amount = int(total)
    return_url = request.build_absolute_uri("/respuesta/")

    # Aquí está el uso correcto de create
    response = transaction.create(buy_order, session_id, amount, return_url)
    return redirect(response['url'] + "?token_ws=" + response['token'])

def respuesta_pago(request):
    token = request.GET.get("token_ws")

    if token:
        carrito = obtener_carrito(request) 
        carrito.items.all().delete()  
        carrito.save()

    response = transaction.commit(token)

    return render(request, "resultado.html", {"response": response})

#Api 
@api_view(['GET', 'POST'])
def productos_por_sucursal(request, sucursal_id):
    if request.method == 'GET':
        productos = Producto.objects.filter(sucursal_id=sucursal_id)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        data = request.data.copy()
        data['sucursal'] = sucursal_id  
        serializer = ProductoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['GET', 'POST'])
def sucursales_api(request):
    if request.method == 'GET':
        sucursales = Sucursal.objects.all()
        serializer = SucursalSerializer(sucursales, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = SucursalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
def obtener_carrito(request):
    carrito_id = request.session.get("carrito_id")
    if carrito_id:
        carrito = Carrito.objects.get(id=carrito_id)
    else:
        carrito = Carrito.objects.create()
        request.session["carrito_id"] = carrito.id
    return carrito

def agregar_al_carrito(request, producto_id):
    carrito = obtener_carrito(request)

    if request.method == "POST":
        if producto_id == 0:
            for key, value in request.POST.items():
                if key.startswith("cantidad_"):
                    try:
                        cantidad = int(value)
                        if cantidad > 0:
                            pid = int(key.replace("cantidad_", ""))
                            producto = Producto.objects.get(id=pid)
                            item, creado = ItemCarrito.objects.get_or_create(
                                carrito=carrito, producto=producto,
                                defaults={"cantidad": cantidad}
                            )
                            if not creado:
                                item.cantidad += cantidad
                                item.save()
                    except (ValueError, Producto.DoesNotExist):
                        continue
        else:
            cantidad = int(request.POST.get("cantidad", 0))
            if cantidad > 0:
                producto = Producto.objects.get(id=producto_id)
                item, creado = ItemCarrito.objects.get_or_create(
                    carrito=carrito, producto=producto,
                    defaults={"cantidad": cantidad}
                )
                if not creado:
                    item.cantidad += cantidad
                    item.save()

    return redirect("ver_carrito")

def ver_carrito(request):
    carrito = obtener_carrito(request)

    try:
        response = requests.get("https://api.exchangerate.host/latest?base=CLP&symbols=USD")
        data = response.json()
        clp_to_usd = Decimal(str(data['rates']['USD']))
    except Exception:
        clp_to_usd = Decimal('0.0011')  

    total_usd = carrito.total * clp_to_usd  

    context = {
        'carrito': carrito,
        'total_usd': total_usd,
        'tipo_cambio': clp_to_usd,
    }

    return render(request, 'carrito.html', context)


def limpiar_carrito(request):
    carrito_id = request.session.get("carrito_id")
    if carrito_id:
        from .models import Carrito
        try:
            carrito = Carrito.objects.get(id=carrito_id)
            carrito.items.all().delete()  
        except Carrito.DoesNotExist:
            pass
    return redirect('ver_carrito')  