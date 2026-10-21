
import sqlite3

conexao = sqlite3.connect("data/transacoes.db")

registros = conexao.execute("""
    SELECT customer_id, amount, city, timestamp, fraude, tipo_fraude
    FROM transacoes
    WHERE customer_id = ?
    ORDER BY timestamp
""", ("cliente_5",)).fetchall()

for registro in registros:
    print(registro)

conexao.close()
