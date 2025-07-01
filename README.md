
# 🐧 Linux to SQL Server on Windows VM

This project demonstrates how to connect Python code running on a **Linux Mint host** to a **SQL Server instance running on a Windows Virtual Machine (VM)** using `pyodbc` and `ODBC Driver 18`.

---

## 🎯 Project Goal

Enable remote interaction with a SQL Server database on a Windows VM from Python scripts on a Linux machine.

---

## 📁 Contents

- ✔️ VM Network Configuration (NAT + Host-Only)
- ✔️ SQL Server Setup and Configuration
- ✔️ Firewall and TCP/IP Enabling (port 1433)
- ✔️ SQL User Authentication (SQL Auth only)
- ✔️ Installing pyodbc and msodbcsql18 on Linux
- ✔️ Python code example to insert into SQL table
- ✔️ Clipboard sharing between host and VM
- ✔️ Full documentation in Serbian and English

---

## 🧪 Quick Python Example

```python
import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=192.168.56.101,1433;"
    "DATABASE=testDB;"
    "UID=linux;"
    "PWD=0668080569;"
    "Encrypt=no;TrustServerCertificate=yes;"
)
cursor = conn.cursor()
cursor.execute("INSERT INTO Users (name) VALUES ('Nikola')")
conn.commit()
conn.close()
```

---

## 📦 Requirements

- Python 3
- pyodbc
- msodbcsql18
- A SQL Server running on a Windows VM
- VM configured with NAT and Host-Only networking

Install dependencies:

```bash
sudo apt install curl gnupg unixodbc-dev
pip install pyodbc
```

---

## 📄 Documentation

- [📘 Dokumentacija na srpskom (Markdown)](Dokumentacija_sr.md)
- [📘 English Documentation (Markdown)](Documentation_en.md)

---

## 🖼️ Screenshots

Place all screenshots in the `screenshots/` folder.

---

## 👤 Author

Nikola Jovanović – first GitHub project documenting cross-platform database communication.

---

## 📝 License

MIT License (or leave blank if not applying one)
