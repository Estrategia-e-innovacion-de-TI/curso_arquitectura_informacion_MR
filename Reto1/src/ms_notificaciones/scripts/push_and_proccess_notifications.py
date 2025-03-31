from multiprocessing import Process, Manager
import numpy as np
import boto3
import threading
import time
import csv
from datetime import datetime
import uuid

# Configuración de la cola SQS
sqs = boto3.client('sqs', region_name='us-east-1')
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/538430999815/reto1-arquitectura.fifo"

def enviar_mensajes_sqs(num_mensajes):
    for _ in range(num_mensajes):
        mensaje_id = str(uuid.uuid4())
        sqs.send_message(
            QueueUrl=QUEUE_URL, 
            MessageBody=mensaje_id,
            MessageGroupId="default"  # Necesario para colas FIFO
        )
    print(f"Se enviaron {num_mensajes} mensajes a la cola SQS.")


# Función que procesa un mensaje
def procesar_mensaje(mensaje):
    try:
        inicio = start_time
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Hilo {threading.current_thread().name} procesando {mensaje}")
        processing_time = np.random.uniform(0.05, 0.1)  # Simula 50-100 ms de procesamiento
        time.sleep(processing_time)  # Simula latencia del procesamiento
        fin = time.time()
        latencia = (fin - inicio) * 1000  # Convertir a ms
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {mensaje} procesado en {latencia:.2f} ms")
        return latencia
    except Exception as e:
        print(f"⚠️ Error en hilo {threading.current_thread().name}: {e}")
        return None

# Función para procesar mensajes con múltiples hilos
def procesar_con_hilos(num_hilos, num_mensajes):
    mensajes = [str(uuid.uuid4()) for _ in range(num_mensajes)]
    hilos = []
    latencias = []

    for mensaje in mensajes:
        if num_hilos > 1:
            hilo = threading.Thread(target=lambda: latencias.append(procesar_mensaje(mensaje)))
            hilo.start()
            hilos.append(hilo)
        else:
            latencias.append(procesar_mensaje(mensaje))

    for hilo in hilos:
        hilo.join()

    return latencias

# Función principal
def main():
    global start_time, num_hilos
    hilos_input = input("Ingrese los valores de hilos separados por comas (ej: 1,5,10,16,32,64): ")
    num_mensajes = int(input("Ingrese el número total de notificaciones a enviar: "))
    num_iteraciones = int(input("Ingrese el número de iteraciones del experimento: "))

    valores_hilos = [int(x.strip()) for x in hilos_input.split(",")]

    resultados = []

    for iteracion in range(1, num_iteraciones + 1):
        for num_hilos in valores_hilos:
            print(f"Iniciando iteración {iteracion}/{num_iteraciones} con {num_hilos} hilos...")
            enviar_mensajes_sqs(num_mensajes)
            start_time = time.time()
            latencias = procesar_con_hilos(num_hilos, num_mensajes)

            for latencia in latencias:
                if latencia is not None:
                    resultados.append([iteracion, num_hilos, latencia])

    # Guardar resultados en CSV
    with open('latencias_sqs.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["iteracion", "num_hilos", "latencia"])
        writer.writerows(resultados)

    print(f"✅ Resultados guardados en 'latencias_sqs.csv' ({len(resultados)} registros).")

if __name__ == "__main__":
    main()
