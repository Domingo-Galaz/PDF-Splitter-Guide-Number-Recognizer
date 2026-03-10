import os
import re
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np
import pikepdf
import pdfplumber

# Ruta Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class SeparadorGuiasPro:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Splitter and N° Recognizer v2.1")
        self.root.geometry("450x350")
        self.pdf_path = None

        tk.Label(root, text="Massive PDF Splitter and N° Recognizer", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Button(root, text="1. Select PDF", command=self.seleccionar_pdf, width=25).pack(pady=5)
        self.btn_procesar = tk.Button(root, text="2. Start Split", command=self.iniciar_proceso, 
                                     width=25, state=tk.DISABLED, bg="#d4edda")
        self.btn_procesar.pack(pady=5)

        self.progress = Progressbar(root, length=350, mode='determinate')
        self.progress.pack(pady=20)
        self.estado = tk.Label(root, text="Waiting for file...", fg="gray")

        footer_frame = tk.Frame(root)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        texto_pie = "Created by Domingo Galaz Ramirez © All rights reserved"
        tk.Label(footer_frame, text=texto_pie, font=("Arial", 8, "italic"), fg="gray").pack()
        
        # Ajusta el tamaño de la ventana para que quepa el texto
        self.root.geometry("450x400")

        self.estado.pack()

    def seleccionar_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.pdf_path:
            self.btn_procesar.config(state=tk.NORMAL)
            self.estado.config(text="PDF loaded correctly", fg="blue")

    def extraer_numero_robusto(self, texto):
        texto = texto.upper().replace('O', '0').replace('I', '1')
        
        # 1. Buscar N° 829597 [cite: 12, 35, 62]
        match_std = re.search(r"N[°\.\s]{1,3}(\d{6,8})", texto)
        if match_std:
            return match_std.group(1)
            
        # 2. Buscar en cadena de código de barras [cite: 26, 46, 72]
        match_long = re.search(r"000000000(\d{8})0000000000", texto)
        if match_long:
            return match_long.group(1)
            
        return None

    def procesar_pagina_ocr(self, i):
        img_list = convert_from_path(self.pdf_path, first_page=i+1, last_page=i+1, 
                                   dpi=250, poppler_path=r"C:\poppler\Library\bin")
        if not img_list: return None
            
        img = np.array(img_list[0])
        h, w, _ = img.shape
        crop = img[int(h*0.02):int(h*0.20), int(w*0.60):w]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        texto_ocr = pytesseract.image_to_string(gray, config='--psm 6')
        return self.extraer_numero_robusto(texto_ocr)

    def iniciar_proceso(self):
        self.btn_procesar.config(state=tk.DISABLED)
        threading.Thread(target=self.ejecutar_logica, daemon=True).start()

    def ejecutar_logica(self):
        try:
            output_dir = "Separate_Files"
            error_dir = os.path.join(output_dir, "Unidentified")
            os.makedirs(error_dir, exist_ok=True)

            pdf_original = pikepdf.open(self.pdf_path)
            total = len(pdf_original.pages)
            self.progress["maximum"] = total

            with pdfplumber.open(self.pdf_path) as plub:
                for i in range(total):
                    texto_nativo = plub.pages[i].extract_text() or ""
                    num = self.extraer_numero_robusto(texto_nativo)
                    
                    if not num:
                        num = self.procesar_pagina_ocr(i)

                    # --- SECCIÓN MODIFICADA ---
                    if num:
                        # Ahora el nombre es solo el número [cite: 12, 35, 62]
                        nombre_final = f"{num}.pdf"
                        ruta_destino = os.path.join(output_dir, nombre_final)
                    else:
                        nombre_final = f"Page_{i+1}_Review.pdf"
                        ruta_destino = os.path.join(error_dir, nombre_final)
                    # --------------------------

                    count = 1
                    base, ext = os.path.splitext(ruta_destino)
                    while os.path.exists(ruta_destino):
                        ruta_destino = f"{base}_{count}{ext}"
                        count += 1

                    nueva_guia = pikepdf.new()
                    nueva_guia.pages.append(pdf_original.pages[i])
                    nueva_guia.save(ruta_destino)

                    self.progress["value"] = i + 1
                    self.estado.config(text=f"Processing {i+1} of {total}...")
                    self.root.update_idletasks()

            pdf_original.close()
            
            # --- APERTURA AUTOMÁTICA DE CARPETA ---
            os.startfile(os.path.abspath(output_dir))
            # ---------------------------------------
            
            messagebox.showinfo("Completed", f"Processed {total} guides.\nThe folder has been opened automatically.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.btn_procesar.config(state=tk.NORMAL)
            self.estado.config(text="Process completed")

if __name__ == "__main__":
    root = tk.Tk()
    app = SeparadorGuiasPro(root)
    root.mainloop()
