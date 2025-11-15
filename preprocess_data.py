import pandas as pd
import mygene


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




if __name__ == "__main__":

    reformat_vst("data/GSE152004/vst.csv", "data/GSE152004/vst_reformated.csv")
