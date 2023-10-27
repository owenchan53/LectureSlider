import cv2 as cv
import time

index = 1

# Initialize video capture
video_capture = cv.VideoCapture('test.mp4')

# Define an initial frame
ret, previous_frame = video_capture.read()
if not ret:
    exit()

# Initialize a timestamp variable to track the last screenshot time
last_screenshot_time = time.time()

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Convert frames to grayscale for easier comparison
    previous_frame_gray = cv.cvtColor(previous_frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Calculate the absolute difference between frames
    frame_diff = cv.absdiff(previous_frame_gray, frame_gray)

    # Define a threshold to consider as a change
    threshold = 30
    _, thresholded_frame = cv.threshold(frame_diff, threshold, 255, cv.THRESH_BINARY)

    # Count the number of changed pixels
    num_changed_pixels = cv.countNonZero(thresholded_frame)

    # Check if the minimum delay of 5 seconds has passed since the last screenshot
    current_time = time.time()
    if current_time - last_screenshot_time >= 5:
        if num_changed_pixels > 1000:  # Adjust this threshold as needed
            # Significant change detected - take a screenshot
            screenshot = frame.copy()
            cv.imwrite(f'slide{index}.png', screenshot)
            index += 1
            last_screenshot_time = current_time  # Update the last screenshot time

    # Update the previous frame for the next iteration
    previous_frame = frame

# Release the video capture and close OpenCV windows
video_capture.release()
cv.destroyAllWindows()
