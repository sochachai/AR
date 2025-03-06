import cv2
import numpy as np

# Load the reference image
img1 = cv2.imread("../reference.jpg")
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
h, w, c = img1.shape
# Load the camera
cap = cv2.VideoCapture(0)

myVid = cv2.VideoCapture('video.mp4')
success, imgVideo = myVid.read()
imgVideo = cv2.resize(imgVideo,(w,h))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    imgAug = frame.copy()
    gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect keypoints and compute descriptors
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    # Match the descriptors
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Filter the matches using the ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])
            print(kp1[m.queryIdx].pt)
    #print(len(good))
    # Draw the matches
    img3 = cv2.drawMatchesKnn(img1, kp1, frame, kp2, good, None, flags=2)
    srcPts = np.float32([kp1[m[0].queryIdx].pt for m in good])


    #if len(good) > 50:

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


    # Display the resulting frame
    cv2.imshow('frame', imgAug)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

