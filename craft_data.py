import pandas as pd
import glob
import os
import compute_psd
import numpy as np

def craft_psd_total_energy_data(signal_folder:str, output_file:str):
    """ """

    data = {}
    for folder in glob.glob(f"{signal_folder}/*"):

        if os.path.isdir(folder):
            pathway = folder.split("/")[-1]

            for signal_file in glob.glob(f"{folder}/*_freq.csv"):
                
                sample_id = signal_file.split("/")[-1].replace("_freq.csv", "")
                total_energy = compute_psd.compute_total_energy(signal_file)

                if sample_id not in data:
                    data[sample_id] = {"ID":sample_id}
                data[sample_id][pathway] = total_energy

    # craft dataframe
    data = list(data.values())
    df = pd.DataFrame(data)

    # save dataframe
    df.to_csv(output_file, index=False)

                
def add_label(data_file, manifest, label, output_file):
    """ """

    # load data
    df = pd.read_csv(data_file)
    df_manifest = pd.read_csv(manifest)

    # check for labels
    id_to_label = {}
    for index, row in df_manifest.iterrows():
        id_to_label[row['ID']] = row[label]
    for i in list(df['ID']):
        if i not in id_to_label:
            id_to_label[i] = np.nan
    
    # add labels & drop unlabeled
    df['LABEL'] = df['ID'].replace(id_to_label)
    df = df.dropna()

    # save
    df.to_csv(output_file, index=False)
    



if __name__ == "__main__":
    
    
    # craft_psd_total_energy_data("data/GSE83687/signals", "data/GSE83687/totalenergy.csv")
    add_label("data/GSE83687/totalenergy.csv", "data/GSE83687/manifest.csv", "clinical condition", "data/GSE83687/totalenergy_labeled.csv")
