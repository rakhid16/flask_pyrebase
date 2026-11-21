from flask import Flask, redirect, render_template, request, url_for
from pyrebase import initialize_app

app = Flask(__name__)

FIREBASE_CONFIG = {
    "apiKey": "rahasia",
    "authDomain": "rahasia",
    "databaseURL": "rahasia",
    "projectId": "rahasia",
    "storageBucket": "rahasia",
    "messagingSenderId": "rahasia",
    "appId": "rahasia",
}

database = initialize_app(FIREBASE_CONFIG).database()


@app.route("/")
def index():
    records = database.child("").get().val()
    if records is None:
        records = {"-": {"nama": "-", "jurusan": "-"}}

    return render_template("index.html", data=records)


@app.route("/tambah-data", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        student_id = request.form["id"]
        if database.child(student_id).get().val() is not None:
            return (
                "NPM sudah ada, silakan masukkan data yang lain."
                '<br><br><a href="/tambah-data">Kembali</a>'
            )

        database.child(student_id).set(
            {
                "nama": request.form["nama"],
                "jurusan": request.form["jurusan"],
            }
        )
        return redirect(url_for("index"))

    return render_template("tambah.html")


@app.route("/edit/<student_id>", methods=["GET", "POST"])
def edit(student_id):
    if request.method == "POST":
        database.child(student_id).update(
            {
                "nama": request.form["nama"],
                "jurusan": request.form["jurusan"],
            }
        )
        return redirect(url_for("index"))

    record = database.child(student_id).get().val()
    if record is None:
        return redirect(url_for("index"))

    return render_template("edit.html", id=student_id, data=record)


@app.route("/hapus/<student_id>")
def hapus(student_id):
    database.child(student_id).remove()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
