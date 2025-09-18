# DiagnoVET - Asistente de Diagnóstico Veterinario con IA 🩺

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

---

## 📖 Descripción del Proyecto

En DiagnoVET estamos transformando la medicina veterinaria con inteligencia artificial. Hoy, los veterinarios tardan en promedio 45 minutos en redactar un informe diagnóstico, una tarea que genera estrés, burnout y les quita tiempo valioso de la atención animal. Nuestra plataforma reduce este proceso a solo 5 minutos, utilizando un LLM para extraer y estructurar la información clave de los reportes en PDF, devolviendo a los profesionales horas cada semana para enfocarse en lo que realmente importa: sus pacientes.

---

## Deployed - onrender
https://diagnovet-app.onrender.com

---

## ✨ Características Principales

* **Carga de Múltiples Archivos:** Sube uno o más reportes veterinarios en formato PDF simultáneamente.
* **Extracción de Datos con IA:** Utiliza la API de **Google Gemini** para analizar el texto no estructurado y extraer información clave de forma inteligente.
* **Datos Estructurados:** Normaliza la información del paciente (nombre, especie, raza, edad, sexo) en un objeto anidado y extrae datos del tutor, veterinario, diagnóstico y recomendaciones.
* **Extracción de Imágenes:** Detecta y extrae automáticamente todas las imágenes incrustadas en los archivos PDF.
* **Filtrado Inteligente de Imágenes**
* **Galería Interactiva:** Muestra las imágenes relevantes en una galería responsive con la funcionalidad de Lightbox2 para verlas en pantalla completa.
* **Interfaz Simple:** Una interfaz web limpia y fácil de usar para la carga de archivos y la visualización de resultados.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3.9+
* **Framework Web:** Flask
* **Base de Datos:** PostgreSQL
* **ORM:** SQLAlchemy
* **Extracción de PDF:** PyMuPDF
* **Procesamiento de Imágenes:** Pillow
* **Modelo de Lenguaje (LLM):** Google Gemini API
* **Contenerización:** Docker para la gestión de la base de datos.
* **Frontend:** HTML5, CSS3, JavaScript (vanilla)
* **Galería de Imágenes:** Lightbox2
* **Gestión de Entorno:** python-dotenv

---

## 🚀 Puesta en Marcha y Configuración

Sigue estos pasos para levantar el proyecto en un entorno de desarrollo local.

### Prerrequisitos

* Python 3.8+
* Docker y Docker Compose
* Una cuenta de Google para obtener la API Key de Gemini.

### 1. Configurar Variables de Entorno

Este proyecto utiliza un archivo `.env` para gestionar las claves de API de forma segura.

1.  Crea un archivo llamado `.env` en la raíz del proyecto.
2.  Copia el contenido del siguiente bloque en tu nuevo archivo `.env`.

    ```
    # Archivo .env
    # Reemplaza el valor con tu clave de API obtenida de Google AI Studio
    GOOGLE_API_KEY="TU_API_KEY_DE_GEMINI_AQUÍ"
    ```

### 2. Iniciar la Base de Datos con Docker

Ejecuta el siguiente comando en la terminal para descargar e iniciar un contenedor de PostgreSQL:

```bash
docker run --name diagnovet-db -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_USER=user -e POSTGRES_DB=diagnovet -p 5432:5432 -d postgres
```

### 3. Configurar el entorno de Python
  ```
  # Crear un entorno virtual
  python -m venv venv
  
  # Activar el entorno virtual
  # En Windows:
  venv\Scripts\activate
  # En macOS/Linux:
  source venv/bin/activate
  
  # Instalar las dependencias del proyecto
  pip install -r requirements.txt
  ```

### 4. Iniciar la BD y correr la AP!

```
# Abre un shell interactivo de Flask
flask shell

from app.models import db
db.create_all()
exit()

flask run
```

La aplicación estará disponible en `http://127.0.0.1:5000`.










