from flask import Flask

app = Flask(__name__)
app.config.from_object('dx_app.config')

import dx_app.views