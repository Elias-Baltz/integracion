from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('comprar/', views.comprar, name="comprar"),
    path('iniciar/', views.iniciar_pago, name="iniciar_pago"),
    path('respuesta/', views.respuesta_pago, name="respuesta_pago"),
    path('api/productos/sucursal/<int:sucursal_id>/', views.productos_por_sucursal, name='api_productos_por_sucursal'),
    path('api/sucursales/', views.sucursales_api, name='api_sucursales'),

    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/limpiar/', views.limpiar_carrito, name='limpiar_carrito'),

     path('agregar-producto/', views.agregar_producto, name='agregar_producto'),

     #SSE
     path('stream/', views.sse_stream, name='sse_stream'),

]
