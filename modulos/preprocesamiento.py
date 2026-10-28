from scipy.signal import butter, sosfiltfilt
import pandas as pd
import numpy as np
from pathlib import Path

def cargar_ECG_offline(codigo, fs):

  path = Path(f"registros/{codigo}.txt")
  df = pd.read_csv(path, sep=r"\s+", header=None, names=["voltaje", "tiempo", "raw"])

  df = df.drop(columns=["raw"]) #saco columna de datos crudos
  df = df.drop(columns=["tiempo"]) #saco el tiempo porque lo recontruyo luego con fs

  df["voltaje"] = pd.to_numeric(df["voltaje"], errors="coerce") #convierto a numerico
  df = df.dropna(subset=["voltaje"]).reset_index(drop=True) #elimino datos faltantes y reseto el índice

  df['tiempo']= np.arange(len(df)) / fs #genero el eje temporal con la frecuencia de muestreo

  return df

def filtroPB(fs, ecg):

    f1, f2, orden = 0.5, 40, 3

    # Pasabanda Butterworth
    sos = butter(N=orden, Wn=[f1, f2], btype="bandpass", fs=fs, output="sos")
    ecg_limpio = sosfiltfilt(sos, ecg)
    
    return ecg_limpio