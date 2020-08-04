import random
import urllib.request
import cv2
import numpy as np
import os 
from PIL import Image
import urllib.request as ur
import requests

def download_web_image(url):
    #name=random.randrange(1,30)
    full_name='1.jpg'
    urllib.request.urlretrieve(url, full_name)
a=r"https://manned-problems.000webhostapp.com/2"
while True:
    try:
        download_web_image(a)
        facerec()
    except urllib.error.HTTPError:
        print("Error")

def facerec():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('C:/pro_/trainer.yml')
    cascadePath = "C:/pro_/haarcascade_frontalface_default.xml"
    eye_cascade = cv2.CascadeClassifier("C:/pro_/haarcascade_eye.xml")
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX
    id = 0
    names = ['None', 'karthik','jayanth','jayanth']
    i=0
    stri=""
    os.remove('hci.txt')
    while i<3:
        img = cv2.imread("1.jpg")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            if (confidence < 100):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
                stri=stri+"_"+id
                #print(stri)
                #break
                i=4
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))        
                stri=stri+id
                #print("unknown")
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1) 
        print(stri)
        cv2.imshow('img',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        i=i+1
    print("\n [INFO] Exiting Program and cleanup stuff")
    file = open('hci.txt','w')
    file.write(stri)
    file.close()
    r = requests.get("https://manned-problems.000webhostapp.com/hci_server.php", params=stri)
    r=requests.post("https://manned-problems.000webhostapp.com/hci_server.php",data=stri)