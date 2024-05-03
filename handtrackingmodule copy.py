import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackDec=0.5,model_complexity=1):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackDec=trackDec
        self.model_complexity=model_complexity
        
        self.mpDraw=mp.solutions.drawing_utils

        self.mpHand=mp.solutions.hands
        self.hands=self.mpHand.Hands(self.mode,self.maxHands,self.model_complexity,self.detectionCon,self.trackDec)

    def findHands(self,img,draw=True):

        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
        #print(self.results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handMrks in self.results.multi_hand_landmarks:
                if draw:
                    #this is to draw the hand connections and landmarks
                    self.mpDraw.draw_landmarks(img,handMrks,self.mpHand.HAND_CONNECTIONS)
        return img
    
    def findPostion(self,img,handNo=0,draw=True):

        lmlist=[]
        if self.results.multi_hand_landmarks:
            Myhand=self.results.multi_hand_landmarks[handNo]
        
            for id , ln in enumerate(Myhand.landmark):
                h,w,c=img.shape
                cx,cy=int(ln.x*w),int(ln.y*h)
                #print(id,cx,cy)
                lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)
            
        return lmlist
    

def main():
    ptime=0
    ctime=0
    detec=handDetector()
    cap=cv2.VideoCapture(0)
    while True:
        success,img=cap.read()
        img=detec.findHands(img,draw=False)
        lmlist=detec.findPostion(img,draw=False)
        if len(lmlist)!=0:
            print(lmlist[4])

        #this is to print the frame rate
        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime
        
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,255),3)
        cv2.imshow("Image",img)
        cv2.waitKey(1)



if __name__ =="__main__":
    main()


