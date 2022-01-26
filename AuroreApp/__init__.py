# Create the app
from flask import Flask
from AuroreApp.models.sql_aurore import AuroreSQL
from AuroreApp.dataclasses import aurore_dataclasses

app = Flask(__name__)

import AuroreApp.routes
