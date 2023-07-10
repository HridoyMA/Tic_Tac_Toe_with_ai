import numpy as np
import cv2
import time
from collections import deque

#default called trackbar function
def setValues(x):
    print("")
bo=[0]* 10
count=0
# creating the trackbars needed for adjusting the object colour
cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors", 153,180,setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255,255, setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255,255,setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 64,180,setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 172,255,setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 200,255,setValues)

# here is code for canvas setup
paintWindow=np.zeros((600,600,3))+255
paintWindow=cv2.line(paintWindow,(20,200),(580,200),(0,0,0),10)
paintWindow=cv2.line(paintWindow,(20,400),(580,400),(0,0,0),10)
paintWindow=cv2.line(paintWindow,(200,20),(200,580),(0,0,0),10)
paintWindow=cv2.line(paintWindow,(400,20),(400,580),(0,0,0),10)

# Loading the default webcam of pc
cap=cv2.VideoCapture(0)
cap.set(4,800)
cap.set(3,800)

# keep looping
board = [" "] * 9

def get_ai_move(board):
    best_score = -float("inf")
    best_move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

def minimax(board, is_maximizing):
    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = " "
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, True)
                board[i] = " "
                best_score = min(best_score, score)
        return best_score

temp=1
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    u_hue=cv2.getTrackbarPos("Upper Hue", "Color detectors")
    u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
    u_value= cv2.getTrackbarPos("Upper Value", "Color detectors")
    l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
    l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
    l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")
    Upper_hsv=np.array([u_hue,u_saturation,u_value])
    Lower_hsv=np.array([l_hue,l_saturation,l_value])

    frame = cv2.line(frame, (20, 200), (580, 200), (0, 0, 0), 10)
    frame = cv2.line(frame, (20, 400), (580, 400), (0, 0, 0), 10)
    frame = cv2.line(frame, (200, 20), (200, 580), (0, 0, 0), 10)
    frame = cv2.line(frame, (400, 20), (400, 580), (0, 0, 0), 10)

    Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)

    cnts,_=cv2.findContours(Mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    center=None
    #If the contours are formed
    if len(cnts)>0:
        # sorting the contours to find biggest
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        # get the radius of the enclosing circle around the found contour
        ((x,y), radius)= cv2.minEnclosingCircle(cnt)
        #draw the circle around the contour
        cv2.circle(frame, (int (x),int(y)),int(radius),(0,255,255),2)
        # calculating the center of the detected contour
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        center = (cX,cY)
        if temp==1:
            if 40<= center[1]<= 160:
                if 40<= center[0]<=160:
                    if (count+2) %2 == 0 and bo[1] !=8:
                        move = 0
                        board[move] = "X"
                        cv2.line(paintWindow, (40,40), (160,160), (0,0,0),5)
                        cv2.line(paintWindow, (160, 40), (40, 160), (0, 0, 0), 5)
                        bo[1]=9
                        count+=1
                    elif (count+2) %2 != 0 and bo[1] !=9:
                        # cv2.line(paintWindow, (40,40), (160,160), (0,0,0),5)
                        # cv2.line(paintWindow, (160, 40), (40, 160), (0, 0, 0), 5)
                        cv2.circle(paintWindow, (100,100), 70, (0,0,0),5)
                        bo[1] = 8
                        count += 1
                elif 240<=center[0]<=360:
                    if (count+2) %2 == 0 and bo[2] !=8:
                        move = 1
                        board[move] = "X"
                        cv2.line(paintWindow, (240,40), (360,160), (0,0,0),5)
                        cv2.line(paintWindow, (360, 40), (240, 160), (0, 0, 0), 5)
                        bo[2]=9
                        count+=1
                    elif (count+2) %2 != 0 and bo[2] !=9:
                        cv2.circle(paintWindow, (300,100), 70, (0,0,0),5)
                        bo[2] = 8
                        count += 1
                elif 440<=center[0]<=560:
                    if (count + 2) % 2 == 0 and bo[3] != 8:
                        move = 2
                        board[move] = "X"
                        cv2.line(paintWindow, (440, 40), (560, 160), (0, 0, 0), 5)
                        cv2.line(paintWindow, (560, 40), (440, 160), (0, 0, 0), 5)
                        bo[3] = 9
                        count += 1
                    elif (count + 2) % 2 != 0 and bo[3] != 9:
                        cv2.circle(paintWindow, (500, 100), 70, (0, 0, 0), 5)
                        bo[3] = 8
                        count += 1
            elif 240<=center[1]<=360:

                if 40<= center[0]<=160:
                    if (count+2) %2 == 0 and bo[4] !=8:
                        move = 3
                        board[move] = "X"
                        cv2.line(paintWindow, (40,240), (160,360), (0,0,0),5)
                        cv2.line(paintWindow, (160, 240), (40, 360), (0, 0, 0), 5)
                        bo[4]=9
                        count+=1
                    elif (count+2) %2 != 0 and bo[4] !=9:
                        cv2.circle(paintWindow, (100,300), 70, (0,0,0),5)
                        bo[4] = 8
                        count += 1
                elif 240<=center[0]<=360:
                    if (count+2) %2 == 0 and bo[5] !=8:
                        move = 4
                        board[move] = "X"
                        cv2.line(paintWindow, (240,240), (360,360), (0,0,0),5)
                        cv2.line(paintWindow, (360, 240), (240, 360), (0, 0, 0), 5)
                        bo[5]=9
                        count+=1
                    elif (count+2) %2 != 0 and bo[5] !=9:
                        # cv2.line(paintWindow, (240,240), (360,360), (0,0,0),5)
                        # cv2.line(paintWindow, (360, 240), (240, 360), (0, 0, 0), 5)
                        cv2.circle(paintWindow, (300,300), 70, (0,0,0),5)
                        bo[5] = 8
                        count += 1
                elif 440<=center[0]<=560:
                    if (count + 2) % 2 == 0 and bo[6] != 8:
                        move = 5
                        board[move] = "X"
                        cv2.line(paintWindow, (440, 240), (560, 360), (0, 0, 0), 5)
                        cv2.line(paintWindow, (560, 240), (440, 360), (0, 0, 0), 5)
                        bo[6] = 9
                        count += 1
                    elif (count + 2) % 2 != 0 and bo[6] != 9:
                        cv2.circle(paintWindow, (500, 300), 70, (0, 0, 0), 5)
                        bo[6] = 8
                        count += 1
            elif 440<=center[1]<=560:

                if 40<= center[0]<=160:
                    if (count+2) %2 == 0 and bo[7] !=8:
                        move = 6
                        board[move] = "X"
                        cv2.line(paintWindow, (40,440), (160,560), (0,0,0),5)
                        cv2.line(paintWindow, (160, 440), (40, 560), (0, 0, 0), 5)
                        bo[7]=9
                        count+=1
                    elif (count+2) %2 != 0 and bo[7] !=9:
                        cv2.circle(paintWindow, (100,500), 70, (0,0,0),5)
                        bo[7] = 8
                        count += 1
                elif 240<=center[0]<=360:
                    if (count+2) %2 == 0 and bo[8] !=8:
                        move = 7
                        board[move] = "X"
                        cv2.line(paintWindow, (240,440), (360,560), (0,0,0),5)
                        cv2.line(paintWindow, (360, 440), (240, 560), (0, 0, 0), 5)
                        bo[8]=9
                        count+=1
                    elif (count+2) %2 != 0 and bo[8] !=9:
                        cv2.circle(paintWindow, (300,500), 70, (0,0,0),5)
                        bo[8] = 8
                        count += 1
                elif 440<=center[0]<=560:
                    if (count + 2) % 2 == 0 and bo[9] != 8:
                        move = 8
                        board[move] = "X"
                        cv2.line(paintWindow, (440, 440), (560, 560), (0, 0, 0), 5)
                        cv2.line(paintWindow, (560, 440), (440, 560), (0, 0, 0), 5)
                        bo[9] = 9
                        count += 1
                    elif (count + 2) % 2 != 0 and bo[9] != 9:
                        cv2.line(paintWindow, (440, 440), (560, 560), (0, 0, 0), 5)
                        cv2.line(paintWindow, (560, 440), (440, 560), (0, 0, 0), 5)
                        cv2.circle(paintWindow, (500, 500), 70, (0, 0, 0), 5)
                        bo[9] = 8
                        count += 1
            # temp=0

        # elif temp==0:
        #     ai_move = get_ai_move(board)
        #     if ai_move==0:
        #         board[ai_move] = "O"
        #         if bo[1]!=8:
        #             cv2.circle(paintWindow, (100, 100), 70, (0, 0, 0), 5)
        #         bo[1] = 8
        #         count += 1
        #     elif ai_move==1:
        #         board[ai_move] = "O"
        #         if bo[2]!=8:
        #             cv2.circle(paintWindow, (300, 100), 70, (0, 0, 0), 5)
        #         bo[2] = 8
        #         count += 1
        #     elif ai_move==2:
        #         board[ai_move] = "O"
        #         if bo[3]!=8:
        #             cv2.circle(paintWindow, (500, 100), 70, (0, 0, 0), 5)
        #         bo[3] = 8
        #         count += 1
        #     elif ai_move==3:
        #         board[ai_move] = "O"
        #         if bo[4]!=8:
        #             cv2.circle(paintWindow, (100, 300), 70, (0, 0, 0), 5)
        #         bo[4] = 8
        #         count += 1
        #     elif ai_move==4:
        #         board[ai_move] = "O"
        #         if bo[5]!=8:
        #             cv2.circle(paintWindow, (300, 300), 70, (0, 0, 0), 5)
        #         bo[5] = 8
        #         count += 1
        #     elif ai_move==5:
        #         board[ai_move] = "O"
        #         if bo[6]!=8:
        #             cv2.circle(paintWindow, (500, 300), 70, (0, 0, 0), 5)
        #         bo[6] = 8
        #         count += 1
        #     elif ai_move==6:
        #         board[ai_move] = "O"
        #         if bo[7]!=8:
        #             cv2.circle(paintWindow, (100, 500), 70, (0, 0, 0), 5)
        #         bo[7] = 8
        #         count += 1
        #     elif ai_move==7:
        #         board[ai_move] = "O"
        #         if bo[9]!=8:
        #             cv2.circle(paintWindow, (300, 500), 70, (0, 0, 0), 5)
        #         bo[8] = 8
        #         count += 1
        #     elif ai_move==8:
        #         board[ai_move] = "O"
        #         if bo[9]!=8:
        #             cv2.circle(paintWindow, (500, 500), 70, (0, 0, 0), 5)
        #         bo[9] = 8
        #         count += 1
        #     temp=1


    # show all windows
    cv2.imshow("Tracking",frame)
    cv2.imshow("paint", paintWindow)

    #conditions of winner of game
    if (bo[1]==9 and bo[2]==9 and bo[3]==9) or (bo[4]==9 and bo[5]==9 and bo[6]==9) or (bo[7]==9 and bo[8]==9 and bo[9]==9) or (bo[1]==9 and bo[4]==9 and bo[7]==9) or (bo[2]==9 and bo[5]==9 and bo[8]==9) or (bo[3]==9 and bo[6]==9 and bo[9]==9) or (bo[1]==9 and bo[5]==9 and bo[9]==9) or (bo[3]==9 and bo[5]==9 and bo[7]==9):
        print("X is winner")
        break
    if (bo[1]==8 and bo[2]==8 and bo[3]==8) or (bo[4]==8 and bo[5]==8 and bo[6]==8) or (bo[7]==8 and bo[8]==8 and bo[9]==8) or (bo[1]==8 and bo[4]==8 and bo[7]==8) or (bo[2]==8 and bo[5]==8 and bo[8]==8) or (bo[3]==8 and bo[6]==8 and bo[9]==8) or (bo[1]==8 and bo[5]==8 and bo[9]==8) or (bo[3]==8 and bo[5]==8 and bo[7]==8):
        print("O is winner")
        break
    if (bo[1]==9 or bo[1]==8) and (bo[2]==9 or bo[2]==8) and (bo[3]==9 or bo[3]==8) and (bo[4]==9 or bo[4]==8) and (bo[5]==9 or bo[5]==8) and (bo[6]==9 or bo[6]==8) and (bo[7]==9 or bo[7]==8) and (bo[8]==9 or bo[8]==8) and (bo[9]==9 or bo[9]==8):
        print("game draw")
        break
# 'q' key press for stop
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break
cv2.imshow("final positions", paintWindow)
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()

