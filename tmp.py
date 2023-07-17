import cv2import dlib
from scipy.spatial import distanceimport time
import serialimport urllib.request
stateFlag = False

# s = serial.Serial("COM3", 9600)
def calculate_EAR(eye):
    A = distance.euclidean(eye[1], eye[5])    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])    ear_aspect_ratio = (A + B) / (2.0 * C)
    return ear_aspect_ratio

# ThingSpeak API parameters
api_key = "0AMG19C4NKZLBQBI"field_id = "1"
cap = cv2.VideoCapture(0)
hog_face_detector = dlib.get_frontal_face_detector()dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while True:
    if stateFlag == False:
        url = f"https://api.thingspeak.com/update?api_key={api_key}&field{field_id}={0}"        urllib.request.urlopen(url)
    _, frame = cap.read()    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = hog_face_detector(gray)
    for face in faces:
        face_landmarks = dlib_facelandmark(gray, face)
        leftEye = []        rightEye = []
        
        for n in range(36, 42):
            x = face_landmarks.part(n).x            y = face_landmarks.part(n).y
            leftEye.append((x, y))            next_point = n + 1
            if n == 41:                next_point = 36
            x2 = face_landmarks.part(next_point).x            y2 = face_landmarks.part(next_point).y
            cv2.line(frame, (x, y), (x2, y2), (0, 255, 0), 1)
        
        for n in range(42, 48):            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y            rightEye.append((x, y))
            next_point = n + 1            if n == 47:
                next_point = 42            x2 = face_landmarks.part(next_point).x
            y2 = face_landmarks.part(next_point).y            cv2.line(frame, (x, y), (x2, y2), (0, 255, 0), 1)
        
        left_ear = calculate_EAR(leftEye)
        right_ear = calculate_EAR(rightEye)
        
        EAR = (left_ear + right_ear) / 2        
        EAR = round(EAR, 2)
        
        if EAR < 0.20:
            cv2.putText(frame, "DROWSY", (20, 100),                        cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4)
            cv2.putText(frame, "Take a break", (20, 400),                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
            print("Drowsy")
            counter += 1            print(counter)
            if counter >= 3:
                print("Alert!!!!!!!!!!!!!!!!!!!!!!")                # s.write(b'a')
                # Send data to ThingSpeak                url = f"https://api.thingspeak.com/update?api_key={api_key}&field{field_id}={1}"
                urllib.request.urlopen(url)                stateFlag = True
                break            else:
                    stateFlag = False
            # s.write(b'b')
            time.sleep(1)
        else:            counter = 0
            print("else reached")            url = f"https://api.thingspeak.com/update?api_key={api_key}&field{field_id}={1}"
            urllib.request.urlopen(url)        # s.write(b'b')
        print(EAR)
    
    cv2.imshow("Are you Sleepy", frame)
    key = cv2.waitKey(1)

    if key == 27:        
        break

cap.release()cv2.destroyAllWindows()
