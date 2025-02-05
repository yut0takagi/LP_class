from flask import Flask
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


app = Flask(__name__)




@app.route('/')
def hello_world():
    return 'Hello World!'
