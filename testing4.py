import cv2, sys, numpy, os,pandas as pd,csv

haar_file = 'haarcascade_frontalface_default.xml'
nameListForFunc1=[]
names={}
namesInDirectory=[]
datasets = 'StudentsFolder'
# print(names)
studName=''
listOfNamesPresentToday=[]
TwoDListForCSVFile=[]
countData = []
twoDdf=[]


def funcToCreateDirectoryList():
    for (subdirs, dirs, files) in os.walk(datasets):
        for subdir in dirs:
            namesInDirectory.append(subdir)

def StudentAttendance():
    print(listOfNamesPresentToday)
    # TwoDListForCSVFile.append(listOfNamesPresentToday)
    # print(TwoDListForCSVFile)

    csv=os.path.join('outp112.csv')
    a=os.path.exists(csv)
    # print(a)
    import csv
    if a==False:
        d = pd.DataFrame(listOfNamesPresentToday)
        d.to_csv("outp112.csv")
    else:
        # TwoDListForCSVFile=pd.read_csv("outp112.csv")
        # TwoDListForCSVFile.append(listOfNamesPresentToday)
        # TwoDListForCSVFile.to_csv("outp112.csv")
        import csv
        TwoDListForCSVFile.append(listOfNamesPresentToday)
        with open('outp112.csv','a',newline='') as file:
            wr=csv.writer(file)
            wr.writerows(TwoDListForCSVFile)

def funcToRecognise():
    size = 4

    print('Recognizing Face Please Be in sufficient Lights...')
    (images, lables, id) = ([], [], 0)
    for (subdirs, dirs, files) in os.walk(datasets):
        for subdir in dirs:
            names[id] = subdir
            subjectpath = os.path.join(datasets, subdir)
            for filename in os.listdir(subjectpath):
                path = subjectpath + '/' + filename
                lable = id
                images.append(cv2.imread(path, 0))
                lables.append(int(lable))
            id += 1
    (width, height) = (130, 100)

    (images, lables) = [numpy.array(lis) for lis in [images, lables]]
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(images, lables)
    face_cascade = cv2.CascadeClassifier(haar_file)
    webcam = cv2.VideoCapture(0)
    while True:
        (_, im) = webcam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            prediction = model.predict(face_resize)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

            if prediction[1] < 500:

                cv2.putText(im, '% s - %.0f' %
                            (names[prediction[0]], prediction[1]), (x - 10, y - 10),
                            cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                studName = names[prediction[0]]
                # print(studName)
                Variable = all(name != studName for name in listOfNamesPresentToday)
                if Variable == True:
                    listOfNamesPresentToday.append(studName)

            else:
                cv2.putText(im, 'not recognized',
                            (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

        cv2.imshow('OpenCV', im)

        key = cv2.waitKey(10)
        if key == 27:
            break
    print("TODAY'S ATTEDANCE DONE")

def func1():
    print("List of student already present")
    funcToCreateDirectoryList()
    print(namesInDirectory)
    sub_data = input("Enter New Student Name")

    check=all(checking != sub_data for checking in namesInDirectory)
    if check==True:
        path = os.path.join(datasets, sub_data)
        if not os.path.isdir(path):
            os.mkdir(path)
        (width, height) = (130, 100)
        face_cascade = cv2.CascadeClassifier(haar_file)
        webcam = cv2.VideoCapture(0)
        count = 1
        while count < 30:
            (_, im) = webcam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (width, height))
                cv2.imwrite('% s/% s.png' % (path, count), face_resize)
            count += 1

            cv2.imshow('OpenCV', im)
            key = cv2.waitKey(10)
            if key == 27:
                break
        print("STUDENT DETAILS ADDED")
    else:
        print("STUDENT ALREADY PRESENT")

def func2():
    funcToRecognise()
    print("Todays attendance List:")
    print(listOfNamesPresentToday)
    print('''Do you wanna take Today's attendance again?
             1. Yes
             2. No(Finalise todays attendance)''')
    takeInput=int(input())
    value=True
    while(value):
        if takeInput==1:
            func2()
        elif takeInput==2:
            StudentAttendance()
            value=False
        else:
            print("Invalid Input,Try Again")
            value=False

def predictionFunc():
    csvAttendance = os.path.join('Attendance.csv')
    a = os.path.exists(csvAttendance)
    if a == False:
        df = pd.DataFrame({'names': namesInDirectory})
        df['Days present'] = countData
        df.to_csv("Attendance.csv")
    else:
        xd=pd.read_csv("Attendance.csv")
        xd = pd.DataFrame({'names': namesInDirectory})
        xd['Days present'] = countData
        xd.to_csv("Attendance.csv")

def findAttendance(name):
    d=namesInDirectory.index(name)
    return twoDdf[d]


    # funcToAddListToCSVFile()
def func3():
    csv = os.path.join('outp112.csv')
    a = os.path.exists(csv)
    # print(a)
    import csv
    if a == False:
        print("Attendance Detail Not present")
    else:
        # df = pd.read_csv('outp112.csv')
        # data=df.iloc[:,:].values
        data=[]
        funcToCreateDirectoryList()

        # print(data)
        with open('outp112.csv','r')as file:
            wr=csv.reader(file)
            for row in wr:
                data.append(row)
        # print(data)
        for k in range(len(namesInDirectory)):
            count=0
            for i in range(len(data)):
                for j in range(len(data[i])):
                    if data[i][j]==namesInDirectory[k]:
                        count+=1
            countData.append(count)
        # print(namesInDirectory)
        # print(countData)
        totalNumDays=len(data)
        print("Total days=",totalNumDays)
        for i in range(len(namesInDirectory)):
            num=countData[i]/totalNumDays*100
            twoDdf.append(num)
        # print("percentage",twoDdf)
        predictionFunc()
        name=input("enter the name:")
        a=findAttendance(name)
        if a<70:
            print(a,"% less than 70% and attend future classes")
        else:
            print(a,"%")




if __name__ == '__main__':
    while (True):
        print('''SELECT THE OPERATION YOU WANT TO PERFORM
                         1.ADD NEW STUDENT
                         2.TAKE TODAYS ATTENDANCE
                         3.DISPLAY ATTENDANCE
                         4.EXIT''')
        oper = int(input("Enter any number"))
        print(oper)
        if oper == 1:
            func1()
        elif oper == 2:
            func2()
        elif oper == 3:
            func3()
        elif oper == 4:
            exit(0)
        else:
            print("Invalid Input")