import numpy as np
import pandas as pd
from kymatio.numpy import Scattering1D

def scattering_transform_dataframe(data_file, result_file, J=3, Q=8):
    """
    Applique la scattering transform 1D à chaque patient.
    
    J = profondeur (échelle maximale)
    Q = nombre d'ondelettes par octave
    """

    # load data
    df = pd.read_csv(data_file)
    X = df.iloc[:, :-1].values
    labels = df.iloc[:, -1].values
    n_samples, n_features = X.shape
    
    # La taille doit être une puissance de 2
    N = int(2**np.ceil(np.log2(n_features)))
    
    scattering = Scattering1D(J=J, shape=N, Q=Q)
    
    features = []
    
    for i in range(n_samples):
        signal = X[i]
        
        # padding si nécessaire
        padded = np.zeros(N)
        padded[:n_features] = signal
        
        Sx = scattering(padded)
        features.append(Sx.flatten())
    

    # craft dataframe
    scat_features = np.array(features)
    scat_df = pd.DataFrame(
        scat_features,
        columns=[f"scat_{i}" for i in range(scat_features.shape[1])]
    )
    scat_df["LABEL"] = labels

    # save dataframe
    scat_df.to_csv(result_file, index=False)



if __name__ == "__main__":

    scattering_transform_dataframe("data/toy/test.csv", "data/toy/test_scat.csv")
    
