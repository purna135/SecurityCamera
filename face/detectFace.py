import time
import cv2
import os
import requests
import threading


def send_data():
    print('Sending data to server...')
    urlImages = 'https://litindia.herokuapp.com/receive-images/'
    file = "image.png"

    with open(file, 'rb') as f:
        filename = "image.png"
        files = {'file': (filename, f)}
        r = requests.post(urlImages, files=files)

    os.remove('image.png')
    print(r)


def take_photo():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
    cap = cv2.VideoCapture(0) 
    t = 0

    while True:
        ret, img = cap.read()  
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5) 

        if(type(faces) is not tuple) and (time.time() - t) > 30:
                cv2.imwrite('image.png', img)
                t1 = threading.Thread(target=send_data, args=())
                t1.setDaemon(True)
                t1.start()
                t = time.time()
                
        for (x,y,w,h) in faces: 
            # To draw a rectangle in a face  
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)  
            roi_gray = gray[y:y+h, x:x+w] 
            roi_color = img[y:y+h, x:x+w] 
      
        # Display an image in a window 
        cv2.imshow('img',img) 
      
        k = cv2.waitKey(30) & 0xff
        if k == 27: 
            break
      
    cap.release()
    cv2.destroyAllWindows()

take_photo()