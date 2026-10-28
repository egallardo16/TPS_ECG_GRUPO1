from modulos.preprocesamiento import *
from modulos.procesamiento import *
from modulos.visualizacion import *

#constantes
fs=100
registros = ["VP03","VP05", "VP06","VP27","VP33"]

#el registro 27 tiene un artefacto de movimiento entre 1875 
#y 1880. tambien hay algo raro entre 202 y 203.
#entre 184,5 y 185,5 la onda p se tapa por una caida de voltaje?
#entre 974 y 975 esta raro
#cargo datos
datos3 = cargar_ECG_offline(registros[3], fs)
ecg = datos3['voltaje']

#preproceso
ecg_limpio = filtroPB(fs, ecg)

#detecto picos R
ecg_integrado, ecg_filtrado = panTompkins(fs, ecg_limpio)
picosR = detectar_qrs(fs, ecg_integrado, ecg_filtrado)

#grafico 
graficar_ecg(ecg, fs, 1540, 1560, "crimson", titulo="ECG sin procesar")
graficar_ecg(ecg_limpio, fs, 1540, 1560, "crimson",picosR, "ECG limpio")
graficar_ecg(ecg_integrado, fs, 1540, 1560, "olive",None, "ECG procesado por Pan-Tompkins") 
#la amplitud de el ultimo grafico en realidad seria mv^2
graficar_tacograma(picosR, fs, 1540, 1560, "red", True, "Tacograma")

ectopicos, etiquetas, latidos = clasificar_ectopicos(picosR, fs)
print(f"{len(ectopicos)} latidos sospechosos de {len(latidos)}")

validos, corr = correlacion_latidos(ecg_limpio, picosR, fs, vecinos=15)
graficar_correlacion(validos, corr, fs, color="olive")

graficar_ecg(ecg_limpio, fs, 1870, 1890, "crimson",picosR, "Parte con artefacto") #se pierde pico R
graficar_ecg(ecg_limpio, fs, 970, 980, "crimson",picosR, "Parte con artefacto") #se pierde onda p
graficar_ecg(ecg_limpio, fs, 180, 190, "crimson",picosR, "Parte con artefacto") #se pierde onda p