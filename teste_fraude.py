
from src.fraud_rules import verificar_fraude

transacao = {
    "transaction_id": "teste-001",
    "customer_id": "cliente_teste",
    "amount": 12609.22,
    "city": "Crato",
    "timestamp": "2026-10-21T16:15:26"
}

resultado = verificar_fraude(transacao)

print("Fraudes identificadas:", resultado)
