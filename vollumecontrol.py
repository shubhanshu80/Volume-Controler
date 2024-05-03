import cv2
import mediapipe  # type: ignore
import numpy as np  # type: ignore
import time
import handtrackingmodule as htm
import math
from ctypes import cast,pointer
from comtypes import CLSCTX_ALL  # type: ignore
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # type: ignore

#pycaw initialisations
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#olume.GetMute()
#volume.GetMasterVolumeLevel()

volran=volume.GetVolumeRange()

minvol=volran[0]
maxvol=volran[1]
vol=0
volBar=400
percent=0

#########################
wcam,hcam=640,480
#########################

cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
ctime=0
ptime=0

detector=htm.handDetector(detectionCon=0.7)

while True:
    success,img=cap.read()


    img=detector.findHands(img)
    lemlist=detector.findPostion(img,draw=False)
    
    if len(lemlist)!=0:
        f1,f2=lemlist[4],lemlist[8]
        x1,y1=f1[1],f1[2]
        x2,y2=f2[1],f2[2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)

        length=math.hypot(x2-x1,y2-y1)
        #print(length)

        if length<15 or length>130:
            cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)

        #Hand Range is 15 to 130
        #volume range is -65 to 0

        vol=np.interp(length,[15,130],[minvol,maxvol])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)
        volBar=np.interp(length,[15,130],[400,150])
        percent=np.interp(length,[15,130],[0,100])

    #flipping the image / mirror image
    img=cv2.flip(img,1)


    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img,f'{int(percent)}%',(50,140),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(0,0,255),1)


    #fPS Controls
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,f"FPS: {int(fps)}",(10,30),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(0,0,255),1)
     


    cv2.imshow("VolumeControl",img)
    cv2.waitKey(1)