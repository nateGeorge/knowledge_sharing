from cmath import rect
import copy

import cv2
import numpy as np
from matplotlib import pyplot as plt

filename = r"C:\Users\words\Desktop\fat_cat.jpg"
img = cv2.imread(filename)
img = cv2.imread(cv2.samples.findFile(filename))
original_img = copy.deepcopy(img)
mask = np.zeros(img.shape[:2], np.uint8)
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)


rectangle = []
def shape_selection(event, x, y, flags, param):
    # references to the global variables
    global rectangle, original_img


    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        img = original_img
        rectangle = []
        rectangle = [(x, y)]

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        rectangle.append((x, y))

cv2.namedWindow("image")
cv2.setMouseCallback("image", shape_selection)
cv2.imshow("image", img)

while True:
    # display the image and wait for a keypress
    cv2.imshow("image", img)
    key = cv2.waitKey(1) & 0xFF

    # press 'r' to reset the window
    if key == ord("r"):
        img = original_img.copy()

    # if the 'q' key is pressed, break from the loop
    elif key == ord("q"):
        break

    # draw a rectangle around the region of interest
    if len(rectangle) > 1:
        cv2.rectangle(img, rectangle[0], rectangle[1], (0, 255, 0), 2)
        

print(rectangle)
cv2.destroyAllWindows()

# cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
# mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
# img = img*mask2[:,:,np.newaxis]

# plt.imshow(img),plt.colorbar(),plt.show()