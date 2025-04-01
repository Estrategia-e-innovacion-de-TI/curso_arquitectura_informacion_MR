from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
import time
import random
import requests
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="Monitoring System API",
    description="API para el sistema de monitoreo de microservicios",
    version="1.0.0"
)

# Modelos de datos
class ServiceHealth(BaseModel):
    service_id: str
    status: str
    response_time_ms: float
    cpu_usage: float
    memory_usage: float
    timestamp: datetime

class Alert(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    service_id: str
    alert_type: str
    severity: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
    resolved: bool = False
    resolved_at: Optional[datetime] = None

# Almacenamiento en memoria (reemplazar con base de datos en producción)
service_health_data: Dict[str, List[ServiceHealth]] = {}
alerts: List[Alert] = []

# Configuraciones para servicios monitoreados
SERVICE_CONFIG = {
    "ms-order-service": {
        "base_url": "http://localhost:8000",  # Ajusta según tu configuración
        "endpoints": {
            "health": "/health",
            "create_order": "/create_order",
            "order_status": "/order_status/{order_id}",
            "update_order": "/update_order"
        }
    }
}

# Endpoint para verificar la salud de la API
@app.get("/health")
def health_check():
    """Verifica el estado de salud del sistema de monitoreo"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/monitor/ms-order-service")
async def monitor_order_service():
    """
    Monitorea el estado de salud del microservicio ms_order_service 
    realizando un flujo completo de prueba (crear orden → validar → actualizar → validar)
    
    Returns:
        Dict: Resultados del monitoreo y métricas de rendimiento
    """
    
    service = "ms-order-service"
    base_url = SERVICE_CONFIG[service]["base_url"]
    endpoints = SERVICE_CONFIG[service]["endpoints"]
    start_time = time.time()
    
    try:
        # Paso 1: Verificar el endpoint health
        logger.info(f"Verificando health endpoint de {service}")
        health_response = requests.get(
            f"{base_url}{endpoints['health']}",
            timeout=5
        )
        
        if health_response.status_code != 200:
            raise Exception(f"Health endpoint returned {health_response.status_code}")
            
        # Paso 2: Crear una orden ficticia
        logger.info(f"Creando orden de prueba en {service}")
        orden_prueba = {
            "tipo_productos": "Test_Monitor",
            "cantidad_productos": 1,
            "direccion_entrega": "Dirección de prueba monitor",
            "usuario_creador": "sistema_monitoreo",
            "fecha_entrega": (datetime.now() + timedelta(days=1)).isoformat(),
            "observaciones": "Orden creada por sistema de monitoreo"
        }
        
        create_response = requests.post(
            f"{base_url}{endpoints['create_order']}",
            json=orden_prueba,
            timeout=5
        )
        
        if create_response.status_code != 200:
            raise Exception(f"Create order endpoint returned {create_response.status_code}")
        
        # Extraer el ID de la orden creada
        created_order = create_response.json()
        order_id = created_order.get("order_id")
        
        if not order_id:
            raise Exception("No se pudo obtener el ID de la orden creada")
        
        # Paso 3: Validar que la orden fue creada consultando su estado
        logger.info(f"Consultando estado de orden {order_id}")
        url = f"{base_url}{endpoints['order_status']}".replace("{order_id}",str(order_id))
        status_response = requests.get(
            url,
            timeout=5
        )
        
        if status_response.status_code != 200:
            raise Exception(f"Order status endpoint returned {status_response.status_code}")
            
        order_status = status_response.json()
        if order_status["status"] != "creada":
            raise Exception(f"Estado de orden incorrecto: {order_status['status']}")
        
        # Paso 4: Actualizar la orden
        logger.info(f"Actualizando estado de orden {order_id}")
        update_data = {
            "id": order_id,
            "estado": "en_proceso",
            "observaciones": "Actualizada por el sistema de monitoreo"
        }
        
        update_response = requests.post(
            f"{base_url}{endpoints['update_order']}",
            json=update_data,
            timeout=5
        )
        
        if update_response.status_code != 200:
            raise Exception(f"Update order endpoint returned {update_response.status_code}")
        
        # Paso 5: Validar la actualización
        logger.info(f"Verificando actualización de orden {order_id}")
        url = f"{base_url}{endpoints['order_status']}".replace("{order_id}",str(order_id))
        status_response_2 = requests.get(
            url,
            timeout=5
        )
        
        if status_response_2.status_code != 200:
            raise Exception(f"Second order status check returned {status_response_2.status_code}")
        
        updated_status = status_response_2.json()
        if updated_status["status"] != "en_proceso":
            raise Exception(f"Estado actualizado incorrecto: {updated_status['status']}")
        
        # Calcular tiempo total y métricas
        end_time = time.time()
        total_time = (end_time - start_time) * 1000  # Convertir a ms
        
        # Registrar las métricas de salud
        health_data = ServiceHealth(
            service_id=service,
            status="healthy",
            response_time_ms=total_time,
            cpu_usage=random.uniform(20, 50),  # Simulado - idealmente obtener datos reales
            memory_usage=random.uniform(30, 70),  # Simulado - idealmente obtener datos reales
            timestamp=datetime.now()
        )
        
        # Almacenar las métricas
        if service not in service_health_data:
            service_health_data[service] = []
        
        service_health_data[service].append(health_data)
        
        # Limitar el historial
        if len(service_health_data[service]) > 100:
            service_health_data[service] = service_health_data[service][-100:]
        
        return {
            "service": service,
            "status": "healthy",
            "message": "Flujo completo exitoso",
            "metrics": {
                "total_time_ms": total_time,
                "created_order_id": order_id,
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        # Capturar cualquier error durante el monitoreo
        end_time = time.time()
        total_time = (end_time - start_time) * 1000
        
        # Registrar el servicio como degradado
        health_data = ServiceHealth(
            service_id=service,
            status="degraded",
            response_time_ms=total_time,
            cpu_usage=0.0,  # No disponible durante error
            memory_usage=0.0,  # No disponible durante error
            timestamp=datetime.now()
        )
        
        if service not in service_health_data:
            service_health_data[service] = []
            
        service_health_data[service].append(health_data)
        
        # Crear una alerta
        new_alert = Alert(
            service_id=service,
            alert_type="service_test_failure",
            severity="critical",
            message=f"Fallo en prueba de flujo completo: {str(e)}",
        )
        alerts.append(new_alert)
        
        logger.error(f"Error monitoring {service}: {e}")
        
        return {
            "service": service,
            "status": "degraded",
            "message": f"Error en monitoreo: {str(e)}",
            "metrics": {
                "total_time_ms": total_time,
                "alert_id": new_alert.id,
                "timestamp": datetime.now().isoformat()
            }
        }

