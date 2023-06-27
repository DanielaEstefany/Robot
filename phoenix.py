import pyaudio
from pocketsphinx import Pocketsphinx

# Configura la ruta al archivo de modelo de lenguaje
language_model_path = "ruta_al_archivo/es-es.lm.bin"

# Configura la ruta al archivo de diccionario
dictionary_path = "ruta_al_archivo/es.dict"

# Configura los parámetros del reconocimiento de voz
config = {
    "hmm": "C:/Users/MSI SWORD 15/Documents/Proyectos python/Python/sphinx4-5prealpha-src/sphinx4-data/src/main/resources/edu/cmu/sphinx/models/en-us/en-us/mdef",
    "lm": 'C:/Users/MSI SWORD 15/Documents/Proyectos python/Python/es/es-20k.lm',
    "dict": 'C:/Users/MSI SWORD 15/Documents/Proyectos python/Python/es/es.dict'
}

# Crea el objeto de reconocimiento de voz
recognizer = Pocketsphinx(**config)

# Inicializa PyAudio
audio = pyaudio.PyAudio()

# Configura los parámetros de grabación de audio
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

print("Escuchando...")

# Captura y transcribe el audio en tiempo real
while True:
    data = stream.read(1024)
    recognizer.process_raw(data, False, False)

    # Obtén el resultado del reconocimiento de voz
    result = recognizer.get_hyp()

    # Imprime el texto transcritO
    if result:
        print("Texto transcritO:", result.hypstr)

# Detén la grabación y cierra los recursos
stream.stop_stream()
stream.close()
audio.terminate()