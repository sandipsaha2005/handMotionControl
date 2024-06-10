import cv2
import numpy as np
import time
import handTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 1280, 720

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0
detector=htm.HandDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)


# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

maxVol=volRange[1]
minVol=volRange[0]

while True:
    success, img=cap.read()
    img=detector.findHands(img)
    myList=detector.finePosition(img,draw=False)
    if len(myList) != 0 :
        # print(myList[4], myList[8])
        x1, y1=myList[4][1], myList[4][2]   # for thumb
        x2, y2=myList[8][1], myList[8][2]   # for the othre one finger
        cx,cy=(x1+x2)//2, (y1+y2)//2 
        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(cx,cy),5, (255,0,255),cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2),(255,0,255),3)

        length=math.hypot(x2-x1,y2-y1)
        # print(length)
        # hand range 30 - 300
        # volume range -65 - 0
        vol=np.interp(length,[30,300],[minVol,maxVol])
        # print(vol)
        volume.SetMasterVolumeLevel(vol, None)


        if length <40:
            cv2.circle(img,(cx,cy),5, (0,255,0),cv2.FILLED)




    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, f"Fps : {int(fps)}", (40, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break