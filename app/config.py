class Config:
    PUBMED_GDS_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=gds&linkname=pubmed_gds"
    PUBMED_METADATA_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds"
    BATCH_SIZE = 200
    NUM_OF_PCA_COMPONENTS = 2
    MAX_NUM_OF_CLUSTERS = 5
