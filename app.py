from flask import Flask

from flask import redirect, url_for, request, render_template, send_file, flash
from io import BytesIO

from flask_wtf.file import FileField
from wtforms import SubmitField
from flask_wtf import FlaskForm

from PyPDF2 import PdfFileMerger
import sqlite3 as sql
import io
import sys

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret" # is necessary for Flask wtf


# class UploadFile(FlaskForm):
#     file = FileField()
#     submit = SubmitField("Submit!")
#     download = SubmitField("Download!")


# A simple sql database
def database_in(name, data):
    conn = sql.connect("database.db")
    cursor = conn.cursor()



    cursor.execute("CREATE TABLE IF NOT EXISTS new_table (name TEXT, data BLOB)")  # BLOB: Binary large object

    # Delete all existing items first
    cursor.execute("DELETE FROM new_table")

    # Add new items back up
    cursor.execute("INSERT INTO new_table (name, data) VALUES (?,?)", (name, data))

    conn.commit()
    cursor.close()
    conn.close()

#
@app.route('/', methods=["POST", "GET"]) # necessary for the url_for part in html file
def index():
    # form = UploadFile()

    if request.method == "POST":
        # if 'files[]' not in request.files:

        files = request.files.getlist("files[]")
        print("Found files!", file=sys.stderr)

        # Merge the two files and write it to ouput_files
        output_files = merger(files)

        # for file in files:
        #     database_in(name=file.filename, data=file.read())
        #     print(f"Successfully added: {file} to the database", file=sys.stderr)

        # return render_template("index.html", form=form)
        return render_template("index.html")
    else:
        # return render_template("index.html", form=form)
        return render_template("index.html")


# @app.route('/download_merged_file', methods=["POST", "GET"])
# def download_merged_file():
#
#     print("Onto the merging", file=sys.stderr)
#
#     if request.method == "POST":
#
#         # Get the two files
#         conn = sql.connect("database.db")
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM new_table")
#         input_files = list(cursor.fetchall())
#
#         conn.commit()
#         cursor.close()
#         conn.close()
#
#         # Call the function and parse input_files
#         output_file = merger(input_files)
#
#         # Put merged file to a download
#         return send_file(BytesIO(output_file), attachment_filename='merged.pdf', as_attachment=True)
#
#     return render_template("index.html")


# Get the files from database and merge
def merger(input_files):
    pdf_merger = PdfFileMerger()

    for file in input_files:
        print(f"File {file}")
        pdf_merger.append(file)

    with open('./result/merged.pdf', "wb") as f_out:
        pdf_merger.write(f_out)

    return f_out


if __name__ == '__main__':
    app.run()
