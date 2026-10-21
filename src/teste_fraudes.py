
from fraud_rules import verificar_fraude, historico_clientes


def criar_transacao(cliente, valor, cidade, horario):
    return {
        "transaction_id": f"{cliente}-{horario}",
        "customer_id": cliente,
        "amount": valor,
        "city": cidade,
        "timestamp": horario
    }


def testar(descricao, transacoes, esperado):
    historico_clientes.clear()

    resultados = []

    for transacao in transacoes:
        fraudes = verificar_fraude(transacao)
        resultados.append(fraudes)

    passou = resultados == esperado

    print(f"{'PASSOU' if passou else 'FALHOU'}: {descricao}")
    print("Resultado:", resultados)
    print("Esperado: ", esperado)
    print()


# Teste 1: transação de alto valor
testar(
    "Transação de alto valor",
    [
        criar_transacao(
            "cliente_a", 12000, "Crato",
            "2026-10-21T10:00:00"
        )
    ],
    [["ALTO_VALOR"]]
)


# Teste 2: quatro transações em menos de 60 segundos
testar(
    "Quatro transações em menos de 60 segundos",
    [
        criar_transacao("cliente_b", 100, "Crato", "2026-10-21T11:00:00"),
        criar_transacao("cliente_b", 100, "Crato", "2026-10-21T11:00:10"),
        criar_transacao("cliente_b", 100, "Crato", "2026-10-21T11:00:20"),
        criar_transacao("cliente_b", 100, "Crato", "2026-10-21T11:00:30")
    ],
    [[], [], [], ["TEMPO_60s"]]
)


# Teste 3: mesmo cliente em cidades diferentes
testar(
    "Mesmo cliente em cidades diferentes dentro de 10 minutos",
    [
        criar_transacao("cliente_c", 100, "Crato", "2026-10-21T12:00:00"),
        criar_transacao("cliente_c", 100, "Fortaleza", "2026-10-21T12:05:00")
    ],
    [[], ["GEO_10m"]]
)


# Teste 4: valor alto e regra geográfica ao mesmo tempo
testar(
    "Duas regras acionadas na mesma transação",
    [
        criar_transacao("cliente_d", 100, "Crato", "2026-10-21T13:00:00"),
        criar_transacao("cliente_d", 15000, "Fortaleza", "2026-10-21T13:01:00")
    ],
    [[], ["ALTO_VALOR", "GEO_10m"]]
)
