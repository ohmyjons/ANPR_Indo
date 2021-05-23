import cv2
import numpy as np
import glob
import random
import tensorflow as tf
from tensorflow import keras
import imutils
import os
import pytesseract


cap = cv2.VideoCapture(0)
# gambarr = 1
while True:
    _, image = cap.read()
    # resize = cv.resize(image, (2560, 768), interpolation=cv.INTER_LINEAR)
    cv2.imshow("Frame", image)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('s'):
        cv2.imwrite("capture/1.png", image)
        cap.release()
        cv2.destroyAllWindows()
        break


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

coordinates = None
roi_image = None
roi = None

    # Load Yolo
net = cv2.dnn.readNet("yolov3_training_final.weights", "yolov3_testing.cfg")

    # Name custom object
classes = ["Plate"]

    # Images path
# images_path = glob.glob(save())
images_path = glob.glob(r"C:\Users\USER\OneDrive\Desktop\plat\IMG_20210429_152106.jpg")
# images_path = glob.glob('gambar/plate1.png')


# images_path = imutils.resize(images_path , width = 500)


layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Insert here the path of your images
random.shuffle(images_path)
# loop through all the images
for img_path in images_path:
    # Loading image
    img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape

        # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=True)


    net.setInput(blob)
    outs = net.forward(output_layers)

        # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
               # Object detected
               print(class_id)
               center_x = int(detection[0] * width)
               center_y = int(detection[1] * height)
               w = int(detection[2] * width)
               h = int(detection[3] * height)

                    # Rectangle coordinates
               x = int(center_x - w / 2)
               y = int(center_y - h / 2)

               boxes.append([x, y, w, h])
               confidences.append(float(confidence))
               class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
    print(indexes)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[class_ids[i]]
            # membuat kotak pada objek yang di deteksi
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
            cv2.putText(img, label + " " + confidence, (x, y + 0), font, 1, color, 2)
                #crop pada bagian plat nomor
            plate = img[y:y + h, x:x + w]




    cv2.imshow("Image", img)
    cv2.imshow("Number Plate", plate)
    cv2.imwrite("crop/plate1.png", plate)

    key = cv2.waitKey(0)
    if key == ord('q'):
        break
        cv2.destroyAllWindows()







