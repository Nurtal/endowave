import pandas as pd
import numpy as np
from scipy.stats import gmean


def compute_vst_approximation(input_file, output_file):
    """Compute une approximation, le vrai vst require R et c'est de la merde """ 

    # Charger le fichier counts.tsv.gz
    counts = pd.read_csv(input_file, sep='\t', index_col=0, compression='gzip')
    print("Counts shape:", counts.shape)

    # Filtrer gènes très faibles si besoin
    min_total_counts = 10
    counts = counts.loc[counts.sum(axis=1) >= min_total_counts]

    # stimation des size factors (méthode median ratio)
    def median_ratio_size_factors(counts_df):
        # Moyenne géométrique par gène
        gm = counts_df.replace(0, np.nan).apply(lambda x: gmean(x.dropna()), axis=1)
        gm[gm == 0] = np.nan  # éviter division par 0
        ratios = counts_df.div(gm, axis=0)
        size_factors = ratios.median(axis=0, skipna=True)
        return size_factors

    size_factors = median_ratio_size_factors(counts)

    # Normalisation + log2 transform (VST approx)
    norm_counts = counts.div(size_factors, axis=1)
    vst_approx = np.log2(norm_counts + 1.0)

    # save
    print(vst_approx)
    vst_approx.to_csv(output_file)




if __name__ == "__main__":

    compute_vst_approximation("data/GSE152004/raw_counts.tsv.gz", "data/GSE152004/vst.csv")
    

