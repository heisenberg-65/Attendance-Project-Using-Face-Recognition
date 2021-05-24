import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from database import Database
path = 'Images'

images =[]
classNames = []
mylist = os.listdir(path)

face_database=Database()
temp = face_database.get_returnable_data()


for cl in mylist :
    cur = cv2.imread(f'{path}/{cl}')
    images.append(cur)
    classNames.append(os.path.splitext(cl)[0])

def findEncoding(images):
    encList = []
    for img in images :
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encList.append(encode)
    return encList
falsecnt = [0]*len(temp)
def Attendance(scholar):
    if temp[scholar-1][4] != 'P' :
        falsecnt[scholar-1]+=1
        if(falsecnt[scholar-1]>=10) :
            temp[scholar-1][4]='P'
            temp[scholar-1][3] = datetime.now().strftime('%H:%M:%S')


encodeList = findEncoding(images)


cam = cv2.VideoCapture(0)

while True :
    success, img = cam.read()
    img2 = cv2.resize(img,(0,0),None,0.25,0.25)
    img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
    facesCurLoc = face_recognition.face_locations(img2)
    encodeCur = face_recognition.face_encodings(img2,facesCurLoc)

    for encodeFace,faceLoc in zip(encodeCur,facesCurLoc):
        matches=face_recognition.compare_faces(encodeList,encodeFace)
        dist=face_recognition.face_distance(encodeList,encodeFace)
        bestIdx = np.argmin(dist)

        if matches[bestIdx]:
            scholar = int(classNames[bestIdx])
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            col=(0,255,0)
            thick=2
            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
            cv2.rectangle(img,(x1,y1),(x2,y2),col,thick)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),col,cv2.FILLED)
            cv2.putText(img,temp[scholar-1][1],(x1+6,y2-6),font,1,(255,255,255),thick)
            Attendance(scholar)
    cv2.imshow("Frame", img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

face_database.upload(temp)
