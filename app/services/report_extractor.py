import fitz  # PyMuPDF
import re
import os
import uuid
import io
from PIL import Image

def extract_data_from_pdf(pdf_content):
    """
    Función principal que extrae texto e imágenes, FILTRANDO las firmas y blancos.
    """
    text = extract_text_from_pdf(pdf_content)
    text_data = process_report_text(text)
    
    images_data = []
    
    MIN_WIDTH = 200
    MIN_HEIGHT = 200
    
    try:
        with fitz.open(stream=pdf_content, filetype="pdf") as doc:
            for page_num in range(len(doc)):
                for img in doc.get_page_images(page_num, full=True):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    try:
                        image_stream = io.BytesIO(image_bytes)
                        opened_image = Image.open(image_stream)
                        width, height = opened_image.size

                        # --- Filtro 1: Descartar por tamaño (más eficiente hacerlo primero) ---
                        if width < MIN_WIDTH or height < MIN_HEIGHT:
                            continue
                            
                        # --- Filtro 2: Descartar si es una imagen completamente blanca ---
                        # Convertimos a RGB para estandarizar el análisis de canales
                        img_rgb = opened_image.convert("RGB")
                        
                        # Obtenemos los valores mínimos y máximos de cada canal (R, G, B)
                        extrema = img_rgb.getextrema()
                        
                        is_solid_color = all(min_val == max_val for min_val, max_val in extrema)
                        
                        if is_solid_color:
                            continue

                    except Exception as e:
                        print(f"No se pudo procesar una imagen (formato inválido o corrupto), saltando: {e}")
                        continue
                    
                    ext = base_image["ext"]
                    image_filename = f"{uuid.uuid4()}.{ext}"
                    
                    images_data.append({
                        "filename": image_filename,
                        "bytes": image_bytes
                    })
    except Exception as e:
        print(f"Error al extraer imágenes: {e}")

    return {
        "text_data": text_data,
        "images_data": images_data
    }

def extract_text_from_pdf(pdf_content):
    """Extrae todo el texto de un flujo de bytes de un PDF."""
    text = ""
    try:
        with fitz.open(stream=pdf_content, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error al procesar PDF: {e}")
        return None
    return text

def process_report_text(text):
    """Extrae y normaliza la información clave usando expresiones regulares."""
    if not text:
        return {}

    # Expresiones regulares para buscar la información
    # La bandera re.DOTALL (o 's') permite que '.' coincida con saltos de línea
    # La bandera re.IGNORECASE (o 'i') hace que no distinga mayúsculas/minúsculas
    patterns = {
        'paciente_nombre': r"Paciente:\s*([^\n]*)",
        'tutor_nombre': r"Tutor:\s*([^\n]*)",
        'veterinario_nombre': r"Veterinario:\s*([^\n]*)",
        'diagnostico': r"Diagnóstico:\s*([\s\S]*?)Recomendaciones:",
        'recomendaciones': r"Recomendaciones:\s*([\s\S]*)"
    }
    
    extracted_data = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            # .strip() elimina espacios en blanco al inicio y al final
            extracted_data[key] = match.group(1).strip()
        else:
            extracted_data[key] = None
            
    return extracted_data