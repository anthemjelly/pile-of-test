import psycopg

# 测试连接+查询
conn = psycopg.connect("postgresql://user:password@host/dbname")
cur = conn.cursor()
cur.execute("SELECT 1")
print(cur.fetchone())  # 输出(1,)即正常
conn.close()
