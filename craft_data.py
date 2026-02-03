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

                
def add_label(data_file:str, manifest:str, label, output_file:str):
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
    

def craft_log_normalize_data(tpm_data_file:str, output_file:str):
    """Cleaning & supposed to be more spectral analysis friendly"""

    # load data
    df = pd.read_csv(tpm_data_file)
    df = df.set_index("Ensembl_ID")

    # log2 transformation
    X = np.log2(df + 1)

    # centrage
    X = X.sub(X.mean(axis=1), axis=0)

    # save
    X.to_csv(output_file)


def craft_tcga_phenotype_dataset(output_folder):
    """ """

    # target label list
    target_list = [
        "sample",
        "disease_type",
        "race.demographic",
        "gender.demographic",
        "vital_status.demographic",
        "code.tissue_source_site",
        "name.tissue_source_site",
        "synchronous_malignancy.diagnoses",
        "ajcc_pathologic_stage.diagnoses",
        "primary_diagnosis.diagnoses",
        "prior_malignancy.diagnoses",
        "prior_treatment.diagnoses",
        "ajcc_pathologic_t.diagnoses",
        "ajcc_pathologic_n.diagnoses",
        "ajcc_pathologic_m.diagnoses",
        "icd_10_code.diagnoses",
        "tumor_descriptor.samples",
        "sample_type.samples",
        "specimen_type.samples",
        "tissue_type.samples"
    ]

    # load manifest
    df = pd.read_csv("data/TCGA/TCGA_BRCA_phenotype.csv")
    df = df[target_list]

    # compute PSD total energy
    craft_psd_total_energy_data(f"{output_folder}/signals", f"{output_folder}/data/total_energy.csv")

    # init folder
    if not os.path.isdir(f"{output_folder}/data/phenotype"):
        os.mkdir(f"{output_folder}/data/phenotype")

    # reload data
    df_data = pd.read_csv(f"{output_folder}/data/total_energy.csv")
    for target in target_list[1:-1]:

        df_label = df[['sample', target]]
        df_pheno = df_data

        id_to_label = {}
        for index, row in df_label.iterrows():
            i = row['sample']
            label = row[target]
            id_to_label[i] = label
        df_pheno['LABEL'] = df_pheno['ID'].replace(id_to_label)

        # save
        df_pheno.to_csv(f"{output_folder}/data/phenotype/total_energy_{target.replace('.', '_')}.csv", index=False)

if __name__ == "__main__":
    
    
    # craft_psd_total_energy_data("data/GSE83687/signals", "data/GSE83687/totalenergy.csv")
    # add_label("data/GSE83687/totalenergy.csv", "data/GSE83687/manifest.csv", "clinical condition", "data/GSE83687/totalenergy_labeled.csv")
    # craft_log_normalize_data("data/TCGA/TCGA_BRCA_tpm.csv", "data/TCGA/TCGA_BRCA_tpm_lognorm.csv")
    craft_tcga_phenotype_dataset("data/test_tcga")
