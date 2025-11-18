
import os
import polars as pl
import compute_gene_order


def write_freq(data_file:str, order:list, positions:list, output_folder:str) -> None:
    """Write frequency files from a data_file

    Args:
        - data_file (str) : path to the csv file
        - order (list) : computed gene order
        - positions (list) : computed postions of the genes
        - output_folder (str) : path to the output folder
    
    """

    # check output folder
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    # load data
    df = pl.read_csv(data_file)
    for i in df['ID']:

        # extract values
        dft = df.filter(pl.col('ID') == i).drop(['ID'])
        dft = dft.select(order)
        vector = dft.to_numpy()[0]

        # write signal
        cmpt = 0
        output_file = open(f"{output_folder}/{i}_freq.csv", "w")
        output_file.write("x,y\n")
        for x in positions:
            output_file.write(f"{x},{vector[cmpt]}\n")
            cmpt+=1
        output_file.close()
        



if __name__ == "__main__":

    r = compute_gene_order.build_random_order("data/modules/MSigDB_Hallmark/Apoptosis.csv")

    write_freq("data/modules/MSigDB_Hallmark/Apoptosis.csv", r['order'], r['positions'], "data/signals")

