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
    
class UpdateOrderRequest(BaseModel):
    id: int
    estado: str = Field(..., pattern="^(creada|en_proceso|entregada|cancelada)$")
    observaciones: str = None


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
    return {"message": "order_service is online"}

@app.get("/order_status/{order_id}")
async def order_status(order_id: str):
    """ Consulta de estado de ordenes de compra y venta.
    Este endpoint consulta el estado de una orden de compra o venta, valida el id de la orden y consulta la base de datos para obtener el estado actual.

    Args:
        order_id (str): Id de la orden

    Returns:
        dict: Mensaje de confirmacion de recepcion
    """
    # Validacion de id de orden
    try:
        # Verificar que el ID es un número
        order_id_int = int(order_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de orden inválido. Debe ser un número entero.")
    
    try:
        # Obtener conexión a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Consultar la orden en la base de datos
        query = "SELECT * FROM orden_servicio WHERE id = %s"
        cursor.execute(query, (order_id_int,))
        
        # Obtener el resultado
        order_info = cursor.fetchone()
        
        # Cerrar cursor y conexión
        cursor.close()
        conn.close()
        
        # Verificar si la orden existe
        if not order_info:
            raise HTTPException(status_code=404, detail=f"No se encontró una orden con el ID: {order_id}")
        # Devolver la información del estado de la orden
        return {
            "order_id": order_id_int,
            "status": order_info["estado"],
            "details": {
                "tipo_productos": order_info["tipo_productos"],
                "cantidad_productos": order_info["cantidad_productos"],
                "direccion_entrega": order_info["direccion_entrega"],
                "usuario_creador": order_info["usuario_creador"],
                "fecha_creacion": order_info["fecha_hora_creacion"].isoformat() if order_info["fecha_hora_creacion"] else None,
                "fecha_entrega": order_info["fecha_entrega"].isoformat() if order_info["fecha_entrega"] else None,
                "observaciones": order_info["observaciones"]
            }
        }  
    except Exception as e:
        # En caso de error, intentar cerrar la conexión
        if 'conn' in locals() and conn:
            conn.close()
        print(f"Error consultando estado de orden: {e}")
        raise HTTPException(status_code=500, detail=f"Error al consultar el estado de la orden: {str(e)}")
    
    

@app.post("/create_order")
async def create_order(order: CreateOrderRequest):
    """ Recepcion de ordenes de compra y venta.
    Este endpoint recibe una orden de compra o venta, valida el tipo de orden y la envia al broker Kafka. Se simula un tiempo de 30 ms para operaciones bloqueantes y 170 ms para operaciones asincronas.

    Args:
        order (Order): Orden de compra o venta

    Returns:
        dict: Mensaje de confirmacion de recepcion
    """
    # Simular fallo aleatorio (5% de probabilidad)
    import random
    if random.random() < 0.02:  # 5% de probabilidad
        print("Fallo aleatorio simulado en create_order")
        raise HTTPException(status_code=500, detail="Error aleatorio simulado en la creación de orden (5% de probabilidad)")

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
async def update_order(update_request: UpdateOrderRequest):
    """ Actualización del estado de una orden de servicio.
    Este endpoint actualiza el estado de una orden existente en la base de datos.

    Args:
        update_request (UpdateOrderRequest): Datos para actualizar la orden

    Returns:
        dict: Mensaje de confirmación de la actualización
    """
    import random
    if random.random() < 0.02:  # 5% de probabilidad
        print("Fallo aleatorio simulado en update_order")
        raise HTTPException(status_code=500, detail="Error aleatorio simulado en la actualizacion de orden (5% de probabilidad)")
    try:
        # Obtener conexión a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si la orden existe
        check_query = "SELECT id FROM orden_servicio WHERE id = %s"
        cursor.execute(check_query, (update_request.id,))
        order = cursor.fetchone()
        
        if not order:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail=f"No se encontró una orden con el ID: {update_request.id}")
        
        # Preparar la consulta SQL para actualizar
        update_query = """
        UPDATE orden_servicio 
        SET estado = %s, 
            observaciones = CASE 
                WHEN %s IS NOT NULL THEN %s 
                ELSE observaciones 
            END
        WHERE id = %s
        RETURNING id, estado;
        """
        
        # Ejecutar la consulta
        cursor.execute(
            update_query,
            (
                update_request.estado,
                update_request.observaciones,
                update_request.observaciones,
                update_request.id
            )
        )
        
        # Obtener el resultado de la actualización
        updated_order = cursor.fetchone()
        
        # Confirmar la transacción
        conn.commit()
        
        # Cerrar cursor y conexión
        cursor.close()
        conn.close()
        
        # Simular un pequeño retraso de procesamiento
        time.sleep(0.05)
        
        return {
            "message": "Estado de la orden actualizado exitosamente",
            "order_id": updated_order["id"],
            "new_status": updated_order["estado"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        # En caso de error, intentar cerrar la conexión
        if 'conn' in locals() and conn:
            conn.close()
        print(f"Error updating order: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar la orden: {str(e)}")



