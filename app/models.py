from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ImagenReporte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    # Clave foránea para vincular la imagen con un reporte
    reporte_id = db.Column(db.Integer, db.ForeignKey('reporte.id'), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'url': f'/static/uploads/images/{self.nombre_archivo}'}

class Reporte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    fecha_carga = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Campos extraídos del reporte
    paciente_nombre = db.Column(db.String(150))
    tutor_nombre = db.Column(db.String(150))
    veterinario_nombre = db.Column(db.String(150))
    diagnostico = db.Column(db.Text)
    recomendaciones = db.Column(db.Text)

    # Esto nos permite acceder a las imágenes de un reporte con `reporte.imagenes`
    imagenes = db.relationship('ImagenReporte', backref='reporte', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        """Convierte el objeto a un diccionario para serialización JSON."""
        return {
            'id': self.id,
            'nombre_archivo': self.nombre_archivo,
            'fecha_carga': self.fecha_carga.isoformat(),
            'paciente_nombre': self.paciente_nombre,
            'tutor_nombre': self.tutor_nombre,
            'veterinario_nombre': self.veterinario_nombre,
            'diagnostico': self.diagnostico,
            'recomendaciones': self.recomendaciones,
            'imagenes': [img.to_dict() for img in self.imagenes]
        }