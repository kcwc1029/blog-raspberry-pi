"""
Pose Module
By: Computer Vision Zone
Website: https://www.computervision.zone/
"""
import math

import cv2
import mediapipe as mp


class PoseDetector:
    """
    Estimates Pose points of a human body using the mediapipe library.
    """

    def __init__(self, staticMode=False,
                 modelComplexity=1,
                 smoothLandmarks=True,
                 enableSegmentation=False,
                 smoothSegmentation=True,
                 detectionCon=0.5,
                 trackCon=0.5):
        """
        :param mode: In static mode, detection is done on each image: slower
        :param upBody: Upper boy only flag
        :param smooth: Smoothness Flag
        :param detectionCon: Minimum Detection Confidence Threshold
        :param trackCon: Minimum Tracking Confidence Threshold
        """

        self.staticMode = staticMode
        self.modelComplexity = modelComplexity
        self.smoothLandmarks = smoothLandmarks
        self.enableSegmentation = enableSegmentation
        self.smoothSegmentation = smoothSegmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.staticMode,
                                     model_complexity=self.modelComplexity,
                                     smooth_landmarks=self.smoothLandmarks,
                                     enable_segmentation=self.enableSegmentation,
                                     smooth_segmentation=self.smoothSegmentation,
                                     min_detection_confidence=self.detectionCon,
                                     min_tracking_confidence=self.trackCon)

    def findPose(self, img, draw=True):
        """
        Find the pose landmarks in an Image of BGR color space.
        :param img: Image to find the pose in.
        :param draw: Flag to draw the output on the image.
        :return: Image with or without drawings
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True, bboxWithHands=False):
        self.lmList = []
        self.bboxInfo = {}
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # The magnitude of z uses roughly the same scale as x.
                cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                self.lmList.append([cx, cy, cz])

            # Bounding Box
            ad = abs(self.lmList[12][0] - self.lmList[11][0]) // 2
            if bboxWithHands:
                if self.lmList[15][0] > self.lmList[16][0]:
                    x1 = self.lmList[16][0] - ad
                    x2 = self.lmList[15][0] + ad
                else:
                    x1 = self.lmList[15][0] - ad
                    x2 = self.lmList[16][0] + ad
            else:
                if self.lmList[11][0] > self.lmList[12][0]:
                    x1 = self.lmList[12][0] - ad
                    x2 = self.lmList[11][0] + ad
                else:
                    x1 = self.lmList[11][0] - ad
                    x2 = self.lmList[12][0] + ad

            y1 = self.lmList[1][1] - ad
            if self.lmList[30][1] > self.lmList[29][1]:
                y2 = self.lmList[30][1] + ad
            else:
                y2 = self.lmList[29][1] + ad

            if x1 < 0: x1 = 0
            if y1 < 0: y1 = 0
            bbox = (x1, y1, x2 - x1, y2 - y1)
            cx, cy = bbox[0] + (bbox[2] // 2), \
                     bbox[1] + bbox[3] // 2
            
            self.bboxInfo = {"bbox": bbox, "center": (cx, cy)}

            if draw:
                cv2.rectangle(img, bbox, (255, 0, 255), 3)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        return self.lmList, self.bboxInfo

    def findDistance(self, p1, p2, img=None, color=(255, 0, 255), scale=5):
        """
           Find the distance between two landmarks input should be (x1,y1) (x2,y2)
           :param p1: Point1 (x1,y1)
           :param p2: Point2 (x2,y2)
           :param img: Image to draw output on. If no image input output img is None
           :return: Distance between the points
                    Image with output drawn
                    Line information
           """
        if len(p1) == len(p2) == 3:
            # Get the landmarks
            x1, y1 = p1[0:2]
            x2, y2 = p2[0:2]
        else:
            x1, y1 = p1
            x2, y2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)

        if img is not None:
            cv2.line(img, (x1, y1), (x2, y2), color, max(1, scale // 3))
            cv2.circle(img, (x1, y1), scale, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), scale, color, cv2.FILLED)
            cv2.circle(img, (cx, cy), scale, color, cv2.FILLED)

        return length, img, info
    
    def findDistance3D(self, p1, p2, img=None, color=(255, 0, 255), scale=5):
        """
           Find the distance between two landmarks input should be (x1,y1,z1) (x2,y2,z2)
           :param p1: Point1 (x1,y1,z1)
           :param p2: Point2 (x2,y2,z2)
           :param img: Image to draw output on. If no image input output img is None
           :return: Distance between the points
                    Image with output drawn
                    Line information
           """
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        info = (x1, y1, x2, y2, cx, cy)

        if img is not None:
            cv2.line(img, (x1, y1), (x2, y2), color, max(1, scale // 3))
            cv2.circle(img, (x1, y1), scale, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), scale, color, cv2.FILLED)
            cv2.circle(img, (cx, cy), scale, color, cv2.FILLED)

        return length, img, info
    
    def findAngle(self,p1, p2, p3, img=None, color=(255, 0, 255), scale=5):
        """
        Finds angle between three points.

        :param p1: Point1 - (x1,y1,z1)
        :param p2: Point2 - (x2,y2,z2)
        :param p3: Point3 - (x3,y3,z3)
        :param img: Image to draw output on. If no image input output img is None
        :return:
        """
        angle, img = self.findAngle3D(p1[0:2], p2[0:2], p3[0:2],
                                      img=img,
                                      color=color,
                                      scale=scale)
        return angle, img

    def findAngle3D(self, point_a, point_b, point_c, img=None, color=(255, 0, 255), scale=5):
        """
        Finds angle between three points.

        :param point_a: Point1 - (x1,y1,z1)
        :param point_b: Point2 - (x2,y2,z2)
        :param point_c: Point3 - (x3,y3,z3)
        :param img: Image to draw output on. If no image input output img is None
        :return:   
        """
        a_x, b_x, c_x = point_a[0], point_b[0], point_c[0]  # a、b、c三個點的x座標
        a_y, b_y, c_y = point_a[1], point_b[1], point_c[1]  # a、b、c三個點的y座標

        if len(point_a) == len(point_b) == len(point_c) == 3:
            a_z, b_z, c_z = point_a[2], point_b[2], point_c[2]  # a、b、c三個點的z座標
        else:
            a_z, b_z, c_z = 0,0,0  # 因為是二維座標, 所以z軸都為0

        # 向量 m=(x1,y1,z1), n=(x2,y2,z2)
        x1,y1,z1 = (a_x-b_x),(a_y-b_y),(a_z-b_z)
        x2,y2,z2 = (c_x-b_x),(c_y-b_y),(c_z-b_z)

        # 計算角度
        cos_b = (x1*x2 + y1*y2 + z1*z2) / (math.sqrt(x1**2 + y1**2 + z1**2) *(math.sqrt(x2**2 + y2**2 + z2**2))) 
        angle = math.degrees(math.acos(cos_b))
        
        # Draw
        if img is not None:
            cv2.line(img, (a_x, a_y), (b_x, b_y), (255, 255, 255), max(1,scale//5))
            cv2.line(img, (c_x, c_y), (b_x, b_y), (255, 255, 255), max(1,scale//5))
            cv2.circle(img, (a_x, a_y), scale, color, cv2.FILLED)
            cv2.circle(img, (a_x, a_y), scale+5, color, max(1,scale//5))
            cv2.circle(img, (b_x, b_y), scale, color, cv2.FILLED)
            cv2.circle(img, (b_x, b_y), scale+5, color, max(1,scale//5))
            cv2.circle(img, (c_x, c_y), scale, color, cv2.FILLED)
            cv2.circle(img, (c_x, c_y), scale+5, color, max(1,scale//5))
            cv2.putText(img, str(int(angle)), (b_x - 50, b_y + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, color, max(1,scale//5))
        
        return angle, img

    def angleCheck(self, myAngle, targetAngle, offset=20):
        return targetAngle - offset < myAngle < targetAngle + offset


def main():
    # Initialize the webcam and set it to the third camera (index 2)
    cap = cv2.VideoCapture(2)

    # Initialize the PoseDetector class with the given parameters
    detector = PoseDetector(staticMode=False,
                            modelComplexity=1,
                            smoothLandmarks=True,
                            enableSegmentation=False,
                            smoothSegmentation=True,
                            detectionCon=0.5,
                            trackCon=0.5)

    # Loop to continuously get frames from the webcam
    while True:
        # Capture each frame from the webcam
        success, img = cap.read()

        # Find the human pose in the frame
        img = detector.findPose(img)

        # Find the landmarks, bounding box, and center of the body in the frame
        # Set draw=True to draw the landmarks and bounding box on the image
        lmList, bboxInfo = detector.findPosition(img, draw=True, bboxWithHands=False)

        # Check if any body landmarks are detected
        if lmList:
            # Get the center of the bounding box around the body
            center = bboxInfo["center"]

            # Draw a circle at the center of the bounding box
            cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

            # Calculate the distance between landmarks 11 and 15 and draw it on the image
            length, img, info = detector.findDistance(lmList[11][0:2],
                                                      lmList[15][0:2],
                                                      img=img,
                                                      color=(255, 0, 0),
                                                      scale=10)

            # Calculate the angle between landmarks 11, 13, and 15 and draw it on the image
            angle, img = detector.findAngle(lmList[11][0:2],
                                            lmList[13][0:2],
                                            lmList[15][0:2],
                                            img=img,
                                            color=(0, 0, 255),
                                            scale=10)

            # Check if the angle is close to 50 degrees with an offset of 10
            isCloseAngle50 = detector.angleCheck(myAngle=angle,
                                                 targetAngle=50,
                                                 offset=10)

            # Print the result of the angle check
            print(isCloseAngle50)

        # Display the frame in a window
        cv2.imshow("Image", img)

        # Wait for 1 millisecond between each frame
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
