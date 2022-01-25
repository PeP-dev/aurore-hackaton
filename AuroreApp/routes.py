from flask import Flask, request, render_template, app


@app.route("/")
def home_page():
    return render_template("index.html")
