from flask import Flask, request, render_template, app


@app.route("/")
def home_page():
    render_template("index.html")
