from db import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute("""
IF NOT EXISTS (
    SELECT * FROM sysobjects
    WHERE name='users' AND xtype='U'
)
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255),
    role VARCHAR(20)
)
""")
conn.commit()
print("Table created")