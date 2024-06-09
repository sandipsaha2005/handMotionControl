import cv2
import mediapipe as mp
import time
cap=cv2.VideoCapture(0)

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands=mpHands.Hands()

pTime=0
cTime=0

while True:
    success, img=cap.read()
    imageRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imageRGB)
    # print(f"the result is : {results.multi_hand_landmarks}")

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w) , int(lm.y*h)
                print(id,cx,cy)
                if(id==0):
                    cv2.circle(img, (cx,cy), 25, (255,0,255),cv2.FILLED)
                if(id==1):
                    cv2.circle(img, (cx,cy), 25, (0,255,255),cv2.FILLED)
            mpDraw.draw_landmarks(img,handLms, mpHands.HAND_CONNECTIONS)


    cTime=time.time()
    fps = 1/ (cTime-pTime)
    pTime=cTime


    cv2.putText(img,str(int(fps)),(10,70), cv2.FONT_HERSHEY_SIMPLEX,3, ( 255,0,255),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break