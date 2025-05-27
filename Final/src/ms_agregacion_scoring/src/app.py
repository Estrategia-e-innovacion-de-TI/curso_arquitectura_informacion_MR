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
async def evaluate_score(score_card: Score):
    """ Recepcion de score crediticio
    
    Args:
        score_card (Score): Datos del score crediticio
    Returns:
        dict: Mensaje de confirmacion y datos del score
    """
    # Validacion de tipo de orden
    print(f"Validating order: {score_card}")
    time.sleep(0.05)
    
    # Envio al broker kafka
    print(f"Sending order to Kafka: {score_card}")
    await asyncio.sleep(0.13)
    
    
    return {"message": "Order sent to Kafka", "order": score_card}
