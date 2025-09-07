import os
from flask import Blueprint, request, jsonify, render_template, current_app
from .models import db, Reporte, ImagenReporte
from .services.report_extractor import extract_data_from_pdf

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Sirve el frontend principal."""
    return render_template('index.html')

@main_bp.route('/api/reports', methods=['GET'])
def get_reports():
    """Obtiene todos los reportes de la base de datos."""
    reports = Reporte.query.order_by(Reporte.fecha_carga.desc()).all()
    return jsonify([report.to_dict() for report in reports])

@main_bp.route('/api/upload', methods=['POST'])
def upload_report():
    if 'files' not in request.files:
        return jsonify({"error": "No se subieron archivos"}), 400

    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({"error": "No se seleccionaron archivos"}), 400

    image_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'images')
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    for file in files:
        pdf_content = file.read()
        
        extracted_data = extract_data_from_pdf(pdf_content)
        text_data = extracted_data["text_data"]
        images_data = extracted_data["images_data"]
        
        # 1. Crear el registro del reporte con los datos de texto
        nuevo_reporte = Reporte(
            nombre_archivo=file.filename,
            paciente_nombre=text_data.get('paciente_nombre'),
            tutor_nombre=text_data.get('tutor_nombre'),
            veterinario_nombre=text_data.get('veterinario_nombre'),
            diagnostico=text_data.get('diagnostico'),
            recomendaciones=text_data.get('recomendaciones')
        )
        db.session.add(nuevo_reporte)
        # Hacemos un "flush" para que nuevo_reporte obtenga un ID
        db.session.flush()

        # 2. Guardar cada imagen y asociarla al reporte
        for image_info in images_data:
            # Guardar el archivo de imagen en el servidor
            image_path = os.path.join(image_folder, image_info["filename"])
            with open(image_path, "wb") as image_file:
                image_file.write(image_info["bytes"])

            # Crear el registro en la base de datos
            nueva_imagen = ImagenReporte(
                nombre_archivo=image_info["filename"],
                reporte_id=nuevo_reporte.id
            )
            db.session.add(nueva_imagen)

    db.session.commit()
    
    return jsonify({"message": f"Archivos procesados: {len(files)}"}), 201