# GEO Dataset Insights from PMIDs

This web service allows users to upload a file of PubMed IDs, fetch associated GEO datasets using the e-utils API, and visualize their semantic similarity via clustering based on TF-IDF vectorization of metadata fields.

## Installation & Usage

1. Clone the repository:
```
git clone https://github.com/dec0dedd/paper-insights.git
cd paper-insights
```

2. (Optional) Create a virtual environment (e.g. with `venv` or `conda`) and activate it:
```
conda create -n paper-insights python=3.10
conda activate paper-insights
```

3. Install necessary requirements:
```
pip install -r requirements.txt
```

4. Configure the application:
- open `app/Config.py` and adjust the configuration parameters if necessary

5. Run the Flask app:
```
python run.py
```

and access the web service at http://127.0.0.1:5000/.