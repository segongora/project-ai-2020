import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/addinfected")
def addinfected():
    return render_template("addinfected.html")


@app.route("/add", methods=["POST"])
def add():
    return ""


@app.route("/spotted")
def spotted():
    return render_template("spotted.html")


if __name__ == '__main__':
    app.run()
