from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuración de la carpeta de subida (asegúrate de que exista)
UPLOAD_FOLDER = os.path.join(app.root_path, 'images', 'galeria')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta para subir imágenes
@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No se encontró el archivo."
        file = request.files['image']
        if file.filename == '':
            return "No se seleccionó ningún archivo."
        if file and allowed_file(file.filename):
            # Se recibe la categoría seleccionada en el formulario
            category = request.form.get('category', 'SinCategoria')
            # Se asegura el nombre del archivo
            filename = secure_filename(file.filename)
            # Opcional: renombrar el archivo para incluir la categoría (en minúsculas)
            new_filename = f"{category.lower()}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(file_path)
            # Aquí podrías guardar la metadata en una base de datos o archivo si lo requieres
            return redirect(url_for('gallery'))
    return render_template('upload.html')

# Ruta para mostrar la galería agrupada por categoría
@app.route('/gallery')
def gallery():
    gallery_data = {}
    # Listar todos los archivos de la carpeta de galería
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if allowed_file(filename):
            # Suponemos que el nombre tiene el formato "categoria_nombre.jpg"
            parts = filename.split('_', 1)
            if len(parts) == 2:
                # Capitalizamos la categoría para mostrarla (por ejemplo, "cardio" -> "Cardio")
                category = parts[0].capitalize()
            else:
                category = "Sin Categoría"
            # Agrupar imágenes por categoría
            gallery_data.setdefault(category, []).append(filename)
    return render_template('gallery.html', gallery_data=gallery_data)

if __name__ == '__main__':
    app.run(debug=True)
