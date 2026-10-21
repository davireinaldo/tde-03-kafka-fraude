
from fraud_rules import verificar_fraude


def testar_caso(descricao, transacoes, resultado_esperado):
    resultados = []

    for transacao in transacoes:
        fraudes = verificar_fraude(transacao)
        resultados.append("GEO_10m" in fraudes)

    passou = resultados == resultado_esperado

    print(f"{'PASSOU' if passou else 'FALHOU'}: {descricao}")
    print(f"  Resultado: {resultados}")
    print(f"  Esperado:  {resultado_esperado}\n")


def transacao(cliente, cidade, horario):
    return {
        "transaction_id": f"{cliente}-{cidade}-{horario}",
        "customer_id": cliente,
        "amount": 100.0,
        "city": cidade,
        "timestamp": horario
    }


# Caso 1: mesmo cliente, cidades diferentes em 5 minutos
testar_caso(
    "Mesmo cliente em cidades diferentes dentro de 10 minutos",
    [
        transacao("cliente_a", "Crato", "2026-10-21T10:00:00"),
        transacao("cliente_a", "Fortaleza", "2026-10-21T10:05:00")
    ],
    [False, True]
)

# Caso 2: mesmo cliente, mesma cidade
testar_caso(
    "Mesmo cliente na mesma cidade",
    [
        transacao("cliente_b", "Crato", "2026-10-21T11:00:00"),
        transacao("cliente_b", "Crato", "2026-10-21T11:05:00")
    ],
    [False, False]
)

# Caso 3: clientes diferentes em cidades diferentes
testar_caso(
    "Clientes diferentes em cidades diferentes",
    [
        transacao("cliente_c", "Crato", "2026-10-21T12:00:00"),
        transacao("cliente_d", "Fortaleza", "2026-10-21T12:05:00")
    ],
    [False, False]
)

# Caso 4: mesmo cliente, mas com 15 minutos de diferença
testar_caso(
    "Cidades diferentes com 15 minutos de diferença",
    [
        transacao("cliente_e", "Crato", "2026-10-21T13:00:00"),
        transacao("cliente_e", "Fortaleza", "2026-10-21T13:15:00")
    ],
    [False, False]
)
