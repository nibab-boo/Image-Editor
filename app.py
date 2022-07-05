from flask import Flask, render_template, request, redirect, url_for,after_this_request, send_file
from PIL import Image, ImageFilter
from werkzeug.utils import secure_filename
# from tempfile import NamedTemporaryFile
# from shutil import copyfileobj
import os
# Configure application
app = Flask(__name__)

UPLOAD_FOLDER = os.getcwd() + '/static'
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024

@app.route("/")
def index():
  # return "HELLLO WORLD"
  return render_template("index.html")


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/image", methods = ["POST", "GET"])
def blur():

  # if no photo key on form
  if 'photo' not in request.files:
    return redirect("/")

  photo = request.files["photo"]

  # if no photo
  if photo.filename == "":
    return redirect("/")

  if photo and allowed_file(photo.filename):
    filename = secure_filename(photo.filename)
    img = Image.open(photo)
    img = img.convert('L')
    img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('output', name=filename))

@app.route("/output/<name>")
def output(name):
  filepath = os.path.join(app.config['UPLOAD_FOLDER'], name)
  if os.path.isfile(filepath):
    return render_template("output.html", filepath=filepath, name=name)

  return redirect("/")


@app.route('/uploads/<name>')
def download_file(name):
    filepath = os.path.join(UPLOAD_FOLDER, name)
    if not os.path.isfile(filepath):
      redirect("/")
    @after_this_request
    def remove_file(response):
      os.remove(filepath)
      return response
    return send_file(filepath, as_attachment=True)


@app.route("/delete/<name>")
def delete_file(name):
  filepath = os.path.join(UPLOAD_FOLDER, name)
  if os.path.isfile (filepath):
    os.remove(filepath)
  return redirect("/")
