from fastapi import FastAPI
from pydantic import BaseModel, Field
import asyncio
import time

app = FastAPI()

class Order(BaseModel):
    order_type: str = Field(..., pattern="^(venta|compra)$")  # "venta" o "compra"
    asset_type: str
    amount_in_usd: float = Field(..., gt=0)


@app.get("/health")
def health():
    return {"message": "app is online"}

@app.post("/order")
async def create_order(order: Order):
    """ Recepcion de ordenes de compra y venta.
    Este endpoint recibe una orden de compra o venta, valida el tipo de orden y la envia al broker Kafka. Se simula un tiempo de 30 ms para operaciones bloqueantes y 170 ms para operaciones asincronas.

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
    
    
    return {"message": "Order sent to Kafka", "order": order}
