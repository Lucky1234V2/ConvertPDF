import base64
import io
import os

from flask import Flask, jsonify, render_template, request, send_file
from fpdf import FPDF
from PIL import Image

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({"error": "Aucun fichier sélectionné"}), 400
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "Aucun fichier sélectionné"}), 400

        if file:
            try:
                image = Image.open(file.stream)
                pdf_data = convert_image_to_pdf(image)

                # Envoyer le PDF généré en réponse
                response = send_file(
                    io.BytesIO(pdf_data),
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name='image_to_pdf.pdf'
                )

                return response
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    return render_template('index.html')


def convert_image_to_pdf(image):
    pdf = FPDF()
    pdf.add_page()
    # Convertir l'image PIL en bytes pour FPDF
    img_data = io.BytesIO()
    image.save(img_data, format='JPEG')
    img_data.seek(0)  # Revenir au début du flux
    pdf.image(img_data, x=10, y=10, w=190)
    pdf_data = pdf.output(dest='S').encode('latin1')
    return pdf_data


if __name__ == '__main__':
    app.run(debug=True)
