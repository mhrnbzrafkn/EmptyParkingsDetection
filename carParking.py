import pickle
import cv2

cap = cv2.VideoCapture('./src/vid-01.mp4')

width, height = 20, 50
with open('CarParkPos', 'rb') as f:
    poslist = pickle.load(f)

def putTextRect(img, text, pos, scale=3, thickness=3, colorT=(255, 255, 255),
                colorR=(255, 0, 255), font=cv2.FONT_HERSHEY_PLAIN,
                offset=10, border=None, colorB=(0, 255, 0)):
    ox, oy = pos
    (w, h), _ = cv2.getTextSize(text, font, scale, thickness)
    
    x1, y1, x2, y2 = ox - offset, oy + offset, ox + w + offset, oy - h - offset
    
    cv2.rectangle(img, (x1, y1), (x2, y2), colorR, cv2.FILLED)
    if border is not None:
        cv2.rectangle(img, (x1, y1), (x2, y2), colorB, border)
    cv2.putText(img, text, (ox, oy), font, scale, colorT, thickness)
    
    return img, [x1, y1, x2, y2]

def carParkCheck(img):
    carParkCount = 0
    for pos in poslist:
        x, y = pos
        carParkImg = img[y: y + height, x: x + width]
        countWhite = cv2.countNonZero(carParkImg)
        
        if countWhite < 115:
            carParkCount += 1
            color = (0, 255, 0)

        else:
            color = (0, 0, 255)
            
        cv2.rectangle(frame, pos, (pos[0] + width, pos[1] + height), color, 4)
        putTextRect(frame, str(countWhite), (x, y + height + 3), scale=1,
                   thickness=2, offset=0, colorR=countWhite)
    
    putTextRect(frame, f'Free: {carParkCount}/{len(poslist)}', (20, 150), scale=1,
                   thickness=2, offset=0, colorR=(0, 200, 0))
    
# Video #
while True:
    ret, frame = cap.read()
    
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgBlurThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    # imgMedian = cv2.medianBlur(imgBlurThreshold, 5)

    carParkCheck(imgBlurThreshold)
    
    if ret:
        cv2.imshow('Image 1', frame)
        cv2.imshow('Image 2', imgBlurThreshold)
        
    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
# Video #

# One Image #
# ret, frame = cap.read()
    
# imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
# imgBlurThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
# # imgBlur = cv2.medianBlur(imgBlurThreshold, 3)

# carParkCheck(imgBlurThreshold)

# if ret:
#     cv2.imshow('Image 1', frame)
#     cv2.imshow('Image 2', imgBlurThreshold)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
# One Image #