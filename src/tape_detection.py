import cv2
import numpy as np

def detect_tapes(frame):
    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range for blue color
    blue_lower = np.array([100, 150, 50])
    blue_upper = np.array([140, 255, 255])

    # Define range for yellow color
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([40, 255, 255])

    # Create masks for blue and yellow tapes
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

    # Find contours for both colors
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return blue_contours, yellow_contours
