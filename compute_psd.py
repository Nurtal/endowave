
import numpy as np
import pandas as pd
from scipy.signal import welch

def compute_welch(filename, nperseg=None, noverlap=None, window='hann'):
    """
    Calcule la PSD (méthode de Welch) à partir d'un fichier CSV contenant
    deux colonnes : x (temps) et y (signal).

    - filename : chemin du fichier CSV
    - nperseg  : taille de segment (None = auto)
    - noverlap : chevauchement entre segments (None = auto)
    - window   : fenêtre (hann, hamming, blackman…)

    Retourne :
        freqs  : fréquences (Hz)
        psd    : densité spectrale de puissance (unit^2/Hz)
    """

    # --- Lecture du CSV ---
    df = pd.read_csv(filename)
    x = df.iloc[:,0].values
    y = df.iloc[:,1].values

    # --- Calcul fréquence d'échantillonnage ---
    dx = x[1] - x[0]
    fs = 1.0 / dx

    # --- Welch ---
    freqs, psd = welch(
        y,
        fs=fs,
        window=window,
        nperseg=nperseg,
        noverlap=noverlap,
        scaling='density',
        detrend='constant'
    )

    return freqs, psd


def compute_total_energy(csv_path, nperseg=None, noverlap=None, window="hann"):
    """
    Calcule l'énergie totale du signal via sa PSD (méthode de Welch).
    Le CSV doit contenir deux colonnes : x (temps) et y (signal).
    """
    # Load CSV
    df = pd.read_csv(csv_path)
    x = df.iloc[:, 0].values
    y = df.iloc[:, 1].values

    # Sampling frequency
    dt = x[1] - x[0]
    fs = 1.0 / dt

    # PSD (Welch)
    freqs, psd = welch(
        y, fs=fs,
        window=window,
        nperseg=nperseg,
        noverlap=noverlap,
        scaling="density"
    )

    # Frequency resolution
    dfreq = freqs[1] - freqs[0]

    # Total energy = ∑ PSD(f) * Δf
    total_energy = np.sum(psd) * dfreq

    return total_energy



if __name__ == "__main__":

    freqs, psd = compute_welch("data/signals/Adipogenesis/GSM4594795_freq.csv")
    print(freqs)
    print(psd)
    m = compute_total_energy("data/signals/Adipogenesis/GSM4594795_freq.csv")
    print(m)
    

    
