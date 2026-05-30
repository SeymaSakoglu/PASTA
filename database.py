import sqlite3
from datetime import datetime

VERITABANI = "pasta.db"

def veritabani_olustur():
	baglanti = sqlite3.connect(VERITABANI)
	cursor = baglanti.cursor()

	cursor.execute("""
		CREATE TABLE IF NOT EXISTS taramalar (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			ip_adresi TEXT NOT NULL,
			tarama_tarihi TEXT NOT NULL,
			durum TEXT NOT NULL
		)
	""")

	cursor.execute("""
		CREATE TABLE IF NOT EXISTS taramalar (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			tarama_id INTEGER NOT NULL,
			port INTEGER NOT NULL,
			servis TEXT,
			versiyon TEXT,
			durum TEXT,
			FOREING KEY (tarama_id) REFERANCES taramalar(id)
		)
	""")

	baglanti.commit()
	baglanti.close()
	print("[+] Veritabani hazir.")

	def tarama_kaydet(ip_adresi):
		baglanti = sqlite3.connect(VERITABANI)
		cursor = baglanti.cursor()

		tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		cursor.execute("""
			INSERT INTO taramalar (ip_adresi, tarama_tarihi, durum) VALUES (?, ?, ?)
		""", (ip_adresi, tarih, "tamamlandi"))

		tarama_id = cursor.lastrowid
		baglanti.commit()
		baglanti.close()
		return tarama_id

	def sonuc_kaydet(tarama_id, port, servis, versiyon, durum):
		baglanti = sqlite3.connect(VERITABANI)
		cursor = baglanti.cursor()

		cursor.execute("""
			INSERT INTO sonuclar (tarama_id ,port, servis, versiyon, durum) VALUES (?, ?, ?, ?)
		""", (tarama_id, port, servis, versiyon, durum))

		baglanti.commit()
		baglanti.close()

	def taramalari_listele():
		baglanti = sqlite3.connect(VERITABANI)
		cursor = baglanti.cursor()

		cursor.execute("SELECT * FROM taramalar")
		kayitlar = cursor.fetchall()
		baglanti.close()	
		return kayitlar