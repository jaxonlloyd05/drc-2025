import cv2
import numpy as np

def process_frame(frame):
    """
        steering_value: float between -1 and 1 (0 is straight)
        processed_frame: visualized frame with detected lines highlighted
        finish_detected: boolean indicating if finish line (green) is detected
    """
    height, width = frame.shape[:2]
    half_width = width // 2

    frame = frame[:, :half_width]
    frame = cv2.flip(frame, -1)

    processed_frame = frame.copy()
    height, width = frame.shape[:2]
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # right side of track range
    blue_lower = np.array([96, 56, 51])
    blue_upper = np.array([111, 255, 255])
    
    # left side of track range
    yellow_lower = np.array([23, 20, 165])
    yellow_upper = np.array([53, 175, 255])
    
    # end of track range
    green_lower = np.array([40, 26, 116])
    green_upper = np.array([76, 255, 255])

    # mask image for ranges    
    blue_mask = cv2.inRange(hsv_frame, blue_lower, blue_upper)
    yellow_mask = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)

    green_mask = cv2.inRange(hsv_frame, green_lower, green_upper) 
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
    
    combined_mask = cv2.bitwise_or(blue_mask, cv2.bitwise_or(yellow_mask, green_mask))
    processed_frame = np.where(combined_mask[:, :, np.newaxis] > 0, frame, gray_frame)
    
    # look for green
    green_pixels = cv2.countNonZero(green_mask)
    finish_detected = green_pixels > (width * height * 0.05)
    
    # steering calc for mid of screen in bottom third
    roi_height = height // 3
    bottom_region = hsv_frame[height - roi_height:height, :]
    
    bottom_blue_mask = cv2.inRange(bottom_region, blue_lower, blue_upper)
    # bottom_blue_mask[:, :half_width] = 0

    bottom_yellow_mask = cv2.inRange(bottom_region, yellow_lower, yellow_upper)
    # bottom_yellow_mask[:, half_width:] = 0

    
    # find blue and yellow
    blue_moments = cv2.moments(bottom_blue_mask)
    yellow_moments = cv2.moments(bottom_yellow_mask)
    
    # Default to center position (0 for Servo library)
    steering_value = 0.0
    
    # Find both lines
    if blue_moments["m00"] > 0 and yellow_moments["m00"] > 0:
        # adjusted_blue_mask = blue_mask
        # adjusted_blue_mask[:, :half_width] = 0

        # adjusted_yellow_mask = yellow_mask
        # adjusted_yellow_mask[:, half_width:] = 0

        # adjusted_blue_moments = ...

        blue_x = int(blue_moments["m10"] / blue_moments["m00"])
        yellow_x = int(yellow_moments["m10"] / yellow_moments["m00"])
        
        # find center of lines
        center_x = (blue_x + yellow_x) // 2
        
        # Map center_x from 0-width to -1 to 1
        # 0 = left edge (-1), width/2 = center (0), width = right edge (1)
        steering_value = (center_x - (width / 2)) / (width / 2)
        
        # draw line for visuals
        print("both colors detected")
        cv2.line(processed_frame, (width//2, height), (center_x, height - roi_height), (0, 255, 255), 2)
    
    # if only blue steer left (away)
    elif blue_moments["m00"] > 0: 
        blue_x = int(blue_moments["m10"] / blue_moments["m00"])
        # Convert original 0-1 scale to -1 to 1 (shifting left)
        raw_steering = 0.3 - (0.3 * (1 - (blue_x / width)))  # 0 to 0.3 range
        steering_value = (raw_steering * 2) - 1
        
    # if only yellow steer right (away)
    elif yellow_moments["m00"] > 0:
        yellow_x = int(yellow_moments["m10"] / yellow_moments["m00"])
        # Convert original 0-1 scale to -1 to 1 (shifting right)
        raw_steering = 0.7 + (0.3 * (yellow_x / width))  # 0.7 to 1 range
        steering_value = (raw_steering * 2) - 1
        
    # Ensure steering value is between -1 and 1
    steering_value = max(-1.0, min(1.0, steering_value))
    
    cv2.putText(processed_frame, f"Steering: {steering_value:.2f}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    if finish_detected:
        cv2.putText(processed_frame, "FINISH LINE DETECTED", (width//2 - 150, height//2), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    
    return steering_value, processed_frame, finish_detected
