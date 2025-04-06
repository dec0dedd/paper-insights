from app import app

import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np


def fetch_geo_datasets(pmids, batch_size):
    """Fetches GSE IDs via e-utils API"""
    all_datasets = []
    gse_to_pmid = {}

    for i in range(0, len(pmids), batch_size):
        batch_pmids = pmids[i:i+batch_size]
        ids_str = ",".join(batch_pmids)
        link_url = app.config['PUBMED_GDS_API_URL'] + f"&id={ids_str}&retmode=json"
        res = requests.get(link_url)
        link_data = res.json()

        for linkset in link_data.get('linksets', []):
            this_pmid = linkset.get('ids', [None])[0]
            if not this_pmid:
                continue
            for linksetdb in linkset.get('linksetdbs', []):
                for gse_id in linksetdb.get('links', []):
                    gse_to_pmid[gse_id] = this_pmid

    gse_ids = list(gse_to_pmid.keys())
    metadata_map = fetch_geo_metadata_batch(gse_ids, batch_size)

    for gse_id, meta in metadata_map.items():
        all_datasets.append({
            **meta,
            'pmid': gse_to_pmid[gse_id],
            'gse_id': gse_id
        })

    return all_datasets


def fetch_geo_metadata_batch(gse_ids, batch_size):
    """Fetches GEO metadata via e-utils API"""

    metadata = {}
    for i in range(0, len(gse_ids), batch_size):
        batch = gse_ids[i:i+batch_size]
        ids_str = ",".join(batch)
        url = app.config['PUBMED_METADATA_API_URL'] + f"&id={ids_str}&retmode=json"
        res = requests.get(url)
        result = res.json().get('result', {})

        for gse_id in batch:
            if gse_id not in result:
                continue
            data = result[gse_id]
            metadata[gse_id] = {
                'title': data.get('title', ''),
                'type': data.get('gdstype', ''),
                'summary': data.get('summary', ''),
                'organism': data.get('taxon', ''),
                'design': data.get('overall_design', '')
            }

    return metadata


def merge_metadata(metadata):
    """Function to merge dataset's metadata into one string"""
    return " ".join([
        metadata['title'], metadata['type'], metadata['summary'],
        metadata['organism'], metadata['design']
    ])


def cluster_datasets(datasets):
    texts = [merge_metadata(metadata) for metadata in datasets]

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(texts)

    # in case of only 1 vector  or all zero vectors return default data
    if X.shape[0] < 2 or np.all(X.toarray() == 0):
        return [{
            'x': 0.0,
            'y': 0.0,
            'label': 0,
            'pmid': d['pmid'],
            'gse_id': d['gse_id'],
            'title': d['title']
        } for d in datasets]

    # perform PCA to visualize data in 2D
    try:
        pca = PCA(n_components=app.config['NUM_OF_PCA_COMPONENTS'])
        reduced = pca.fit_transform(X.toarray())
    except Exception:
        reduced = X.toarray()[:, :app.config['NUM_OF_PCA_COMPONENTS']]

    n_clusters = max(
        1,
        min(app.config['MAX_NUM_OF_CLUSTERS'], len(np.unique(reduced, axis=0)))
    )

    kmeans = KMeans(n_clusters=n_clusters, n_init='auto')
    labels = kmeans.fit_predict(reduced)

    return [{
        'x': float(reduced[i][0]),
        'y': float(reduced[i][1]),
        'label': int(labels[i]),
        'pmid': datasets[i]['pmid'],
        'gse_id': datasets[i]['gse_id'],
        'title': datasets[i]['title']
    } for i in range(len(datasets))]
