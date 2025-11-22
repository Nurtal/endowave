import pandas as pd
import glob
import os
import compute_psd

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

                



if __name__ == "__main__":
    
    
    craft_psd_total_energy_data("data/signals", "data/totalenergy.csv")
