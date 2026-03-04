import pandas as pd
import numpy as np
import umap
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import os


def generate_umap(data_file:str, figure_file:str) -> None:
    """Generate a UMAP visualisation from a csv file

    Args:
        - data_file (str) : path to the input csv file (must colomn bust be LABEL)
        - figure_file (str) : name of the img saved in the images subfolder
    
    """

    # init output folder
    if not os.path.isdir('images'):
        os.mkdir('images')

    # parameters
    n_neighbors=15
    min_dist=0.1
    random_state=42

    # Charger le fichier
    df = pd.read_csv(data_file)
    
    #  Séparer features et labels
    X = df.iloc[:, :-1].values
    labels = df.iloc[:, -1].values

    # Normalize
    X = StandardScaler().fit_transform(X)
    
    # UMAP
    reducer = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        random_state=random_state
    )
    embedding = reducer.fit_transform(X)
    
    # Plot
    plt.figure(figsize=(8,6))
    unique_labels = np.unique(labels)
    for lab in unique_labels:
        idx = labels == lab
        plt.scatter(
            embedding[idx, 0],
            embedding[idx, 1],
            label=str(lab),
            alpha=0.7
        )
    plt.xlabel("UMAP1")
    plt.ylabel("UMAP2")
    plt.title("UMAP projection")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"images/{figure_file}")
    plt.close()


if __name__ == "__main__":

    generate_umap("data/toy/test.csv", "test.png")
    
