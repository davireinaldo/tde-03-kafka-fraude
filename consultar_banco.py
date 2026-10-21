
import sqlite3

conexao = sqlite3.connect("data/transacoes.db")

cursor = conexao.execute("""
    SELECT
        transaction_id,
        customer_id,
        amount,
        city,
        timestamp,
        fraude,
        tipo_fraude
    FROM transacoes
    ORDER BY id DESC
    LIMIT 10
""")

transacoes = cursor.fetchall()

for transacao in transacoes:
    print(transacao)

conexao.close()
