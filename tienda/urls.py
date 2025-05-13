from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('comprar/', views.comprar, name="comprar"),
    path('iniciar/', views.iniciar_pago, name="iniciar_pago"),
    path('respuesta/', views.respuesta_pago, name="respuesta_pago"),
    path('api/productos/sucursal/<int:sucursal_id>/', views.productos_por_sucursal, name='api_productos_por_sucursal'),
    path('api/sucursales/', views.sucursales_api, name='api_sucursales'),

]
