from flask import Flask, render_template, request, make_response, send_file
from PyPDF2 import PdfFileMerger
import sqlite3 as sql

app = Flask(__name__)


def createDB():
    conn = sql.connect('database.db')
    app.logger.info("Opened database successfully")
    conn.execute("CREATE TABLE files (filename TEXT, file BLOB)")
    conn.close()


@app.route('/', methods=["POST", "GET"])
def index():
    response = make_response(render_template("index.html", title="home"))
    return response


# Upload the files to a sql database
@app.route("/upload/", methods=['POST'])
def upload():
    if request.method == 'POST':
        try:
            f = request.files.getlist("mergeFile[]")
            currentFiles = []

            con = sql.connect("database.db")

            cur = con.cursor()

            print(f.filename)
            print(con)
            print(cur)
            print("file:" + f.filename)

            cur.execute("INSERT INTO files (filename,file) VALUES (?,?)", (f.filename, f.read()))
            con.commit()
            print("Record successfully added")

            cur.close()
            con.close()
        except:
            print("error in insert operation")
            return render_template('index.html', file_names=currentFiles, title='Home')
        finally:
            return render_template('index.html', file_names=currentFiles, title='Home')


# Get the files from database and merge
@app.route("/merge/", methods=['POST'])
def merger():
    pdf_merger = PdfFileMerger()
    con = sql.connect("database.db")
    cursor = con.cursor()
    input_files = cursor.execute("SELECT * FROM files")

    for row in input_files:
        pdf_merger.append(row)
        # merger.append(io.BytesIO(row[3]))

    with open('./downloads/result.pdf', "wb") as f_out:
        pdf_merger.write(f_out)
    return send_file('./downloads/result.pdf',
                     mimetype='application/pdf',
                     attachment_filename='result.pdf',
                     as_attachment=True)


if __name__ == '__main__':
    # createDB()
    app.run(debug=True)
