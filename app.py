import os
import tempfile
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
    pdf_filepath = None
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'Aucun fichier sélectionné', 400
        file = request.files['image']
        if file.filename == '':
            return 'Aucun fichier sélectionné', 400

        if file:
            # Utilisation d'un répertoire temporaire pour stocker l'image
            with tempfile.TemporaryDirectory() as temp_dir:
                image_path = os.path.join(temp_dir, "temp_image.jpg")
                image = Image.open(file.stream)
                image.save(image_path)

                pdf = FPDF()
                pdf.add_page()
                pdf.image(image_path, x=0, y=0, w=210)

                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                pdf_filename = f"image_to_pdf_{timestamp}.pdf"
                pdf_filepath = os.path.join(PDF_FOLDER, pdf_filename)
                pdf.output(pdf_filepath)

                # Génère le chemin relatif pour le template
                pdf_rel_path = os.path.join('pdfs', pdf_filename)

        # Supprime l'image temporaire après avoir créé le PDF
        os.remove(image_path)

        return redirect(url_for('download_pdf', pdf_filename=pdf_filename))

    return render_template('index.html', pdf_filepath=pdf_rel_path if pdf_filepath else None)


@app.route('/download/<pdf_filename>')
def download_pdf(pdf_filename):
    # Sécurise le nom du fichier pour éviter les chemins d'accès relatifs
    safe_pdf_filename = os.path.basename(pdf_filename)
    return send_from_directory(PDF_FOLDER, safe_pdf_filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
