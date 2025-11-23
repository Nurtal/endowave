import pandas as pd
import mygene
import os
import re


def reformat_vst(data_file, output_file):
    """ """

    # load data
    df = pd.read_csv(data_file)
    df["GeneID"] = df["GeneID"].astype(str)

    # init mygene
    mg = mygene.MyGeneInfo()

    # Récupération des symboles (nom des gènes)
    gene_info = mg.querymany(df['GeneID'].tolist(),
                             scopes="entrezgene",
                             fields="symbol",
                             species="human")

    # Convertir en dictionnaire GeneID -> symbole
    mapping = {
        item["query"]: item.get("symbol", item["query"])
        for item in gene_info
    }

    # Rename genes
    df['GeneID'] = df['GeneID'].map(mapping)

    # Transposition
    df = df.rename(columns={'GeneID':'ID'})
    df.index = df['ID']
    df = df.drop(columns=['ID'])
    df = df.T
    
    # Reorder cols
    df['ID'] = df.index
    last_col = df.columns[-1]
    df = df[[last_col] + df.columns[:-1].tolist()]

    # save
    df.to_csv(output_file, index=False)



def extract_labels_from_matrix(matrix_file, manifest_file):
    """ """

    # decompress if needed
    uncompress_file = matrix_file.replace('.gz', '')
    if matrix_file.split(".")[-1] == "gz" and os.path.isfile(matrix_file):
        os.system(f"gunzip {matrix_file}")

    # parse
    vectors = {}
    data = open(uncompress_file, "r")
    for line in data:

        # catch GEO ID
        if re.search('Sample_geo_accession', line):
            array = line.rstrip().split("\t")[1:-1]
            array = [x.replace("\"", "") for x in array]
            vectors['ID'] = array

        # catch labels
        if re.search('Sample_characteristics_ch1', line):
            array = line.rstrip().split("\t")[1:-1]
            array = [x.replace("\"", "").replace("\\", "") for x in array]
            condition_name = array[0].split(":")[0]
            array = [x.replace(f"{condition_name}: ", '') for x in array]
            vectors[condition_name] = array
            
    data.close()

    # create and save manifest
    df = pd.DataFrame(vectors)
    df.to_csv(manifest_file, index=False)


if __name__ == "__main__":

    # reformat_vst("data/GSE152004/vst.csv", "data/GSE152004/vst_reformated.csv")
    extract_labels_from_matrix("data/GSE83687/matrix.txt.gz", "data/GSE83687/manifest.csv")
