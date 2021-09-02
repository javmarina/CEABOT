import cv2 as cv
import cv2.aruco as aruco

numMarkers = 2
markerSize = 4
CUSTOM_DICT = aruco.custom_dictionary(numMarkers, markerSize, 0)


def get_custom_dict():
    return CUSTOM_DICT


if __name__ == "__main__":
    pixels_per_cell = 10
    for i in range(numMarkers):
        img = aruco.drawMarker(CUSTOM_DICT, i, pixels_per_cell*(markerSize+2))
        cv.imwrite("marker{:d}.png".format(i), img)
