from flask import Flask, redirect, render_template, request, url_for
from pyrebase import initialize_app
from werkzeug.utils import secure_filename

app = Flask(__name__)

FIREBASE_CONFIG = {
    "apiKey": "rahasia",
    "authDomain": "rahasia",
    "databaseURL": "rahasia",
    "projectId": "rahasia",
    "storageBucket": "rahasia",
    "messagingSenderId": "rahasia",
    "appId": "rahasia",
    "serviceAccount": "firebase_key.json",
}

storage = initialize_app(FIREBASE_CONFIG).storage()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files["gambar"]
        safe_file_name = secure_filename(uploaded_file.filename)
        storage.child(safe_file_name).put(uploaded_file)
        return redirect(url_for("index"))

    file_names = [file.name for file in storage.child("").list_files()]
    return render_template("index.html", data=file_names)


@app.route("/lihat/<file_name>")
def lihat(file_name):
    image_url = storage.child(file_name).get_url(None)
    return render_template("lihat.html", image_url=image_url)


@app.route("/unduh/<file_name>")
def unduh(file_name):
    storage.child(file_name).download(file_name)
    return redirect(url_for("index"))


@app.route("/hapus/<file_name>")
def hapus(file_name):
    storage.delete(file_name)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
