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
    range = [(int(min[0]*w), int(max[0]*w)), (int(min[1]*h), int(max[1]*h))]
    posInRange = [pt for pt in posList if range[0][0] < pt[0]
                  < range[0][1] and range[1][0] < pt[1] < range[1][1]]
    cv2.rectangle(img, range[0], range[1], color=(0, 255, 0))
    if len(posInRange) > 0:
        pos = posInRange[0]
        cv2.rectangle(
            img, pos, (pos[0]+to_find.shape[0], pos[1]+to_find.shape[1]), color=(255, 0, 0))
        return pos
    else:
        return None


def main():
    def subaction(i, name, min, max, clicks=1, interval=0):
        filename = name+".png"
        p = screenshot()
        pos = findImage(p, filename, min, max)
        cv2.imwrite(PIC_DIR+"p"+str(i)+".png", p)
        if not pos:
            return False
        if i != 10:
            pyautogui.click(pos, clicks=clicks,
                            interval=interval, duration=0.2)
        time.sleep(0.2)
        return True

    def substep(i, name, min, max, clicks=1, interval=0):
        while not subaction(i, name, min, max, clicks, interval):
            print("Does not find the icon of "+name+".")

    while True:
        substep(1, "iconarrow", [0.7, 0.8], [1, 1])
        substep(2, "wxicon", [0.7, 0.7], [1, 1], clicks=2, interval=0.2)
        substep(3, "programentry", [0, 0.6], [0.2, 0.9])
        substep(4, "programicon", [0, 0.5], [0.2, 0.8])
        substep(5, "record", [0.4, 0.4], [0.6, 0.6])
        while not subaction(6, "back", [0.4, 0.4], [0.6, 0.6]):
            print("Found to have not recorded yet at " + time.asctime() + ".")
            f = subaction(7, "selecthealth", [0.4, 0.4], [0.6, 0.6])
            f = f and subaction(8, "ensurehealth", [0.4, 0.4], [0.6, 0.6])
            f = f and subaction(9, "selectisolation", [0.4, 0.4], [0.6, 0.6])
            f = f and subaction(10, "ensureisolation", [0.4, 0.4], [0.6, 0.6])
            f = f and subaction(11, "commitrecord", [0.4, 0.6], [0.6, 0.8])
            if f:
                print("Record at " + time.asctime())
            print("But also does not find where to record.")
        else:
            print("Found to have already recorded at " + time.asctime() + ".")
        substep(12, "close", [0.5, 0.1], [0.7, 0.3])
        t = time.localtime(time.time())
        sec = t.tm_sec + t.tm_min * 60 + t.tm_hour * 60 * 60
        time.sleep(24 * 60 * 60 + 15 * 60 - sec)


if __name__ == "__main__":
    main()
