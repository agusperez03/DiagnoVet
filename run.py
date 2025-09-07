from app import create_app

app = create_app()

# Flask shell
# >>> from app.models import db
# >>> db.drop_all()  # Borra todas las tablas
# >>> db.create_all() # Vuelve a crearlas con la nueva estructura
# >>> exit()

if __name__ == '__main__':
    app.run(debug=True)