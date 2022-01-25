from flask import Flask, request, render_template

from AuroreApp import app


@app.route("/", methods=["GET"])
def home_page():
    print("test")
    return render_template("index.html")
