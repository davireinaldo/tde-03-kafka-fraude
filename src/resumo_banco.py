
import sqlite3

conexao = sqlite3.connect("data/transacoes.db")

total = conexao.execute("""
    SELECT COUNT(*) FROM transacoes
""").fetchone()[0]

suspeitas = conexao.execute("""
    SELECT COUNT(*) FROM transacoes WHERE fraude = 1
""").fetchone()[0]

sem_alerta = conexao.execute("""
    SELECT COUNT(*) FROM transacoes WHERE fraude = 0
""").fetchone()[0]

print("Total de transações:", total)
print("Transações com alertas:", suspeitas)
print("Transações sem alertas:", sem_alerta)

print("\nResumo por tipo de alerta:")

resumo = conexao.execute("""
    SELECT tipo_fraude, COUNT(*)
    FROM transacoes
    WHERE fraude = 1
    GROUP BY tipo_fraude
    ORDER BY COUNT(*) DESC
""").fetchall()

for tipo, quantidade in resumo:
    print(f"{tipo}: {quantidade}")

conexao.close()
