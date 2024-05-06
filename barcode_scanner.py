import cv2
from pyzbar.pyzbar import decode
import requests

def scan_barcode():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Unable to capture video.")
            break

        decoded_objects = decode(frame)

        for obj in decoded_objects:
            barcode_data = obj.data.decode('utf-8')
            print("Detected Barcode:", barcode_data)
            send_barcode_data(barcode_data)

        cv2.imshow("Barcode Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def send_barcode_data(data):
    url = "http://127.0.0.1:5000/barcode"
    payload = {"barcode": data}

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raise an exception for non-2xx responses
        print("Barcode data sent successfully:", response.text)
    except requests.exceptions.RequestException as e:
        print("An error occurred while sending data:", e)

if __name__ == "__main__":
    scan_barcode()

