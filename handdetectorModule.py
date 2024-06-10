import cv2
import mediapipe as mp
import time
import handTrackingModule as htm

pTime = 0
cap = cv2.VideoCapture(0)
detector = htm.HandDetector()

while True:
    success, img = cap.read()
    if not success:
        break

    img = detector.findHands(img)
    myList=detector.finePosition(img)
    if len(myList) != 0:
        print(myList[4])
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

