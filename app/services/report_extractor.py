import fitz  # PyMuPDF
import re
import os
import uuid
import io
from PIL import Image
import json
import google.generativeai as genai

#Crear el archivo .env y colocar api key de gemini
try:
    api_key = os.environ["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # Usamos un modelo rápido y eficiente, ideal para extracción de datos.
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"Error al configurar Gemini: Asegúrate de haber establecido la variable de entorno GOOGLE_API_KEY. Error: {e}")
    model = None

def extract_data_with_gemini(text: str) -> dict:
    """
    Usa el LLM de Gemini para extraer información estructurada del texto de un reporte.
    """
    if not model:
        raise ConnectionError("El modelo de Gemini no está configurado. Revisa la API Key.")
        
    # --- PROMPT ENGINEERING ---
    prompt = f"""
    Eres un asistente experto en analizar informes de diagnóstico veterinario. Tu tarea es extraer la siguiente información del texto que te proporciono y devolverla estrictamente en formato JSON.

    Las claves que debes usar en el JSON son:
    - "paciente_nombre": Ademas del nombre, agrega detalles encontrados como, edad, especie, raza y sexo separados por coma
    - "tutor_nombre": El nombre del tutor o propietario.
    - "veterinario_nombre": El nombre del profesional. Busca explícitamente etiquetas como "Veterinario", "Derivante", "Profesional Solicitante" o similares.
    - "observaciones": Un resumen de los hallazgos clínicos o descriptivos del estudio.
    - "diagnostico": La conclusión diagnóstica del especialista.
    - "recomendaciones": Las acciones o tratamientos sugeridos.

    Reglas importantes:
    1.  NO inventes información. Si un campo no se encuentra en el texto, su valor en el JSON debe ser null.
    2.  El campo "observaciones" debe contener un resumen de los hallazgos clínicos o descriptivos del estudio.
    3.  El campo "diagnostico" debe contener la conclusión diagnóstica del especialista.
    4.  Tu respuesta debe ser únicamente el objeto JSON, sin texto introductorio, explicaciones adicionales, ni ```json ``` al inicio o final.

    Aquí tienes el texto del informe para analizar:
    ---
    {text}
    ---
    """

    try:
        response = model.generate_content(prompt)
        # El LLM devuelve el JSON como texto, lo convertimos a un diccionario de Python
        return json.loads(response.text)
    except Exception as e:
        print(f"Error al llamar a la API de Gemini o al procesar la respuesta: {e}")
        # En caso de error, devolvemos un diccionario vacío para no romper la aplicación
        return {
            "paciente_nombre": None, "tutor_nombre": None, "veterinario_nombre": None,
            "observaciones": None, "diagnostico": None, "recomendaciones": None
        }

def es_imagen_util(image: Image.Image, min_width: int = 200, min_height: int = 200) -> bool:
    """
    Devuelve True si la imagen es útil (no es demasiado pequeña ni completamente blanca).
    """
    width, height = image.size
    if width < min_width or height < min_height:
        return False
    img_rgb = image.convert("RGB")
    extrema = img_rgb.getextrema()
    is_solid_color = all(min_val == max_val for min_val, max_val in extrema)
    if is_solid_color:
        return False
    return True

def extract_data_from_pdf(pdf_content):
    """
    Función principal que extrae texto e imágenes, FILTRANDO las firmas y blancos.
    """
    text = extract_text_from_pdf(pdf_content)
    text_data = extract_data_with_gemini(text) if text else {}
    
    images_data = []

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

                        if not es_imagen_util(opened_image):
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