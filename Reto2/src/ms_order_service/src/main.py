from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import asyncio
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

app = FastAPI()

class Order(BaseModel):
    order_type: str = Field(..., pattern="^(venta|compra)$")  # "venta" o "compra"
    asset_type: str
    amount_in_usd: float = Field(..., gt=0)
    
class CreateOrderRequest(BaseModel):
    tipo_productos: str
    cantidad_productos: int
    direccion_entrega: str
    usuario_creador: str
    fecha_entrega: str
    observaciones: str


# Database connection function
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")


@app.get("/health")
def health():
    return {"message": "app is online"}

@app.get("/order_status/{order_id}")
async def order_status(order_id: str):
    """ Consulta de estado de ordenes de compra y venta.
    Este endpoint consulta el estado de una orden de compra o venta, valida el id de la orden y simula un tiempo de 30 ms para operaciones bloqueantes y 170 ms para operaciones asincronas.

    Args:
        order_id (str): Id de la orden

    Returns:
        dict: Mensaje de confirmacion de recepcion
    """
    # Validacion de id de orden
    print(f"Validating order ID: {order_id}")
    time.sleep(0.05)
    
    # Simulacion de consulta al broker kafka
    print(f"Fetching order status from Kafka for ID: {order_id}")
    await asyncio.sleep(0.13)
    
    return {"message": "Order status fetched", "order_id": order_id}

@app.post("/create_order")
async def create_order(order: CreateOrderRequest):
    """ Recepcion de ordenes de compra y venta.
    Este endpoint recibe una orden de compra o venta, valida el tipo de orden y la envia al broker Kafka. Se simula un tiempo de 30 ms para operaciones bloqueantes y 170 ms para operaciones asincronas.

    Args:
        order (Order): Orden de compra o venta

    Returns:
        dict: Mensaje de confirmacion de recepcion
    """
    try:
        # Obtener conexión a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Preparar la consulta SQL
        insert_query = """
        INSERT INTO orden_servicio 
        (tipo_productos, cantidad_productos, direccion_entrega, usuario_creador, estado, fecha_entrega, observaciones)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        
        # Convertir la fecha de entrega si existe
        fecha_entrega = None
        if order.fecha_entrega:
            try:
                fecha_entrega = datetime.fromisoformat(order.fecha_entrega)
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use formato ISO (YYYY-MM-DD HH:MM:SS)")
        
        # Ejecutar la consulta
        cursor.execute(
            insert_query,
            (
                order.tipo_productos,
                order.cantidad_productos,
                order.direccion_entrega,
                order.usuario_creador,
                "creada",
                fecha_entrega,
                order.observaciones
            )
        )
        
        # Obtener el ID de la orden creada
        order_id = cursor.fetchone()["id"]
        
        # Confirmar la transacción
        conn.commit()
        
        # Cerrar cursor y conexión
        cursor.close()
        conn.close()
        
        # Simular operación asíncrona
        await asyncio.sleep(0.13)
        
        return {
            "message": "Orden de servicio creada exitosamente",
            "order_id": order_id,
            "order_details": order.dict()
        }
        
    except Exception as e:
        # En caso de error, intentar cerrar la conexión
        if 'conn' in locals() and conn:
            conn.close()
        print(f"Error creating order: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear la orden: {str(e)}")



@app.post("/update_order")
async def update_order(order: Order):
    """ Actualizacion de ordenes de compra y venta.
    Este endpoint actualiza una orden de compra o venta, valida el tipo de orden y la envia al broker Kafka. Se simula un tiempo de 30 ms para operaciones bloqueantes y 170 ms para operaciones asincronas.

    Args:
        order (Order): Orden de compra o venta

    Returns:
        dict: Mensaje de confirmacion de recepcion
    """
    # Validacion de tipo de orden
    print(f"Validating order: {order}")
    time.sleep(0.05)
    
    # Envio al broker kafka
    print(f"Sending order to Kafka: {order}")
    await asyncio.sleep(0.13)
    
    
    return {"message": "Order updated in Kafka", "order": order}
