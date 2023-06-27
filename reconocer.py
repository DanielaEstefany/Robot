import speech_recognition as sr

# Crear un reconocedor de voz
recognizer = sr.Recognizer()

# Utilizar el micrófono como fuente de audio
with sr.Microphone() as source:
    print("Di algo...")
    audio = recognizer.listen(source, phrase_time_limit=5)  # Escuchar el audio del micrófono por un máximo de 3 segundos

    try:
        # Reconocer el texto utilizando el reconocedor de voz
        text = recognizer.recognize_google(audio, language="es")  # Puedes cambiar el idioma aquí

        print("Texto reconocido:")
        print(text)

    except sr.UnknownValueError:
        print("No se pudo reconocer el audio.")

    except sr.RequestError as e:
        print("Error al solicitar los resultados del reconocimiento de voz; {0}".format(e))