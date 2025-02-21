import boto3
import time
import concurrent.futures
import uuid
import numpy as np
# Configurar cliente de SQS
sqs = boto3.client('sqs', region_name='us-east-1')  # Cambia a tu región
queue_url = "https://sqs.us-east-1.amazonaws.com/538430999815/reto1-arquitectura.fifo"



# Simula 1000 notificaciones por minuto
def send_notifications():
    for i in range(1000):
        message_body = f"Notificación {i+1}"
        message_group_id = "notification_group"
        deduplication_id = str(uuid.uuid4())  # Asegura que no haya duplicados en FIFO

        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            MessageGroupId=message_group_id,
            MessageDeduplicationId=deduplication_id
        )

        if i % 100 == 0:
            print(f"Enviadas {i+1} notificaciones...")
        #lambda_param = 60 / 1000  # 1000 mensajes en 60 segundos (aprox. 1 msg cada 60ms)
        #time.sleep(np.random.exponential(lambda_param))



# Función para procesar una notificación
def process_notification(message):
    start_time = time.time()
    message_body = message['Body']
    
    # Simula tiempo de procesamiento (100-150ms)
    processing_time = round(time.time() * 1000) % 50 + 100
    time.sleep(processing_time / 1000)

    end_time = time.time()
    latency = (end_time - start_time) * 1000  # Convertir a ms

    print(f"✅ Procesado: {message_body} en {latency:.2f} ms")

    # Confirmar eliminación del mensaje de la cola
    receipt_handle = message['ReceiptHandle']
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

    return latency

# 🟢 Modo 1: Procesamiento Secuencial
def sequential_processing():
    total_time = 0
    for _ in range(50):
        send_notifications()
        print("✅ Todos los mensajes fueron enviados a SQS.")

        start_batch = time.time()
        while True:
            response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=1)

            if 'Messages' in response:
                for message in response['Messages']:
                    process_notification(message)
            else:
                break
        total_time += time.time() - start_batch
    return total_time / 50

# 🔵 Modo 2: Procesamiento Concurrente con 10 Threads
def concurrent_processing(num_workers=10):
    total_time = 0
    for _ in range(50):
        send_notifications()
        print("✅ Todos los mensajes fueron enviados a SQS.")
        start_batch = time.time()
        while True:
            response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=1)

            if 'Messages' in response:
                with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                    executor.map(process_notification, response['Messages'])
            else:
                break
        total_time += time.time() - start_batch
    return total_time / 50

# Ejecutar modo secuencial o concurrente
if __name__ == "__main__":
    sequential_avg_time = sequential_processing()
    print(f"🔄 Tiempo promedio de procesamiento secuencial: {sequential_avg_time:.2f}s")
    concurrent_2_avg_time = concurrent_processing(num_workers=2)
    print(f"🚀 Tiempo promedio de procesamiento concurrente: {concurrent_2_avg_time:.2f}s")
    concurrent_avg_time = concurrent_processing(num_workers=10)
    print(f"🚀 Tiempo promedio de procesamiento concurrente: {concurrent_avg_time:.2f}s")

    # Guardar resultados en un archivo
    with open('./resultados_experimento_2.txt', 'w') as file:
        file.write(f"🔄 Tiempo promedio de procesamiento secuencial: {sequential_avg_time:.2f}s\n")
        file.write(f"🚀 Tiempo promedio de procesamiento concurrente (2 workers): {concurrent_avg_time:.2f}s\n")
        file.write(f"🚀 Tiempo promedio de procesamiento concurrente (10 workers): {concurrent_avg_time:.2f}s\n")
