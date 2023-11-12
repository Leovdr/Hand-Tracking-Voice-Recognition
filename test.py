import pyttsx3
import speech_recognition as sr
import os

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Silakan ucapkan perintah...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Mengenali perintah...")
        command = recognizer.recognize_google(audio, language="id-ID").lower()
        print("Anda mengatakan:", command)
        return command
    except sr.UnknownValueError:
        print("Maaf, tidak dapat mengenali perintah.")
        return ""
    except sr.RequestError as e:
        print(f"Error saat mengakses layanan Google Speech Recognition: {e}")
        return ""

def open_application(application_name):
    try:
        if "notepad" in application_name:
            os.system("start notepad.exe")
        elif "calculator" in application_name:
            os.system("start calc.exe")
        # Tambahkan aplikasi lain sesuai kebutuhan

        speak(f"{application_name} berhasil dibuka.")
    except Exception as e:
        speak(f"Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    speak("Halo, saya siap mendengarkan perintah Anda.")

    while True:
        command = listen()

        if "buka" in command and ("notepad" in command or "kalkulator" in command):
            open_application(command)
        elif "keluar" in command or "selesai" in command:
            speak("Program selesai.")
            break
