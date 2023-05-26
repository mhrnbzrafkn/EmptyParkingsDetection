import cv2
import pickle

width, height = 20, 50

imgLocationsPath = './src/vidFirstFrame.png'
cap = cv2.VideoCapture('./src/vid-01.mp4')
ret, frame = cap.read()
cv2.imwrite(imgLocationsPath, frame)

try:
    with open('CarParkPos', 'rb') as f:
        poslist = pickle.load(f)
except:
    poslist = []
    
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        poslist.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(poslist):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                poslist.pop(i)
    
    with open('CarParkPos', 'wb') as f:
        pickle.dump(poslist, f)
        
while True:
    img = cv2.imread(imgLocationsPath)
    for pos in poslist:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
    
    cv2.imshow('Image', img)
    cv2.setMouseCallback('Image', mouseClick)
    if cv2.waitKey(40) == 27:
        break
        
cv2.destroyAllWindows()