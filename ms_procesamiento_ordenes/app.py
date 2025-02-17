from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
# from kafka import KafkaProducer
import json

app = FastAPI()

class Order(BaseModel):
    order_type: str = Field(..., pattern="^(venta|compra)$")  # "venta" o "compra"
    asset_type: str
    amount_in_usd: float = Field(..., gt=0)

# producer = KafkaProducer(
#     bootstrap_servers='localhost:9092',
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

@app.get("/health")
def health():
    return {"message": "app is online"}

@app.post("/order")
def create_order(order: Order):
    if order.order_type not in ["venta", "compra"]:
        raise HTTPException(status_code=400, detail="Invalid order type")
    if order.amount_in_usd <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")

    topic = 'orders_purchase' if order.order_type == 'compra' else 'orders_selling'
    print(f"Order sent to topic {topic}: {order}")
    
    # producer.send(topic, order.dict())
    # producer.flush()
    return {"message": "Order sent to Kafka", "order": order.dict()}
