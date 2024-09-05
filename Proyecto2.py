import cv2
import numpy as np
import webbrowser
import pyautogui

qcd = cv2.QRCodeDetector()
cap = cv2.VideoCapture(0)
video = cv2.VideoWriter("ProyectoQR.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640, 480))

#cv2.namedWindow("Codigo QR")
if not cap.isOpened():
    print("Error al acceder a la camara")
    exit()

while cap.isOpened():
    ret,frame = cap.read()
    
    if ret:
        video.write(frame)
        retQR, decode_info, points,straight_qrcode=qcd.detectAndDecodeMulti(frame)
        if retQR:
            mask = np.zeros_like(frame,dtype=np.uint8)
            points = np.array(points, np.int32)

            #print(decode_info)


            cv2.fillPoly(mask,points,(255,255,255))

            frame=cv2.bitwise_and(frame,mask)

            for s,p in zip(decode_info,points):
                frame = cv2.putText(frame,s,p[0].astype(int),
                                  cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2,cv2.LINE_AA)
                webbrowser.open_new(s)
                img = pyautogui.screenshot() #Captura de pantallla

        cv2.imshow("Codigo QR",frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
video.release()