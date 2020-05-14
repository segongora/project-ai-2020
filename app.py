import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.utils import secure_filename
from facerecognition import findFace

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

sp=[]

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/addinfected")
def addinfected():
    people = db.execute("SELECT * FROM people")
    return render_template("addinfected.html", people=people)


@app.route("/add", methods=["POST"])
def add():
	if request.method == "POST":
		if request.files:
			name = request.form.get("name").title()
			phone = request.form.get("phone")
			file = request.files['image']

			if file and allowed_file(file.filename):
				if db.execute("SELECT * FROM people").rowcount == 0:
					filename = "1"
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
					db.execute("INSERT INTO people (name, phone, image) VALUES (:name, :phone, :image)", {"name": name, "phone": phone, "image": filename})
					db.commit()

					return redirect(url_for('addinfected'))

				filename = db.execute("SELECT * from people ORDER BY id DESC").fetchone()
				image_name = filename.id + 1
					#secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

				db.execute("INSERT INTO people (name, phone, image) VALUES (:name, :phone, :image)", {"name": name, "phone": phone, "image": image_name})
				db.commit()

			return redirect(url_for('addinfected'))

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/spotted")
def spotted():
	people = db.execute("SELECT * FROM people").fetchall()
	spot = session.get('people')

	return render_template("spotted.html", people=people, spot=spot)

@app.route("/facialrecognition/<string:id>")
def facialrecognition(id):
	url = 'https://sergio-ai-project.herokuapp.com/static/' + id + ".jpg"
	if findFace(url):
		session['spotted'] = db.execute("SELECT * FROM people WHERE id = :id", {"id": id}).fetchone()
		sp = session.get('people')
		sp.append(session.get('spotted'))
		session['people'] = sp

	return redirect(url_for('spotted'))

@app.route("/removespotted/<string:id>")
def removespotted(id):
	session['remove'] = db.execute("SELECT * FROM people WHERE id = :id", {"id": id}).fetchone()
	s = session.get('people')
	s.remove(session.get('remove'))
	session['people'] = s

	return redirect(url_for('spotted'))

@app.route("/img", methods=["GET"])
def images():
	pics = os.listdir('static/')
	return render_template("img.html", pics=pics)


if __name__ == '__main__':
    app.run()
