import base64
import os
from datetime import datetime
from io import BytesIO

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from fpdf import FPDF
from PIL import Image

app = Flask(__name__)

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
            image = Image.open(file.stream)

            img_io = BytesIO()
            image.save(img_io, format='JPEG')
            img_io.seek(0)
            img_base64 = base64.b64encode(img_io.getvalue()).decode()

            pdf = FPDF()
            pdf.add_page()
            pdf.image('@' + img_base64, x=0, y=0, w=210)

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            pdf_filename = f"image_to_pdf_{timestamp}.pdf"
            pdf_filepath = os.path.join(PDF_FOLDER, pdf_filename)
            pdf.output(pdf_filepath)

            pdf_rel_path = os.path.join('pdfs', pdf_filename)

            return redirect(url_for('download_pdf', pdf_filename=pdf_filename))

    return render_template('index.html', pdf_filepath=pdf_rel_path if pdf_filepath else None)


@app.route('/download/<pdf_filename>')
def download_pdf(pdf_filename):
    safe_pdf_filename = os.path.basename(pdf_filename)
    return send_from_directory(PDF_FOLDER, safe_pdf_filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
