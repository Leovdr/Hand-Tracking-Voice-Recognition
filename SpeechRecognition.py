import wave
import sys
import pyaudio
import speech_recognition as sr
import RPi.GPIO as GPIO

#Konfigurasi record input
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 5
OUTPUT_FILE = 'output.wav'

# Tentukan pin GPIO yang terhubung dengan relay
RELAY_PIN_1 = 18
RELAY_PIN_2 = 27
RELAY_PIN_3 = 22
RELAY_PIN_4 = 23

# Konfigurasi GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN_1, GPIO.OUT)
GPIO.setup(RELAY_PIN_2, GPIO.OUT)
GPIO.setup(RELAY_PIN_3, GPIO.OUT)
GPIO.setup(RELAY_PIN_4, GPIO.OUT)

# Fungsi untuk melakukan transkripsi
def transcribe_audio(audio_file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)  # Merekam audio dari file

        try:
            # Menggunakan recognizer dengan bahasa Indonesia
            text = recognizer.recognize_google(audio_data, language='id-ID')
            print("Program menyatakan", text)

            # Menambahkan kondisi berdasarkan hasil transkripsi
            if 'nyalakan kipas' in text.lower():
                GPIO.output(RELAY_PIN_1, GPIO.HIGH)
                print("Kipas menyala.")
            elif 'matikan kipas' in text.lower():
                GPIO.output(RELAY_PIN_1, GPIO.LOW)
                print("Kipas mati.")
                
            if 'nyalakan lampu belakang' in text.lower():
                GPIO.output(RELAY_PIN_2, GPIO.HIGH)
                print("Lampu belakang menyala.")
            elif 'matikan lampu belakang' in text.lower():
                GPIO.output(RELAY_PIN_2, GPIO.LOW)
                print("Lampu belakang mati.")
                
            if 'nyalakan lampu depan' in text.lower():
                GPIO.output(RELAY_PIN_3, GPIO.HIGH)
                print("Lampu depan menyala.")
            elif 'matikan lampu depan' in text.lower():
                GPIO.output(RELAY_PIN_3, GPIO.LOW)
                print("Lampu depan mati.")
                
            if 'nyalakan lampu tengah' in text.lower():
                GPIO.output(RELAY_PIN_4, GPIO.HIGH)
                print("Lampu tengah menyala..")
            elif 'matikan lampu tengah' in text.lower():
                GPIO.output(RELAY_PIN_4, GPIO.LOW)
                print("Lampu tengah mati.")
                
            # Menambahkan kondisi untuk mematikan semua lampu
            if 'nyalakan semua lampu' in text.lower():
                GPIO.output(RELAY_PIN_2, GPIO.HIGH)
                GPIO.output(RELAY_PIN_3, GPIO.HIGH)
                GPIO.output(RELAY_PIN_4, GPIO.HIGH)
                print("Semua lampu dimatikan.")
            if 'matikan semua lampu' in text.lower():
                GPIO.output(RELAY_PIN_2, GPIO.LOW)
                GPIO.output(RELAY_PIN_3, GPIO.LOW)
                GPIO.output(RELAY_PIN_4, GPIO.LOW)
                print("Semua lampu dimatikan.")
                
        except sr.UnknownValueError:
            print("Google Web API tidak dapat mengenali audio")
        except sr.RequestError as e:
            print("Terjadi kesalahan pada Google Web API; {0}".format(e))

# Merekam suara
with wave.open(OUTPUT_FILE, 'wb') as wf:
    p = pyaudio.PyAudio()
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

    print('Katakan Sesuatu...')
    for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
        wf.writeframes(stream.read(CHUNK))
    print('Selesai')

    stream.close()
    p.terminate()

# Melakukan transkripsi pada file output
transcribe_audio(OUTPUT_FILE)