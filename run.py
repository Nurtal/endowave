import download_data
import compute_vst
import preprocess_data
import split_into_modules
import compute_gene_order
import craft_signal
import compute_fft
import compute_psd
import os
import glob
import pandas as pd

def run():
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
            

if __name__ == "__main__":

    run()
    
