import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sucursales.settings")

django.setup()

import grpc
from concurrent import futures
import producto_pb2
import producto_pb2_grpc
from tienda.models import Producto, Sucursal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sucursales.settings")

django.setup()


class ProductoServiceServicer(producto_pb2_grpc.ProductoServiceServicer):
    def AgregarProducto(self, request, context):
        try:
            sucursal = Sucursal.objects.get(id=request.sucursal_id)
            Producto.objects.create(
                sucursal=sucursal,
                nombre=request.nombre,
                descripcion=request.descripcion,
                precio=request.precio,
                stock=request.stock,
            )
            return producto_pb2.ProductoResponse(
                exito=True, mensaje="Producto creado exitosamente"
            )
        except Exception as e:
            return producto_pb2.ProductoResponse(
                exito=False, mensaje=str(e)
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    producto_pb2_grpc.add_ProductoServiceServicer_to_server(
        ProductoServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC en puerto 50051...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
