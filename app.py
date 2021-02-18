from flask import Flask, render_template
import PyPDF2

app = Flask(__name__)

# Merge the pdf, which are uploaded on the website
def merger(input_files, input_path):
    pdf_merger = PyPDF2.PdfFileMerger()
    for i in input_files:
        pdf_merger.append(i)
    output_path = input_path
    with open(output_path, "wb") as f_out:
        pdf_merger.write(f_out)
    return f_out

@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
