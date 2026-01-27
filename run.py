import download_data
import compute_vst
import preprocess_data
import split_into_modules
import compute_gene_order
import craft_signal
import craft_data
import compute_fft
import compute_psd
import os
import glob
import pandas as pd
import run_xgboost

def run_allergy():
    """Run the entire fucking project on allergy dataset"""

    # download data
    download_data.download_small_allergy()

    # compute vst
    compute_vst.compute_vst_approximation("data/GSE152004/raw_counts.tsv.gz", "data/GSE152004/vst.csv")

    # preprocess & clean
    preprocess_data.reformat_vst("data/GSE152004/vst.csv", "data/GSE152004/vst_reformated.csv")

    # split into module
    if not os.path.isdir("data/modules"):
        os.mkdir("data/modules")
    split_into_modules.split_vst_into_hallmark_module("data/GSE152004/vst_reformated.csv", "data/modules/MSigDB_Hallmark")

    # turn into signals
    if not os.path.isdir("data/signals"):
        os.mkdir("data/signals")
    for module in glob.glob("data/modules/MSigDB_Hallmark/*.csv"):
        module_name = module.split("/")[-1].replace('.csv', '')

        if not os.path.isdir(f"data/signals/{module_name}"):
            os.mkdir(f"data/signals/{module_name}")

        config = compute_gene_order.build_random_order(module)
        craft_signal.write_freq(module, config['order'], config['positions'], f"data/signals/{module_name}")

        for signal_file in glob.glob(f"data/signals/{module_name}/*.csv"): 

            # compute FFT
            freqs, amplitude = compute_fft.compute_fft(signal_file)
            df_fft = pd.DataFrame({"x":freqs, "y":amplitude})
            df_fft.to_csv(signal_file.replace(".csv", "_fft.csv"), index=False)

            # compute PSD
            freqs, psd = compute_psd.compute_welch(signal_file) 
            df_psd = pd.DataFrame({"x":freqs, "y":psd})
            df_psd.to_csv(signal_file.replace(".csv", "_psd.csv"), index=False)



def run_immune(output_dir):
    """Run the entire GSE83687 dataset"""

    # init output dir
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    os.mkdir(f"{output_dir}/data")
    os.mkdir(f"{output_dir}/signals")
    os.mkdir(f"{output_dir}/modules")

    # download data
    download_data.download_GSE83687(f"{output_dir}/data")
    download_data.download_GSE83687_metadata(f"{output_dir}/data")

    # compute vst
    compute_vst.compute_vst_approximation(f"{output_dir}/data/raw_counts.tsv.gz", f"{output_dir}/data/vst.csv")

    # preprocess & clean
    preprocess_data.reformat_vst(f"{output_dir}/data/vst.csv", f"{output_dir}/data/vst_reformated.csv")

    # split into module
    if not os.path.isdir(f"{output_dir}/modules"):
        os.mkdir(f"{output_dir}/modules")
    split_into_modules.split_vst_into_hallmark_module(f"{output_dir}/data/vst_reformated.csv", f"{output_dir}/modules/MSigDB_Hallmark")

    # turn into signals
    if not os.path.isdir(f"{output_dir}/signals"):
        os.mkdir(f"{output_dir}/signals")
    for module in glob.glob(f"{output_dir}/modules/MSigDB_Hallmark/*.csv"):
        module_name = module.split("/")[-1].replace('.csv', '')

        if not os.path.isdir(f"{output_dir}/signals/{module_name}"):
            os.mkdir(f"{output_dir}/signals/{module_name}")

        config = compute_gene_order.build_random_order(module)
        craft_signal.write_freq(module, config['order'], config['positions'], f"{output_dir}/signals/{module_name}")

        for signal_file in glob.glob(f"{output_dir}/signals/{module_name}/*.csv"): 

            # compute FFT
            freqs, amplitude = compute_fft.compute_fft(signal_file)
            df_fft = pd.DataFrame({"x":freqs, "y":amplitude})
            df_fft.to_csv(signal_file.replace(".csv", "_fft.csv"), index=False)

            # compute PSD
            freqs, psd = compute_psd.compute_welch(signal_file) 
            df_psd = pd.DataFrame({"x":freqs, "y":psd})
            df_psd.to_csv(signal_file.replace(".csv", "_psd.csv"), index=False)

    # craft data
    preprocess_data.extract_labels_from_matrix(f"{output_dir}/data/matrix.txt.gz", f"{output_dir}/data/manifest.csv")
    craft_data.craft_psd_total_energy_data(f"{output_dir}/signals", f"{output_dir}/data/totalenergy.csv")
    craft_data.add_label(f"{output_dir}/data/totalenergy.csv", f"{output_dir}/data/manifest.csv", "clinical condition", f"{output_dir}/data/totalenergy_labeled.csv")

    # run clf
    results = run_xgboost.train_xgboost_multiclass(f"{output_dir}/data/totalenergy_labeled.csv", test_size=0.3)
    print("F1 macro (test) :", results["f1_test_macro"])
    print("Cross-val :", results["cv_scores_macro"])
    print("Moyenne CV :", results["cv_mean_macro"])




def run_tcga_pheno(output_dir):
    """ """

    # init output dir [ok]
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
        os.mkdir(f"{output_dir}/data")
        os.mkdir(f"{output_dir}/signals")
        os.mkdir(f"{output_dir}/modules")

    # download data [ok]
    # download_data.download_tcga_data(f"{output_dir}/data")

    # normalize data [ok]
    # craft_data.craft_log_normalize_data(f"{output_dir}/data/TCGA_BRCA_tpm.csv", f"{output_dir}/data/TCGA_BRCA_tpm_lognorm.csv")

    # split into module
    split_into_modules.split_vst_into_hallmark_module(f"{output_dir}/data/TCGA_BRCA_tpm_lognorm.csv", f"{output_dir}/modules/MSigDB_Hallmark")






if __name__ == "__main__":

    # run_immune("data/explore/immue_wave")

    run_tcga_pheno("data/test_tcga")
    
