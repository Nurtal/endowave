import polars as pl
import numpy as np
import random


def build_random_order(data_file:str) -> dict:
    """Compute a random order and random distances for data_file

    Args:
        - data_file (str) path to the data file (should be .csv)

    Returns:
        - (dict) : results with two keys : order and positions
    
    """

    # params
    min_dist = 1
    max_dist = 3

    # load data
    df = pl.read_csv(data_file)

    # create random gene order
    gene_list = []
    for c in list(df.columns):
        if c not in ['LABEL', 'ID', '__index_level_0__', 'Unnamed: 0']:
            gene_list.append(c)
    gene_list = np.random.permutation(gene_list)

    # create position random distances
    positions = [0] 
    distances = [random.randint(min_dist, max_dist) for _ in range(len(gene_list) - 1)]
    for d in distances:
        positions.append(positions[-1] + d)

    return {'order':gene_list, 'positions':positions}




if __name__ == "__main__":

    m = build_random_order("data/modules/MSigDB_Hallmark/Apoptosis.csv")
    
