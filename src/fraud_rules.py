
from datetime import datetime


historico_clientes = {}


def verificar_fraude(transacao):
    fraudes = []

    cliente = transacao["customer_id"]
    valor = transacao["amount"]
    cidade = transacao["city"]
    momento = datetime.fromisoformat(transacao["timestamp"])

    # Regra 1: transação de alto valor
    if valor >= 10000:
        fraudes.append("ALTO_VALOR")

    # Cria o histórico do cliente, caso ainda não exista
    if cliente not in historico_clientes:
        historico_clientes[cliente] = []

    historico = historico_clientes[cliente]

    # Mantém somente transações dos últimos 10 minutos
    historico = [
        evento for evento in historico
        if (momento - evento["timestamp"]).total_seconds() <= 600
    ]

    # Adiciona a transação atual ao histórico
    historico.append({
        "timestamp": momento,
        "city": cidade
    })

    historico_clientes[cliente] = historico

    # Regra 2: quatro transações em menos de 60 segundos
    transacoes_recentes = [
        evento for evento in historico
        if (momento - evento["timestamp"]).total_seconds() < 60
    ]

    if len(transacoes_recentes) >= 4:
        fraudes.append("TEMPO_60s")

    # Regra 3: transações do mesmo cliente em cidades diferentes
    cidades_diferentes = any(
        evento["city"] != cidade
        for evento in historico
        if evento["timestamp"] != momento
    )

    if cidades_diferentes:
        fraudes.append("GEO_10m")

    return fraudes
