import requests
from tqdm import tqdm
import os

def download_small_allergy():
    """Trigger the download of GSE152004 dataset
    """

    # prepare output folder
    if not os.path.isdir("data"):
        os.mkdir("data")
    if not os.path.isdir("data/GSE152004"):
        os.mkdir("data/GSE152004")

    # download raw counts
    url = "https://www.ncbi.nlm.nih.gov/geo/download/?type=rnaseq_counts&acc=GSE152004&format=file&file=GSE152004_raw_counts_GRCh38.p13_NCBI.tsv.gz"
    output = "data/GSE152004/raw_counts.tsv.gz"
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    with open(output, "wb") as f, tqdm(
        desc=output,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            bar.update(size)




def download_GSE83687():
    """Trigger the download of GSE83687 dataset
    """

    # prepare output folder
    if not os.path.isdir("data"):
        os.mkdir("data")
    if not os.path.isdir("data/GSE83687"):
        os.mkdir("data/GSE83687")

    # download raw counts
    url = "https://www.ncbi.nlm.nih.gov/geo/download/?type=rnaseq_counts&acc=GSE83687&format=file&file=GSE83687_raw_counts_GRCh38.p13_NCBI.tsv.gz"
    output = "data/GSE83687/raw_counts.tsv.gz"
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    with open(output, "wb") as f, tqdm(
        desc=output,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            bar.update(size)


def download_GSE83687_metadata():
    """Trigger the download of GSE83687 matrix file containing label
    """

    # prepare output folder
    if not os.path.isdir("data"):
        os.mkdir("data")
    if not os.path.isdir("data/GSE83687"):
        os.mkdir("data/GSE83687")

    # download matrix
    url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE83nnn/GSE83687/matrix/GSE83687_series_matrix.txt.gz"
    output = "data/GSE83687/matrix.txt.gz"
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    with open(output, "wb") as f, tqdm(
        desc=output,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            bar.update(size)
        
if __name__ == "__main__":

    # download_small_allergy()
    # download_GSE83687()
    download_GSE83687_metadata()
