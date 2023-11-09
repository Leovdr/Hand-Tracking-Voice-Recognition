import speech_recognition as sr
import pyttsx3

# Inisialisasi recognizer
recognizer = sr.Recognizer()

# Inisialisasi engine TTS
engine = pyttsx3.init()

# Menggunakan mikrofon sebagai sumber suara
with sr.Microphone() as source:
    print("Silakan bicara...")
    audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio)
        print("Anda mengatakan: " + recognized_text)

        if "hello" in recognized_text:
            response_text = "Halo! Bagaimana saya dapat membantu Anda?"
        elif "Terima kasih" in recognized_text:
            response_text = "Tidak masalah. Semoga harimu menyenangkan."
        else:
            response_text = "Saya tidak mengerti apa yang Anda katakan."

        print("Respons: " + response_text)

        # Memainkan respons suara
        engine.say(response_text)
        engine.runAndWait()

    except sr.UnknownValueError:
        print("Tidak dapat mengenali suara")
    except sr.RequestError as e:
        print("Error pada permintaan suara: {0}".format(e))
