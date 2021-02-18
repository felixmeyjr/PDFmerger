from flask import Flask, render_template
import PyPDF2

app = Flask(__name__)

def merger(input_paths):
    pdf_merger = PyPDF2.PdfFileMerger()
    for i in input_paths:
        pdf_merger.append(i)
    output_path = input_paths[0]
    with open(output_path, "wb") as f_out:
        pdf_merger.write(f_out)

@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
