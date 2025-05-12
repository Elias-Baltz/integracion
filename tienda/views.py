from django.shortcuts import render, redirect
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.webpay.webpay_plus.transaction import WebpayOptions
from transbank.common.integration_type import IntegrationType
import uuid
from .models import Producto

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
    productos = Producto.objects.all()
    return render(request, 'comprar.html', {'productos': productos})

def iniciar_pago(request):
    buy_order = str(uuid.uuid4()).replace("-", "")[:26]
    session_id = "session123"
    amount = 10000
    return_url = request.build_absolute_uri("/respuesta/")

    # Aquí está el uso correcto de create
    response = transaction.create(buy_order, session_id, amount, return_url)
    return redirect(response['url'] + "?token_ws=" + response['token'])

def respuesta_pago(request):
    token = request.GET.get("token_ws")
    response = transaction.commit(token)
    return render(request, "resultado.html", {"response": response})