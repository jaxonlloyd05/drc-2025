## CV2 COLOUR CONFIGURATION CODE. SOURCED FROM ZAC (OTHER MEMBER FOR UTS) ##
import cv2
import numpy as np

class HSVAdjuster:
    def __init__(self):
        self.window_name = "HSV Threshold Adjuster"
        self.lower_blue = np.array([100, 50, 120])
        self.upper_blue = np.array([150, 255, 255])

        # Create OpenCV window
        cv2.namedWindow(self.window_name)

        # Create trackbars for lower HSV
        cv2.createTrackbar("Lower H", self.window_name, self.lower_blue[0], 255, lambda x: None)
        cv2.createTrackbar("Lower S", self.window_name, self.lower_blue[1], 255, lambda x: None)
        cv2.createTrackbar("Lower V", self.window_name, self.lower_blue[2], 255, lambda x: None)

        # Create trackbars for upper HSV
        cv2.createTrackbar("Upper H", self.window_name, self.upper_blue[0], 255, lambda x: None)
        cv2.createTrackbar("Upper S", self.window_name, self.upper_blue[1], 255, lambda x: None)
        cv2.createTrackbar("Upper V", self.window_name, self.upper_blue[2], 255, lambda x: None)

    def get_thresholds(self):
        lh = cv2.getTrackbarPos("Lower H", self.window_name)
        ls = cv2.getTrackbarPos("Lower S", self.window_name)
        lv = cv2.getTrackbarPos("Lower V", self.window_name)
        uh = cv2.getTrackbarPos("Upper H", self.window_name)
        us = cv2.getTrackbarPos("Upper S", self.window_name)
        uv = cv2.getTrackbarPos("Upper V", self.window_name)

        self.lower_blue = np.array([lh, ls, lv])
        self.upper_blue = np.array([uh, us, uv])
        return self.lower_blue, self.upper_blue

    def run(self):
        cap = cv2.VideoCapture(0)  # Change to 'qut_demo.mov' if using a video

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower, upper = self.get_thresholds()

            mask = cv2.inRange(frame_HSV, lower, upper)
            result = cv2.bitwise_and(frame, frame, mask=mask)

            cv2.imshow(self.window_name, result)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = HSVAdjuster()
    app.run()
