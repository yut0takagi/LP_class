from flask import Flask,render_template
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


app = Flask(__name__)

@app.route('/')
def login_form():
    return render_template("main.html")



