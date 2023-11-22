import base64
import os
from io import BytesIO
from tempfile import NamedTemporaryFile

from flask import Flask, jsonify, request, send_file
from fpdf import FPDF
from PIL import Image

app = Flask(__name__)


@app.route('/', methods=['POST'])
def convert_to_pdf():
    try:
        # Récupérer les données JSON de la requête
        data = request.get_json()

        # Récupérer l'image base64 à partir des données JSON
        image_base64 = data.get('image', '')

        # Créer une instance de FPDF
        pdf = FPDF()
        pdf.add_page()

        # Convertir l'image base64 en format image
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))

        # Sauvegarder l'image temporairement
        with NamedTemporaryFile(delete=False, suffix='.jpg') as temp_img:
            image.save(temp_img, format='JPEG')
            temp_img_path = temp_img.name

        # Ajouter l'image au PDF
        pdf.image(temp_img_path, x=0, y=0, w=210)

        # Supprimer le fichier temporaire
        os.remove(temp_img_path)

        # Enregistrer le PDF généré dans un fichier temporaire
        pdf_file = NamedTemporaryFile(delete=False, suffix='.pdf')
        pdf_file.close()
        pdf.output(pdf_file.name)

        # Renvoyer le fichier PDF généré en réponse
        return send_file(pdf_file.name, as_attachment=True, download_name='output.pdf')

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run()
