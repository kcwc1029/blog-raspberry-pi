from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(8)  # 樹莓派5同時連接Pi相機模組是8; 樹莓派4是1, 否則是0
detector = HandDetector(detectionCon=0.5, maxHands=1)

while cap.isOpened():
    success, img = cap.read()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        bbox = hand["bbox"]        
        fingers = detector.fingersUp(hand)
        totalFingers = fingers.count(1)
        print(totalFingers)
        msg = "None"
        if totalFingers == 5:
            msg = "Paper"
        if totalFingers == 0:
            msg = "Rock"
        if totalFingers == 2:
            if fingers[1] == 1 and fingers[2] == 1:
                msg = "Scissors"
        cv2.putText(img, msg, (bbox[0]+200,bbox[1]-30),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.imshow("CVZone Hand Detector", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
        
cap.release()
cv2.destroyAllWindows()
