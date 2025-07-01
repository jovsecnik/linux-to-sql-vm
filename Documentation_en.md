
# Project: Connecting Python to SQL Server on Windows VM from Linux Mint Host

## 🎯 Project Goal

Set up a system where a Linux host (Mint 22.1) uses a Python script to access SQL Server running inside a Windows VM (VirtualBox), using an ODBC connection to execute SQL queries.

Before starting, VirtualBox was installed on the host machine (Linux Mint). A Windows 10 LTS .iso was downloaded and installed in VB. The installation was standard, with no special configuration. Everything described in the text below is done on a clean, newly installed Windows 10.

## 🛠️ Tasks Performed

- Installing and configuring SQL Server on Windows VM
- Network configuration of the VM
- Enabling connection (Firewall + SQL options)
- Creating a user in SQL Server
- Installing required packages on Linux host
- Writing Python code for connecting and manipulating the database
- Debugging issues
- Setting up clipboard sharing between host and VM

## 1. Installing and Configuring SQL Server on Windows VM

SQL Server Express was downloaded and installed on the Windows 10 VM. Also installed was SSMS (SQL Server Management Studio) for graphical database management.

The database was initially set to use Windows Authentication to allow access to Management Studio. A database named `TestDB` was created.

## 2. VM Network Configuration

Initially, the VirtualBox network was set to **Bridged Adapter**, which tries to connect the VM directly to the same network as the host, acting like a physical device connected to your router.

However, the VM received an IP address like `169.254.X.X`, meaning it failed to obtain a DHCP-assigned IP. This often happens when the host is connected via Wi-Fi and the router does not forward DHCP for bridged adapters.

### ✅ Solution:

Two network adapters were added to the VM:

- **Adapter 1: NAT (Network Address Translation)** — allows internet access from the VM
- **Adapter 2: Host-only Adapter** — enables direct communication between host and VM

Example IP addresses:
- VM: `192.168.56.101`
- Host: `192.168.56.1`

## 3. Enabling SQL Server Connectivity

**Problem:** Python could not connect because TCP/IP was disabled or port 1433 was closed.

### Steps:

- Open SQL Server Configuration Manager > Protocols for MSSQLSERVER > TCP/IP > Enabled = Yes
- In the `IP Addresses` tab: clear the value in `TCP Dynamic Ports`, enter `1433` in `TCP Port`
- Restart the SQL Server service

### Firewall:

```bash
netsh advfirewall firewall add rule name="SQL TCP 1433" dir=in action=allow protocol=TCP localport=1433
```

## 4. Creating a User in SQL Server

**Why not Windows Authentication?**  
It only works if the user is already logged into a Windows environment or domain. Since we're accessing SQL Server from a Linux machine, this is not possible.

### Steps:

- In SSMS > Security > Logins > New Login...
- Login name: `LinuxSQL`
- Use SQL Server authentication, password: `nikola`
- Disable "Enforce password policy"
- Assign all server roles (sysadmin)

## 5. Installing Packages on Linux Host (Mint 22.1)

```bash
sudo apt install curl gnupg
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo curl -o /etc/apt/sources.list.d/mssql-release.list https://packages.microsoft.com/config/debian/12/prod.list
sudo apt update
sudo ACCEPT_EULA=Y apt install msodbcsql18 unixodbc-dev
apt install python3-pyodbc
```

## 6. Python Code to Connect and Manipulate the Database

```python
import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=192.168.56.101,1433;"
    "DATABASE=testDB;"
    "UID=LinuxSQL; PWD=nikola;"
    "Encrypt=no;TrustServerCertificate=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE Users (id INT IDENTITY PRIMARY KEY, name NVARCHAR(50))")
    cursor.execute("INSERT INTO Users (name) VALUES ('Nikola')")
    conn.commit()
    print("Success!")
except Exception as e:
    print("Error:", e)
finally:
    conn.close()
```

This code successfully created a table and inserted a record from Linux Mint into SQL Server on a Windows VM using ODBC.

## 7. Copy/Paste and Integration

- `VBoxGuestAdditions.exe` installed in the Windows VM
- In VirtualBox: Settings > General > Advanced:
  - Shared Clipboard: Bidirectional
  - Drag and Drop: Bidirectional
