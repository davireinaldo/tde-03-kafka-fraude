
import json

from kafka import KafkaConsumer
from fraud_rules import verificar_fraude
from database import criar_tabela, salvar_transacao


# Cria a tabela no banco, caso ainda não exista
criar_tabela()


consumer = KafkaConsumer(
    "transacoes",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda dados: json.loads(dados.decode("utf-8"))
)

print("Aguardando transações...\n")

try:
    for mensagem in consumer:
        transacao = mensagem.value

        print("\nTransação recebida:", transacao)

        # Verifica se a transação apresenta fraude
        fraudes = verificar_fraude(transacao)

        if fraudes:
            print("🚨 Fraudes identificadas:", fraudes)
        else:
            print("✅ Nenhuma fraude identificada.")

        # Salva a transação e o resultado da análise no SQLite
        salvar_transacao(transacao, fraudes)

        print("Transação salva no banco de dados.")

except KeyboardInterrupt:
    print("\nConsumer encerrado.")

finally:
    consumer.close()
