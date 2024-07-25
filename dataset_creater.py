import cv2
import numpy as np
import sqlite3

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)


def insertorupdate(Id, Name, Age):
    conn = sqlite3.connect("sqlite.db")
    cmd = "SELECT * FROM Person WHERE Id =" + str(Id)
    cursor = conn.execute(cmd)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if (isRecordExist == 1):
        conn.execute("UPDATE Person SET Name = ?, Age = ? WHERE Id = ? ", (Name, Age, Id))
    else:
        conn.execute("INSERT into person (Id, Name, Age) VALUES (?, ?, ?)", (Id, Name, Age))

    conn.commit()
    conn.close()

    Id = input('Enter your ID: ')
    Name = input('Enter your name: ')
    Age = input('Enter your age: ')

    insertorupdate(Id, Name, Age)

    sampleNum = 0;
    while (True):
        ret, image = cam.read();
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sampleNum = sampleNum + 1;
            cv2.imwrite("dataset/user." + str(Id) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.waitKey(100)
        cv2.imshow("Face", image)
        cv2.waitKey(1);
        if(sampleNum>20):
            break;

    cam.release()
    cv2.destroyAllWindows()
