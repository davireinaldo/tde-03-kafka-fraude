
import json
import random
import time
import uuid
from datetime import datetime

from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda dados: json.dumps(dados).encode("utf-8")
)

cidades = ["Crato", "Juazeiro do Norte", "Barbalha", "Fortaleza"]


def gerar_transacao():
    transacao = {
        "transaction_id": str(uuid.uuid4()),
        "customer_id": f"cliente_{random.randint(1, 10)}",
        "amount": round(random.uniform(50, 15000), 2),
        "city": random.choice(cidades),
        "timestamp": datetime.now().isoformat()
    }

    return transacao


try:
    while True:
        transacao = gerar_transacao()

        producer.send("transacoes", value=transacao)
        producer.flush()

        print("Transação enviada:", transacao)

        time.sleep(3)

except KeyboardInterrupt:
    print("\nProducer encerrado.")

finally:
    producer.close()
    