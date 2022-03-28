from turtle import position, width
import cv2
import pyautogui
import numpy as np
from time import time, sleep
import win32gui
import win32con
import win32ui
import imutils


def get_coordinates():
    pyautogui.alert(
        "Put your mouse cursor on the top right corner of the wheel.You have 2 seconds ")
    sleep(2)
    xtr1, ytr1 = pyautogui.position()

    pyautogui.alert(
        "Put your mouse cursor on the bottm left corner of wheel.You have 2 seconds ")
    sleep(2)
    xbl1, ybl1 = pyautogui.position()

    pyautogui.alert(
        "Put your mouse cursor on the top right of the ball box.You have 2 seconds ")
    sleep(2)
    xtrbb, ytrbb = pyautogui.position()

    pyautogui.alert(
        "Put your mouse cursor on the bottm left of the ball box.You have 2 seconds ")
    sleep(2)
    xblbb, yblbb = pyautogui.position()

    """pyautogui.alert(
        "Put your mouse cursor on the left of the rotor.You have 2 seconds ")
    sleep(2)
    x_rotor_1, y_rotor = pyautogui.position()

    pyautogui.alert(
        "Put your mouse cursor on the right of the rotor.You have 2 seconds ")
    sleep(2)
    x_rotor_2, y_rotor = pyautogui.position()"""

    return xtr1, ytr1, xbl1, ybl1, xtrbb, ytrbb, xblbb, yblbb


def get_screenshot():
    w = 1920
    h = 1080
    hwnd = None

    # get the window image data
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

    # convert the raw data into a format opencv can read
    # dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    # free resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    img = np.ascontiguousarray(img)

    return img

# return the box containg roulette wheel Using numpy slicing.


def crop_screenshot(screenshot, xtr, ytr, xbl, ybl):
    return screenshot[ytr:ybl,
                      xbl:xtr]

# return blurred grayed image


def gray_blur_image(image):

    # convert image to gray
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blur the image  We should specify the width and height of the kernel which should be positive and odd.
    blurred_image = cv2.GaussianBlur(gray_image, (17, 17), 0)
    return blurred_image

# return the baseline frame that we are going to compare the video capture frames against


def get_baseline(xtr, ytr, xbl, ybl):
    screenshot = get_screenshot()

    #   we put the elipse to hide the moving rotator and only detect the ball
    base_line_image = crop_screenshot(screenshot, xtr, ytr, xbl, ybl)
    # base_line_image = cv2.ellipse(
    # base_line_image, center, axis, 0, 0, 360, (0, 0, 255), thickness=-1)

    base_line_image = gray_blur_image(base_line_image)
    return base_line_image


def track_ball(base_line_image_for_ball, image):
    # return the contour of the moving ball

    # we put the elipse to hide the moving rotator and only detect the ball
    # image = cv2.ellipse(
    #  image, center, axis, 0, 0, 360, (0, 0, 255), thickness=-1)

    gray_image_for_ball = gray_blur_image(image)

    # Calculating the absolute difference between baseline image and incoming images and image thresholding
    delta = cv2.absdiff(base_line_image_for_ball, gray_image_for_ball)
    threshold = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(threshold, None, iterations=2)
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    return contours


xtr1, ytr1, xbl1, ybl1, xtrbb, ytrbb, xblbb, yblbb = get_coordinates()
# this value work for evoltion speed auto roulette classic view
# xtr1, ytr1, xbl1, ybl1, center, minor_axis, major_axis = 1292, 166, 622, 550, (
# 949, 353), 105, 125
base_line_image_for_ball = get_baseline(xtrbb, ytrbb, xblbb, yblbb)

t = time()
times = []
while True:
    screenshot = get_screenshot()
    main_image = crop_screenshot(screenshot, xtr1, ytr1, xbl1, ybl1)

    image = crop_screenshot(screenshot, xtrbb, ytrbb, xblbb, yblbb)
    image_for_green = image.copy()

    # draw line for angular speed
    # main_image = cv2.rectangle(
    #   main_image, (290, 30), (350, 100), (0, 0, 255), 2)

    # track ball

    contours = track_ball(base_line_image_for_ball, image)
    if contours is not None:
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

            v = time()-t
            if v > 0.31:

                print(v)
                t = time()
                times.append(v)

            cv2.rectangle(image, (x, y),
                          (x + w, y + h), (0, 255, 0), 2)

    # track green
    """hsv = cv2.cvtColor(image_for_green, cv2.COLOR_BGR2HSV)
    lower_green = np.array([])
    upper_green = np.array([])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    result = cv2.bitwise_and(image_for_ball, image_for_ball, mask=mask)
    cv2.imshow("screen_recorder2", image)"""

    cv2.imshow("screen_recorder", main_image)
    cv2.imshow("screen_recorder12", image)

    if cv2.waitKey(1) == ord("q"):
        cv2.destroyAllWindows()
        print(times)
        print(np.average(times))
        break
