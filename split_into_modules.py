import pandas as pd
import gseapy as gp
import os



def split_vst_into_hallmark_module(input_file, output_dir):
    """ """

    # init output_dir
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # load data
    df = pd.read_csv(input_file)

    # download hallmark genes
    hallmark = gp.get_library(name="MSigDB_Hallmark_2020", organism="Human")

    # split original data
    for module_name, gene_list in hallmark.items():

        # garder seulement les gènes présents dans ton dataset
        genes_in_df = [g for g in gene_list if g in df.columns]

        if len(genes_in_df) == 0:
            continue  # skipper les modules sans gènes trouvés

        # select subset
        target_cols = ['ID'] + genes_in_df
        sub_df = df[target_cols]

        # save
        save_name = f"{output_dir}/{module_name.replace(' ', '_').replace('-', '_').replace('/', '_')}.csv" 
        sub_df.to_csv(save_name, index=False)



if __name__ == "__main__":

    split_vst_into_hallmark_module("data/GSE152004/vst_reformated.csv", "data/modules/MSigDB_Hallmark")
