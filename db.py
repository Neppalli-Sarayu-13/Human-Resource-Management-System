import pyodbc

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-BI5KSME;"
        "DATABASE=ADDS;"
        "UID=sa;"
        "PWD=1234;"
        "TrustServerCertificate=yes;"
    )
