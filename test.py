import cv2
import numpy
import pyautogui
import time

PIC_DIR = "debug/"


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
    def substep(i, filename, min, max, clicks=1, interval=0):
        while True:
            p = screenshot()
            cv2.imwrite(PIC_DIR+"p"+str(i)+".png", p)

            pos = findImage(p, filename, min, max)
            if not pos:
                print("Does not find the icon of icons.")
                continue
            pyautogui.click(pos, clicks=clicks,
                            interval=interval, duration=0.2)
            time.sleep(0.2)
            break
    substep(1, "iconarrow.png", [0.7, 0.8], [1, 1])
    substep(2, "wxicon.png", [0.7, 0.7], [1, 1], clicks=2, interval=0.2)
    substep(3, "programentry.png", [0, 0.6], [0.2, 0.9])
    substep(4, "programicon.png", [0, 0.5], [0.2, 0.8])
    substep(5, "record.png", [0.4, 0.4], [0.6, 0.6])


if __name__ == "__main__":
    main()
