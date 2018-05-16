# coding=utf-8
import os
from PIL import Image
import cv2
import numpy as np
from PyQt5 import QtGui


class Video():
    def __init__(self, capture):
        self.cam = cv2.VideoCapture(capture)
        self.currentFrame = np.array([])
        self.faceCascade = cv2.CascadeClassifier('./data/haarcascades/haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.checkTrainerFound = os.path.isfile('trainer/trainer.yml')
        if self.checkTrainerFound == True:
            self.recognizer.read('trainer/trainer.yml')

    def quit(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def captureNextFrame(self):
        ret, readFrame = self.cam.read()
        gray = cv2.cvtColor(readFrame, cv2.COLOR_BGR2GRAY)
        if (ret == True):
            faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(20, 20)
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(readFrame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            self.currentFrame = cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)

    def convertFrame(self):
        try:
            height, width = self.currentFrame.shape[:2]
            img = QtGui.QImage(self.currentFrame,
                               width,
                               height,
                               QtGui.QImage.Format_RGB888)
            img = QtGui.QPixmap.fromImage(img)
            self.previousFrame = self.currentFrame
            return img
        except:
            return None

    def captureFace(self, face_id):
        self.cam.set(3, 640)  # set video width
        self.cam.set(4, 480)  # set video height

        print('[INFO] Initializing face capture. Look the camera and wait ...')
        count = 0

        while (True):
            ret, img = self.cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1
                cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])
            # Take 30 face sample and stop video
            if count >= 30:
                cv2.imwrite("image/User." + str(face_id) + ".jpg", gray[y:y + h, x:x + w])
                break

        print('[INFO] Face capture had done !!!')

    def trainingFace(self):
        path = 'dataset'
        recognizer = cv2.face.LBPHFaceRecognizer_create()

        def getImagesAndLabels(path):
            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faceSamples = []
            ids = []

            for imagePath in imagePaths:

                PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
                img_numpy = np.array(PIL_img, 'uint8')

                id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces = self.faceCascade.detectMultiScale(img_numpy)

                for (x, y, w, h) in faces:
                    faceSamples.append(img_numpy[y:y + h, x:x + w])
                    ids.append(id)

            return faceSamples, ids

        print("[INFO] Training faces. It will take a few seconds. Wait ...")
        faces, ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        recognizer.write('trainer/trainer.yml')

        print("[INFO] {0} faces trained !!!".format(len(np.unique(ids))))

    def recogitionFace(self, names, defect_out):
        # names = [{'id': 2222, 'name': 'a'}, {'id': 1111, 'name': 'b'}, {'id': 1, 'name': 'c'}]
        # Define min window size to be recognized as a face
        data = []
        name = ''
        id = ''
        confidence = 0.
        minW = 0.1 * self.cam.get(3)
        minH = 0.1 * self.cam.get(4)
        ret, img = self.cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if (ret == True):
            faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if self.checkTrainerFound == True:
                    id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])
                    # Check if confidence is less them 100 ==> is perfect match
                    if (confidence < 100):
                        result_list = [d for d in names if d.get('id', '') == id]
                        name = result_list[0]['name']
                        # Only process if detection than 45%
                        if confidence <= 50:
                            defect_out.append({'id': id, 'name': name})
                        confidence = "  {0}%".format(round(100 - confidence))
                    else:
                        name = "Unknown"
                        confidence = "  {0}%".format(round(100 - confidence))
                else:
                    name = "Unknown"
                cv2.putText(img, str(name), (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)

            self.currentFrame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
