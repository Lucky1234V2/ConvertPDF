import os
from datetime import datetime

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from fpdf import FPDF
from PIL import Image

app = Flask(__name__)

# Assurez-vous que ce dossier existe
PDF_FOLDER = os.path.join('static', 'pdfs')
os.makedirs(PDF_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    pdf_filepath = None  # Initialise la variable pour qu'elle soit accessible en dehors du if
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'Aucun fichier sélectionné', 400
        file = request.files['image']
        if file.filename == '':
            return 'Aucun fichier sélectionné', 400

        if file:
            image_path = os.path.join(PDF_FOLDER, "temp_image.jpg")
            image = Image.open(file.stream)
            image.save(image_path)

            pdf = FPDF()
            pdf.add_page()
            pdf.image(image_path, x=0, y=0, w=210)

            # Créer un nom de fichier unique pour le PDF
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            pdf_filename = f"image_to_pdf_{timestamp}.pdf"
            pdf_filepath = os.path.join(PDF_FOLDER, pdf_filename)
            pdf.output(pdf_filepath)

            os.remove(image_path)  # Supprime l'image temporaire

            # Génère le chemin relatif pour l'utilisation dans le template
            pdf_rel_path = os.path.join('pdfs', pdf_filename)

            # Redirection vers le téléchargement
            return redirect(url_for('download_pdf', pdf_filename=pdf_filename))

    # Si pas POST ou après l'enregistrement de l'image, affiche la page normalement
    return render_template('index.html', pdf_filepath=pdf_rel_path if pdf_filepath else None)


@app.route('/download/<pdf_filename>')
def download_pdf(pdf_filename):
    # Sécurise le nom du fichier pour éviter les chemins d'accès relatifs
    safe_pdf_filename = os.path.basename(pdf_filename)
    return send_from_directory(PDF_FOLDER, safe_pdf_filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
