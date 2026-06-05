import sqlite3
import datetime

DB = "pasta.db"

def baglanti_ac():
    return sqlite3.connect(DB, check_same_thread=False)

def tablo_olustur():
    con = baglanti_ac()
    c = con.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS taramalar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hedef_ip TEXT,
        port_araligi TEXT,
        tarama_tarihi TEXT,
        durum TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS portlar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarama_id INTEGER,
        port INTEGER,
        servis TEXT,
        urun TEXT,
        versiyon TEXT,
        durum TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS zafiyetler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarama_id INTEGER,
        port INTEGER,
        tur TEXT,
        aciklama TEXT
    )""")
    con.commit()
    con.close()
    print("[+] Veritabani tablolari hazir")

def tarama_ekle(ip, portlar, durum="devam"):
    con = baglanti_ac()
    c = con.cursor()
    tarih = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    c.execute("INSERT INTO taramalar (hedef_ip, port_araligi, tarama_tarihi, durum) VALUES (?, ?, ?, ?)",
              (ip, portlar, tarih, durum))
    con.commit()
    tid = c.lastrowid
    con.close()
    return tid

def tarama_guncelle(tid, durum):
    con = baglanti_ac()
    c = con.cursor()
    c.execute("UPDATE taramalar SET durum=? WHERE id=?", (durum, tid))
    con.commit()
    con.close()

def port_ekle(tid, port, servis, urun, ver, durum):
    con = baglanti_ac()
    c = con.cursor()
    c.execute("INSERT INTO portlar (tarama_id, port, servis, urun, versiyon, durum) VALUES (?, ?, ?, ?, ?, ?)",
              (tid, port, servis, urun, ver, durum))
    con.commit()
    con.close()

def zafiyet_ekle(tid, port, tur, aciklama):
    con = baglanti_ac()
    c = con.cursor()
    c.execute("INSERT INTO zafiyetler (tarama_id, port, tur, aciklama) VALUES (?, ?, ?, ?)",
              (tid, port, tur, aciklama))
    con.commit()
    con.close()

def tum_taramalar():
    con = baglanti_ac()
    c = con.cursor()
    c.execute("SELECT * FROM taramalar ORDER BY id DESC")
    sonuc = c.fetchall()
    con.close()
    return sonuc

def tarama_detay(tid):
    con = baglanti_ac()
    c = con.cursor()
    c.execute("SELECT * FROM portlar WHERE tarama_id=?", (tid,))
    portlar = c.fetchall()
    c.execute("SELECT * FROM zafiyetler WHERE tarama_id=?", (tid,))
    zafiyetler = c.fetchall()
    con.close()
    return portlar, zafiyetler