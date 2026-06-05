import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import Image, ImageTk
import threading
import queue
from datetime import datetime

from msf_manager import msf_baslat, msf_kapat, msf_baglan
from scanner import tara
from exploiter import exploit_calistir
from database import tablo_olustur, tum_taramalar, tarama_detay

BG_COLOR     = "#0a0e27"
FG_COLOR     = "#00ff41"
ACCENT_COLOR = "#00d9ff"
BUTTON_BG    = "#1a2332"
BUTTON_HOVER = "#2d3e50"
HEADER_BG    = "#0d1117"

HEDEF_IP      = "192.168.109.128"
KALI_IP       = "192.168.109.129"
HEDEF_PORTLAR = "21,22,80,139,445,1524,3306,3632,5900,6667"


class PastaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PASTA")
        self.root.geometry("1450x850")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(True, True)

        self.msf = None
        self.kuyruk = queue.Queue()
        self.exploit_calisiyor = False

        self.baslik_olustur()
        self.altlik_olustur()
        self.menu_olustur()

        tablo_olustur()
        self.msf_baslat_thread()
        self.kuyruk_kontrol()

    def baslik_olustur(self):
        baslik = tk.Frame(self.root, bg=HEADER_BG, height=80)
        baslik.pack(fill=tk.X, side=tk.TOP)
        baslik.pack_propagate(False)

        tk.Label(baslik, text="PASTA",
                 font=("Courier New", 22, "bold"), fg=FG_COLOR, bg=HEADER_BG).pack(side=tk.LEFT, padx=20, pady=15)

        self.durum_label = tk.Label(
            baslik,
            text=f"DURUM: HAZIR | IP: {KALI_IP}",
            font=("Courier New", 12), fg=ACCENT_COLOR, bg=HEADER_BG
        )
        self.durum_label.pack(side=tk.RIGHT, padx=20, pady=15)

    def altlik_olustur(self):
        altlik = tk.Frame(self.root, bg=HEADER_BG, height=40)
        altlik.pack(fill=tk.X, side=tk.BOTTOM)
        altlik.pack_propagate(False)

        self.altlik_label = tk.Label(altlik, text="Hazir...",
                                     font=("Courier New", 12), fg=FG_COLOR, bg=HEADER_BG)
        self.altlik_label.pack(side=tk.LEFT, padx=20, pady=10)

    def menu_olustur(self):
        ana = tk.Frame(self.root, bg=BG_COLOR)
        ana.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        sol = tk.Frame(ana, bg=BG_COLOR, width=430)
        sol.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sol.pack_propagate(False)

        tk.Label(sol, text="PASTA",
                 font=("Courier New", 20, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=(10, 5))
        tk.Label(sol, text=f"Hedef: {HEDEF_IP}  |  Kali: {KALI_IP}",
                 font=("Courier New", 12), fg=FG_COLOR, bg=BG_COLOR).pack(pady=(0, 20))

        self.buton_ekle(sol, "1", "Metasploitable 2 Tara",  self.hizli_tara)
        self.buton_ekle(sol, "2", "Ozel Tara",              self.ozel_tara)
        self.buton_ekle(sol, "3", "Raporlari Goster",       self.raporlari_goster)
        self.buton_ekle(sol, "4", "Kanit Dosyalari",        self.kanitleri_goster)
        self.buton_ekle(sol, "5", "Cikis",                  self.cikis)

        sag = tk.Frame(ana, bg=BG_COLOR)
        sag.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(sag, text="TERMINAL",
                 font=("Courier New", 14, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack(anchor=tk.W, pady=(0, 5))

        self.terminal = scrolledtext.ScrolledText(
            sag, bg="#000000", fg=FG_COLOR,
            font=("Courier New", 12), insertbackground=FG_COLOR,
            relief=tk.FLAT, borderwidth=2,
            highlightthickness=2, highlightbackground=FG_COLOR
        )
        self.terminal.pack(fill=tk.BOTH, expand=True)
        self.log("Sistem baslatildi.")

    def buton_ekle(self, parent, numara, yazi, komut):
        cerceve = tk.Frame(parent, bg=BUTTON_BG, highlightbackground=FG_COLOR, highlightthickness=1)
        cerceve.pack(fill=tk.X, pady=8, ipady=12, ipadx=15)

        ic = tk.Frame(cerceve, bg=BUTTON_BG)
        ic.pack(fill=tk.X)

        n = tk.Label(ic, text=f"[{numara}]", font=("Courier New", 14, "bold"),
                     fg=ACCENT_COLOR, bg=BUTTON_BG, width=4)
        n.pack(side=tk.LEFT)

        t = tk.Label(ic, text=yazi, font=("Courier New", 14), fg=FG_COLOR, bg=BUTTON_BG, anchor=tk.W)
        t.pack(side=tk.LEFT, fill=tk.X, expand=True)

        