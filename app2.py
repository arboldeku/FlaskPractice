from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os

EXTENSIONES = ["png", "jpg", "jpeg"]
app = Flask (__name__)
app.config