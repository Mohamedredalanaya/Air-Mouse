import cv2
import mediapipe as mp
import math
from Volume_controller import volumec
import time
import win32api, win32con
import pyautogui

mxhand=1
cap = cv2.VideoCapture(0)
mphands=mp.solutions.hands
hands=mphands.Hands(
    static_image_mode=True,
    max_num_hands=mxhand,
    min_detection_confidence=0.7)
mpDraw=mp.solutions.drawing_utils
thumb1=(0,0)
thumb2=(0,0)
clicky1=0
clicky0=0
clickt=0
a=float(input("""what are you gonna use this programme for?
              1-Volume controller
              2-Air mouse
              """))
vol=0
x=1920/2
y=1080/2
while True:
    success, img=cap.read()
    img=cv2.flip(img, 1)
    frame=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result=hands.process(frame)
    lmList=[]
    if a!=1 and a!=2:
        print("make sure to choose 1 or 2!")
        break
    cv2.rectangle(img,(200,0),(650,253),(0,0,255),2)
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                
                h, w , c = img.shape
                cx, cy =int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if a==1:
                    mxhand=2
                    if id==4:
                        cv2.circle(img, (cx,cy), 7, (0,0,255), cv2.FILLED)
                        thumb2=(cx,cy)
                    if id==8:
                        cv2.circle(img, (cx,cy), 7, (0,0,255), cv2.FILLED)
                        thumb1=(cx,cy)
                    cv2.line(img, thumb1, thumb2, (0,0,255),5)
                    rawD=math.sqrt((thumb1[0]-thumb2[0])**2+(thumb1[1]-thumb2[1])**2)-20
                    
                    if rawD<0:
                        pass
                    if rawD>0:
                        if rawD<200:
                            newD=round(rawD*100/20000,2)
                            print('Volume = {}%'.format(int(newD*100)))
                            volumec(newD)
                if a==2:
                    mxhand=1
                    if id==4:
                        thumb2=(cx,cy)
                    if id==8:
                        cv2.circle(img,(cx,cy),5,(0,165,255),cv2.FILLED)
                        if cx>201  and cy<169:
                            ncx=int((cx-200)*4.3)
                            ncy=int((cy)*4.3)
                            clickt=(ncx,ncy)
                            #print(ncx,ncy)
                            
                            #pyautogui.moveTo(ncx,ncy)
                            if clickt<(1920,1080):                                                                        
                                win32api.SetCursorPos((ncx,ncy))
                        thumb1=(cx,cy)
                        ClickD=int(math.sqrt((thumb1[0]-thumb2[0])**2+(thumb1[1]-thumb2[1])**2))
                        print(ClickD)
                        if ClickD<20:
                            pyautogui.mouseDown()
                        if ClickD>20:
                            pyautogui.mouseUp()
                            
                        

    cv2.imshow('Hand Tracker', img)
    if cv2.waitKey(5) & 0xff == 27 :
        break