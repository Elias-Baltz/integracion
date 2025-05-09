from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('comprar/', views.comprar, name="comprar"),
    path('iniciar/', views.iniciar_pago, name="iniciar_pago"),
    path('respuesta/', views.respuesta_pago, name="respuesta_pago"),
]
