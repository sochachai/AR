import cv2
import numpy as np

# Load the reference image
img1 = cv2.imread("reference.jpg")
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
h, w, c = img1.shape
# Load the camera
cap = cv2.VideoCapture(0)



myVid = cv2.VideoCapture('Video_Tam.mp4')
detection = False
frameCounter = 0
success, imgVideo = myVid.read()
imgVideo = cv2.resize(imgVideo,(w,h))


def stackImages(imgArray,scale,labels=[]):
    sizeW= imgArray[0][0].shape[1]
    sizeH = imgArray[0][0].shape[0]
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (sizeW,sizeH), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((sizeH, sizeW, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (sizeW, sizeH), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(labels) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        #print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,labels[d],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    imgAug = frame.copy()
    gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect keypoints and compute descriptors
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    if detection == False:
        myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frameCounter = 0
    else:
        if frameCounter == myVid.get(cv2.CAP_PROP_FRAME_COUNT):
            myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0
        success, imgVideo = myVid.read()
        imgVideo = cv2.resize(imgVideo, (w, h))

    # Match the descriptors
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Filter the matches using the ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])
            #print(kp1[m.queryIdx].pt)
    #print(len(good))
    # Draw the matches
    img3 = cv2.drawMatchesKnn(img1, kp1, frame, kp2, good, None, flags=2)
    srcPts = np.float32([kp1[m[0].queryIdx].pt for m in good])


    if len(good) > 20:
        detection = True
        srcPts = np.float32([kp1[m[0].queryIdx].pt for m in good]).reshape(-1,1,2)
        dstPts = np.float32([kp2[m[0].trainIdx].pt for m in good]).reshape(-1,1,2)
        matrix, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5)
        #print(matrix)
        pts = np.float32([[0,0],[0,h],[w,h],[w,0]]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts, matrix)
        img4 = cv2.polylines(frame,[np.int32(dst)],True,(255,0,255),3)
        imgWarp = cv2.warpPerspective(imgVideo,matrix,(frame.shape[1],frame.shape[0]))

        maskNew = np.zeros((frame.shape[0],frame.shape[1]),np.uint8)
        cv2.fillPoly(maskNew, [np.int32(dst)],(255,255,255)) #white
        maskInv = cv2.bitwise_not(maskNew) #black
        imgAug = cv2.bitwise_and(imgAug,imgAug, mask = maskInv)
        imgAug = cv2.bitwise_or(imgWarp, imgAug)
        imgStacked = stackImages(([frame, imgVideo, img1], [img3, imgWarp, imgAug]), 0.5)


    # Display the resulting frame
    cv2.imshow('Video_on_Drink', imgAug)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    frameCounter += 1




# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
