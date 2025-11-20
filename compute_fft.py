import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def compute_fft(signal_file):
    """ """

    # Charger le CSV (adapter le nom du fichier)
    df = pd.read_csv(signal_file)

    x = df["x"].values
    y = df["y"].values

    # Calcul de la fréquence d’échantillonnage
    dx = x[1] - x[0]          # pas d’échantillonnage
    fs = 1 / dx               # fréquence d’échantillonnage

    # Calcul FFT
    N = len(y)
    Y = np.fft.fft(y)
    freqs = np.fft.fftfreq(N, d=dx)

    # On garde seulement la partie positive
    idx = np.where(freqs >= 0)
    freqs_pos = freqs[idx]
    Y_pos = np.abs(Y[idx])

    return freqs_pos, Y_pos




if __name__ == "__main__":

    m = compute_fft("data/signals/Adipogenesis/GSM4594795_freq.csv")
    print(m)
