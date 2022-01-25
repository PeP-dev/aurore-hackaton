from flask import Flask, request, render_template

from AuroreApp import app


@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html")

@app.route("/faq", methods=["GET"])
def faq():
    return render_template("faq.html")

@app.route("/pro", methods=["GET"])
def pro():
    return render_template("faq.html")

@app.route("/particulier", methods=["GET"])
def particulier():
    return render_template("faq.html")
