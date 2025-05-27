from fastapi import FastAPI
from pydantic import BaseModel, Field
import asyncio
import time

app = FastAPI()

class Score(BaseModel):
    score: int
    identifier: str = Field(..., description="Unique identifier for the user")
    ingress: str = Field(..., description="Ingress money")
    egress: str = Field(..., description="Egress money")


@app.get("/health")
def health():
    return {"message": "app is online"}

@app.post("/evaluate_score")
async def create_order(score_card: Score):
    """ Recepcion de ordenes de compra y venta.
    Este endpoint recibe una orden de compra o venta, valida el tipo de orden y la envia al broker Kafka. Se simula un tiempo de 30 ms para operaciones bloqueantes y 170 ms para operaciones asincronas.

    Args:
        order (Order): Orden de compra o venta

    Returns:
        dict: Mensaje de confirmacion de recepcion
    """
    # Validacion de tipo de orden
    print(f"Validating order: {score_card}")
    time.sleep(0.05)
    
    # Envio al broker kafka
    print(f"Sending order to Kafka: {score_card}")
    await asyncio.sleep(0.13)
    
    
    return {"message": "Order sent to Kafka", "order": score_card}
