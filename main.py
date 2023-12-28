import time
import cv2
import HandTrackingModule as htm
import RPi.GPIO as GPIO

# Set mode pin numbering pada GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Inisialisasi relay
relay_pin_numbers = {1: 18, 2: 27, 3: 22, 4: 23}  # Sesuaikan dengan nomor pin GPIO yang terhubung ke relay
for pin in relay_pin_numbers.values():
    GPIO.setup(pin, GPIO.OUT)

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]
state = ""
while True:
    success, img = cap.read()

    # Check if the image is not empty
    if not success or img is None:
        continue

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []

        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)

        if totalFingers == 1:
            cv2.putText(img, "Satu Jari Terpilih", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            state = 1
        elif totalFingers == 2:
            cv2.putText(img, "Dua Jari Terpilih", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            state = 2
        elif totalFingers == 3:
            cv2.putText(img, "Tiga Jari Terpilih", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            state = 3
        elif totalFingers == 4:
            cv2.putText(img, "Empat Jari Terpilih", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            state = 4
        elif totalFingers == 5 and state != "":
            relay_pin = relay_pin_numbers.get(state)  # Get the actual GPIO pin number
            if relay_pin is not None:  # Check if the relay_pin is found
                GPIO.output(relay_pin, GPIO.HIGH)
                print("Relay " + str(state) + " nyala")
            state = ""
        elif totalFingers == 0 and state != "":
            relay_pin = relay_pin_numbers.get(state)  # Get the actual GPIO pin number
            if relay_pin is not None:  # Check if the relay_pin is found
                GPIO.output(relay_pin, GPIO.LOW)
                print("Relay " + str(state) + " dimatikan")
            state = ""

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, "Terpilih " + str(state), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(10) & 0xFF == 27:  # Keluar dari loop saat tombol Esc ditekan
        break

cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()  # Bersihkan GPIO setelah selesai
