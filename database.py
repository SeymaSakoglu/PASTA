import sqlite3
import datetime

baglanti = sqlite3.connect("pasta.db")
c = baglanti.cursor()

def tablo_olustur():
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
    baglanti.commit()
    print("[+] Veritabani tablolari hazir")

def tarama_ekle(ip, portlar, durum="devam"):
    tarih = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    c.execute("INSERT INTO taramalar (hedef_ip, port_araligi, tarama_tarihi, durum) VALUES (?, ?, ?, ?)",
              (ip, portlar, tarih, durum))
    baglanti.commit()
    return c.lastrowid

def tarama_guncelle(tid, durum):
    c.execute("UPDATE taramalar SET durum=? WHERE id=?", (durum, tid))
    baglanti.commit()

def port_ekle(tid, port, servis, urun, ver, durum):
    c.execute("INSERT INTO portlar (tarama_id, port, servis, urun, versiyon, durum) VALUES (?, ?, ?, ?, ?, ?)",
              (tid, port, servis, urun, ver, durum))
    baglanti.commit()

def zafiyet_ekle(tid, port, tur, aciklama):
    c.execute("INSERT INTO zafiyetler (tarama_id, port, tur, aciklama) VALUES (?, ?, ?, ?)",
              (tid, port, tur, aciklama))
    baglanti.commit()

def tum_taramalar():
    c.execute("SELECT * FROM taramalar ORDER BY id DESC")
    return c.fetchall()

def tarama_detay(tid):
    c.execute("SELECT * FROM portlar WHERE tarama_id=?", (tid,))
    portlar = c.fetchall()
    c.execute("SELECT * FROM zafiyetler WHERE tarama_id=?", (tid,))
    zafiyetler = c.fetchall()
    return portlar, zafiyetler