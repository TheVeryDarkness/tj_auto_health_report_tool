import cv2
import numpy
import pyautogui
import time


def screenshot():
    capturePIL = pyautogui.screenshot()
    captureCV = numpy.array(capturePIL)
    captureCV = cv2.cvtColor(captureCV, cv2.COLOR_RGB2BGR)
    return captureCV


def findImage(img, filename, min, max):
    to_find = cv2.imread(filename)
    match = cv2.matchTemplate(img, to_find,
                              method=cv2.TM_CCOEFF_NORMED)
    filtered = numpy.where(match >= 0.8)
    [h, w,  _] = img.shape
    posList = [pt for pt in zip(*filtered[::-1])]
    posInRange = [pt for pt in posList if min[0]*w < pt[0]
                  < max[0]*w and min[1]*h < pt[1] < max[1]*h]
    if len(posInRange) > 0:
        return posInRange[0]
    else:
        return None


def main():
    while True:
        p1 = screenshot()
        cv2.imwrite("p1.png", p1)

        iconArrowPos = findImage(p1, "iconarrow.png", [0.7, 0.8], [1, 1])
        if not iconArrowPos:
            print("Does not find the icon of icons.")
            continue
        pyautogui.click(iconArrowPos, duration=0.2)
        break

    while True:
        time.sleep(0.2)

        p2 = screenshot()
        cv2.imwrite("p2.png", p2)

        wxIconPos = findImage(p2, "wxicon.png", [0.7, 0.7], [1, 1])
        if not wxIconPos:
            print("Does not find the icon of weixin.")
            continue
        pyautogui.click(wxIconPos, duration=0.2)
        break


if __name__ == "__main__":
    main()
