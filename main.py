import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=192.168.56.101,1433;"
    "DATABASE=TestDB;"
    "UID=LinuxSQL;"
    "PWD=nikola;"
    "Encrypt=no;"
    "TrustServerCertificate=yes;"
)

cursor = conn.cursor()
cursor.execute("CREATE TABLE Users (id INT IDENTITY PRIMARY KEY, name NVARCHAR(50))")
cursor.execute("INSERT INTO Users (name) VALUES ('Nikola')")
conn.commit()
print("Uspešno ubačeno!")
conn.close()
