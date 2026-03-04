import pandas as pd
import itertools

def explore(data_file, work_directory):
    """Combination is too big"""

    # load data
    df = pd.read_csv(data_file)
    cols = list(df.keys())[0:-1]

    for order in itertools.permutations(cols):

        # create dataframe
        new_order = list(order)
        new_order.append('LABEL')
        df = df[new_order]

        # extract 

if __name__ == "__main__":

    explore("data/toy/test.csv")
    
