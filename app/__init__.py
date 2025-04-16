from flask import Flask

app = Flask(__name__)
metrics = PrometheusMetrics(app)

from app import routes
