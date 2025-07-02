
# Projekat: Povezivanje Python koda sa SQL Serverom na Windows VM iz Linux Mint hosta

## 🎯 Cilj projekta

Napraviti postavku gde se koristi Linux host (Mint 22.1) da putem Python skripte pristupi SQL Serveru koji se nalazi unutar Windows VM-a (VirtualBox), koristi ODBC konekciju i izvršava SQL upite.

Pre samog početka, na host računaru (Linux Mint) je instaliran VirtualBox. Skinut je .iso Windowsa 10 LTS i instaliran je na VB. Instalacija je bila klasična, ništa specijalno konfigurisano, sve što bude opisano u tekstu dalje se radi na čistom, novoinstaliranom Windowsu 10.

## 🛠️ Šta je sve rađeno

- Instalacija i konfiguracija SQL Servera na Windows VM
- Mrežna konfiguracija VM-a
- Omogućavanje konekcije (Firewall + SQL opcije)
- Pravljenje korisnika u SQL Serveru
- Instalacija potrebnih paketa na Linux hostu
- Pisanje Python koda za konekciju i manipulaciju bazom
- Debug problema i njihovo rešavanje
- Postavljanje clipboard-a između hosta i VM-a

## 1. Instalacija i konfiguracija SQL Servera na Windows VM

Preuzet je SQL Server Express i instaliran na Windows 10 VM. Takođe instaliran je SSMS (SQL Server Management Studio) za grafičko upravljanje bazama.

U bazi je trenutno postavljen Windows Authentication kako bi moglo da se uđe u Management Studio. Napravljena je baza `TestDB`.

## 2. Mrežna konfiguracija VM-a

Prvobitno je VirtualBox mreža bila podešena kao **Bridged Adapter**. Bridged adapter pokušava da poveže VM direktno na istu mrežu kao i host — kao da je fizički uređaj priključen na ruter.

Međutim, VM je dobijala IP adresu `169.254.X.X`, što znači da nije uspela da dobije adresu preko DHCP-a. To se često dešava kada je host povezan putem Wi-Fi i ruter ne prosleđuje DHCP za bridged adaptere.

### ✅ Rešenje:

Postavljena su **dva mrežna adaptera** u VM:

- **Adapter 1: NAT (Network Address Translation)** — omogućava VM-u pristup internetu
- **Adapter 2: Host-only Adapter** — omogućava direktnu komunikaciju između hosta i VM-a

Primer IP adresa:
- VM: `192.168.56.101`
- Host: `192.168.56.1`

## 3. Omogućavanje konekcije u SQL Serveru

Problem: Python skripta nije mogla da se poveže jer TCP/IP nije bio omogućen ili port 1433 nije bio otvoren.

### Koraci:

- SQL Server Configuration Manager > Protocols for MSSQLSERVER > TCP/IP > Enabled = Yes
- U tabu `IP Addresses`: obrisati vrednost iz `TCP Dynamic Ports`, uneti `1433` u `TCP Port`
- Restartovati SQL Server servis

### Firewall:

```bash
netsh advfirewall firewall add rule name="SQL TCP 1433" dir=in action=allow protocol=TCP localport=1433
```

## 4. Kreiranje korisnika u SQL Serveru

Windows Authentication ne radi jer Linux ne može da se predstavi kao Windows korisnik.

### Koraci:

- SSMS > Security > Logins > New Login...
- Login name: `LinuxSQL`
- SQL Server authentication, password: `nikola`
- Isključiti "Enforce password policy"
- Dodeliti sve server role (sysadmin)

## 5. Instalacija paketa na Linux hostu (Mint 22.1)

```bash
sudo apt install curl gnupg
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo curl -o /etc/apt/sources.list.d/mssql-release.list https://packages.microsoft.com/config/debian/12/prod.list
sudo apt update
sudo ACCEPT_EULA=Y apt install msodbcsql18 unixodbc-dev
apt install python3-pyodbc
```

## 6. Python kod za konekciju i manipulaciju bazom

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
    print("Uspešno!")
except Exception as e:
    print("Greska:", e)
finally:
    conn.close()
```

Ovaj kod je uspešno iz Linux Mint-a, putem ODBC-a, kreirao tabelu i uneo podatak u `TestDB` bazu na Windows VM-u.

## 7. Copy/Paste i integracija

- U Windows VM instaliran `VBoxGuestAdditions.exe`
- U VirtualBox: Settings > General > Advanced:
  - Shared Clipboard: Bidirectional
  - Drag and Drop: Bidirectional
