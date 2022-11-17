import secrets
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import datetime
import PyPDF2
import re
import stats

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

year = datetime.date.today().year


@app.route(rule='/', methods=["GET", "POST"])
def home():
    result, download_filename = None, None
    if request.method == "POST":
        # Save file
        file = request.files.get(key='file')
        filename = secure_filename(filename=file.filename)
        download_filename = filename.replace(".pdf", ".txt")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(dst=file_path)

        # Get advanced settings form data
        advanced_settings = request.form.get('advanced-settings')
        regex, sorting, multiples = None, None, None
        if advanced_settings:
            regex = request.form.get('regex')
            sorting = request.form.get('sorting')
            multiples = request.form.get('multiples')

        # Default regex value
        if not advanced_settings or not regex:
            regex = "(?<!\d)\d{8}(?!\d)"

        # Open file and extract data
        with open(file=file_path, mode='rb') as pdf_file_obj:
            result = []
            pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
            num_pages = pdf_reader.numPages

            for page_num in range(num_pages):
                page_obj = pdf_reader.getPage(page_num)
                new_matches = re.findall(regex, page_obj.extractText())
                for match in new_matches:
                    if multiples or match not in result:
                        result.append(match)

            # Sort the result if requested
            if sorting == "2":
                result.sort()
            elif sorting == "3":
                result.sort(reverse=True)

            # Update JSON
            stats.update_stats(num_of_strings=len(result))

        # Delete file
        os.remove(path=file_path)

    # Get JSON stats
    data = stats.read_stats()

    return render_template(template_name_or_list="index.html", year=year, result=result,
                           stats=data, filename=download_filename)


if __name__ == "__main__":
    app.run(debug=True)
