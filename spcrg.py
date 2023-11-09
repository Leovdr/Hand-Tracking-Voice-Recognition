import speech_recognition as sr
import pyttsx3

# Inisialisasi recognizer
recognizer = sr.Recognizer()

# Inisialisasi engine TTS
engine = pyttsx3.init()

# Menggunakan mikrofon sebagai sumber suara
with sr.Microphone() as source:
    print("Silakan bicara...")
    recognizer.adjust_for_ambient_noise(source)  # Mengatur tingkat kebisingan latar
    audio = recognizer.listen(source)

try:
    recognized_text = recognizer.recognize_sphinx(audio)
    print("Anda mengatakan: " + recognized_text)
    
    # Memainkan teks hasil pengenalan suara sebagai suara
    engine.say("Anda mengatakan: " + recognized_text)
    engine.runAndWait()

except sr.UnknownValueError:
    print("Tidak dapat mengenali suara")
except sr.RequestError as e:
    print("Error pada permintaan suara: {0}".format(e))
