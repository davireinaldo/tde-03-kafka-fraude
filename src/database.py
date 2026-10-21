
import sqlite3


def conectar_banco():
    conexao = sqlite3.connect("data/transacoes.db")
    return conexao


def criar_tabela():
    conexao = conectar_banco()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT UNIQUE,
            customer_id TEXT,
            amount REAL,
            city TEXT,
            timestamp TEXT,
            fraude INTEGER DEFAULT 0,
            tipo_fraude TEXT
        )
    """)

    conexao.commit()
    conexao.close()

    print("Tabela de transações criada com sucesso!")


def salvar_transacao(transacao, fraudes):
    conexao = conectar_banco()

    try:
        conexao.execute("""
            INSERT INTO transacoes (
                transaction_id,
                customer_id,
                amount,
                city,
                timestamp,
                fraude,
                tipo_fraude
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            transacao["transaction_id"],
            transacao["customer_id"],
            transacao["amount"],
            transacao["city"],
            transacao["timestamp"],
            1 if fraudes else 0,
            ", ".join(fraudes) if fraudes else None
        ))

        conexao.commit()

    finally:
        conexao.close()
