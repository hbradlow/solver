import cv2

def crop(f, bbs):
    img = cv2.imread(f)
    i = 0
    for box in bbs:
        cv2.imwrite("tmp"+str(i), img[x1:x2, y1:y2])
        i += 1
