from turtle import position, width
import cv2
import pyautogui
import numpy as np
from time import time, sleep
import win32gui
import win32con
import win32ui
import imutils

# get coordinates of the top right corner and the bottm left corner of each box containing each deflactor


def get_position():
    pyautogui.alert(
        "Put your mouse cursor on the top right corner of the wheel.You have 2 seconds ")
    sleep(2)
    xtr1, ytr1 = pyautogui.position()  # coordinate of the first deflector

    pyautogui.alert(
        "Put your mouse cursor on the bottm left corner of wheel.You have 2 seconds ")
    sleep(2)
    xbl1, ybl1 = pyautogui.position()

    pyautogui.alert(
        "Put your mouse cursor on the center.You have 2 seconds ")
    sleep(2)
    center = pyautogui.position()

    pyautogui.alert(
        "Put your mouse cursor on the top of the rotor.You have 2 seconds ")
    sleep(2)
    x_rotor, y_rotor_1 = pyautogui.position()

    pyautogui.alert(
        "Put your mouse cursor on the bottm of the rotor.You have 2 seconds ")
    sleep(2)
    x_rotor, y_rotor_2 = pyautogui.position()

    pyautogui.alert(
        "Put your mouse cursor on the left of the rotor.You have 2 seconds ")
    sleep(2)
    x_rotor_1, y_rotor = pyautogui.position()

    pyautogui.alert(
        "Put your mouse cursor on the right of the rotor.You have 2 seconds ")
    sleep(2)
    x_rotor_2, y_rotor = pyautogui.position()

    minor_axis = y_rotor_2-y_rotor_1
    major_axis = x_rotor_2-x_rotor_1

    return xtr1, ytr1, xbl1, ybl1, center, major_axis, minor_axis


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

    # drop the alpha channel, or cv.matchTemplate() will throw an error like:
    #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type()
    #   && _img.dims() <= 2 in function 'cv::matchTemplate'

    # make image C_CONTIGUOUS to avoid errors that look like:
    #   File ... in draw_rectangles
    #   TypeError: an integer is required (got type tuple)
    # see the discussion here:
    # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
    img = np.ascontiguousarray(img)

    return img


def crop_screenshot(screenshot, xtr, ytr, xbl, ybl):
    return screenshot[ytr:ybl,
                      xbl:xtr]


def gray_blur_image(image):

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (17, 17), 0)
    return blurred_image


def Hough_circles(threshold,):
    circles = cv2.HoughCircles(threshold, cv2.HOUGH_GRADIENT, 1.2,
                               100, param1=5, param2=20, minRadius=1, maxRadius=10
                               )

    if circles is not None:
        circles = np.round(circles[0, :].astype("int"))
        for (x, y, r) in circles:
            cv2.circle(threshold, (x, y), r, (0, 255, 0), 4)


# xtr1, ytr1, xbl1, ybl1, center, major_axis, minor_axis = get_position()
sleep(4)
xtr1, ytr1, xbl1, ybl1, center, minor_axis, major_axis = 1292, 166, 622, 550, (
    949, 353), 105, 125
screenshot = get_screenshot()
base_line_image = crop_screenshot(screenshot, xtr1, ytr1, xbl1, ybl1)


base_line_image_for_ball = gray_blur_image(base_line_image)
base_line_image_for_ball = cv2.ellipse(
    base_line_image, (327, 192), (major_axis, minor_axis), 0, 0, 360, (255, 255, 255), thickness=-1)

print(base_line_image_for_ball.shape)

f = time()
times = []
while True:
    screenshot = get_screenshot()

    image = crop_screenshot(screenshot, xtr1, ytr1, xbl1, ybl1)

    gray_image_for_ball = gray_blur_image(image)
    gray_image_for_ball = cv2.ellipse(
        gray_image_for_ball, (327, 192), (major_axis, minor_axis), 0, 0, 360, (255, 255, 255), thickness=-1)
    print(gray_image_for_ball.shape)

    # Calculating the absolute difference between baseline image and incoming images and image thresholding
    delta = cv2.absdiff(base_line_image_for_ball, gray_image_for_ball)

    threshold = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(threshold, None, iterations=2)
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

    cv2.imshow("screen_recorder", image)
    cv2.imshow("threshhold", threshold)
    times.append(1/(time()-f))

    f = time()

    if cv2.waitKey(1) == ord("q"):
        cv2.destroyAllWindows()
        print(times)
        print(np.average(times))
        break
