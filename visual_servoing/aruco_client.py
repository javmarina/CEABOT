

class ArucoClient(object):
    def __init__(self, target_marker: int = -1):
        self._last_marker = target_marker

        self.corners = None
        self.image = None

    def _get_marker(self, ids):
        """
        Parses an ArUco ids vector and gets the index for the last used marker, or
        simply the first one found if the last one was not seen. Returns -1 if nothing found.
        """
        if len(ids) == 0:
            return None, None
        marker_idx = self._find_marker(ids, self._last_marker)
        if marker_idx != -1:
            return self._last_marker, marker_idx
        else:
            self._last_marker = ids[0]
            return ids[0], 0

    @staticmethod
    def _find_marker(ids, marker_num):
        """
        Finds index of marker #marker_num in the ArUco ids vector. If not found, returns -1.
        """
        for i, id in enumerate(ids):
            if id == marker_num:
                return i
        return -1

    def _get_image(self, image):
        """
        # Dummy function to save incoming images
        """
        self.image = image

    def _process_detection(self, aruco_detection):
        """
        Process income ArUco detections message, store corners if detections were found.
        """

        corners, ids, rejectedImgPoints = aruco_detection

        # Get best marker for gripper pose
        (my_marker, marker_pos) = self._get_marker(ids=ids)

        if my_marker is None:
            return

        self.corners = corners[marker_pos]
