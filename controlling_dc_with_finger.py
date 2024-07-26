import cv2
import mediapipe as mp
import serial
import time


arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

def send_data(data):
    arduino.write(bytes(data, 'utf-8'))
    time.sleep(0.05)
    response = arduino.readline().decode('utf-8').strip()
    print(f"Arduino response: {response}")
    return response

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

def is_fingers_touching(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
    return distance < 0.05  # Ngưỡng khoảng cách để nhận diện ngón tay chạm nhau

try:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Không thể nhận diện hình ảnh từ camera.")
            break

        # Chuyển đổi màu từ BGR sang RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Xử lý nhận diện bàn tay
        results = hands.process(image_rgb)

        # Vẽ kết quả nhận diện bàn tay lên hình ảnh
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                if is_fingers_touching(hand_landmarks):
                    print("Fingers touching")
                    send_data('1')  # Ngón tay chạm nhau, bật motor
                else:
                    print("Fingers not touching")
                    send_data('0')  # Ngón tay không chạm nhau, tắt motor

        # Hiển thị hình ảnh
        cv2.imshow('Nhận diện tay', image)

        # Thoát bằng cách nhấn phím 'q'
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")

finally:
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()
