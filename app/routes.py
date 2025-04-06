from app import app
from app.utils import fetch_geo_datasets
from app.utils import cluster_datasets

from flask import request
from flask import render_template
from flask import jsonify


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    pmid_file = request.files['file']
    pmids = [line.strip() for line in pmid_file.read().decode('utf-8').splitlines() if line.strip()]
    datasets = fetch_geo_datasets(pmids, app.config['BATCH_SIZE'])
    clustered = cluster_datasets(datasets)
    return jsonify(clustered)
